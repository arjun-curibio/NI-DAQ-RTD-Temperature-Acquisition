"""
Analog data acquisition for QuSpin's OPMs via National Instruments' cDAQ unit
The following assumes:
"""
folder = "C:/Users/achar/Documents/GitHub/NI-DAQ-RTD-Temperature-Acquisition/"

# fname = '2.1.5_100mA_6Hz_10ms_CoolingPlate_36.0C'
fname = 'test' # setting this variable to 'monitor' does not save any data or figures

PLOTTER_WINDOW = 30 # seconds
savefigFlag = True # save the final plot to a separate figure (RECOMMEND TO SET TO TRUE)
rewriteFlag = True # If you want to re-write file, otherwise append number to filename (RECOMMENDED TO SET TO FALSE)

dontInclude = [0,7] # do not include these channels
CHANNEL_NAMES = [
    'cDAQ1Mod1/ai7', # 0
    'cDAQ1Mod1/ai5', # 1
    'cDAQ1Mod2/ai0', # 2
    'cDAQ1Mod2/ai2', # 3
    'cDAQ1Mod1/ai3', # 4
    'cDAQ1Mod1/ai1', # 5
    'cDAQ1Mod1/ai4', # 6
    'cDAQ1Mod1/ai2', # 7
    'cDAQ1Mod1/ai0', # 8
    'cDAQ1Mod2/ai1', # 9
    'cDAQ1Mod1/ai6', # 10
    'cDAQ1Mod2/ai3'  # 11
]
    
CHANNEL_MAP = [
    'A1', # 0
    'A2', # 1
    'A5', # 2
    'A6', # 3
    'B3', # 4
    'B4', # 5
    'C2', # 6
    'C3', # 7
    'C4', # 8
    'C5', # 9
    'D1', # 10
    'D6'  # 11
]
for ii in dontInclude:
    CHANNEL_NAMES.pop(ii)
    CHANNEL_MAP.pop(ii)
# Imports
import matplotlib.pyplot as plt
import numpy as np
from math import floor, ceil

import nidaqmx
from nidaqmx.stream_readers import AnalogMultiChannelReader
from nidaqmx import constants
# from nidaqmx import stream_readers  # not needed in this script
# from nidaqmx import stream_writers  # not needed in this script

import threading
from datetime import datetime
from time import time
from os.path import exists

import pandas as pd

# Parameters
sampling_freq_in = 1  # in Hz, limited by hardware and number of channels (may collected duplicate data if to high)
buffer_in_size = 1 # number of samples to collect on each channel to store in buffer before sending to computer
bufsize_callback = buffer_in_size
buffer_in_size_cfg = round(buffer_in_size * 1)  # clock configuration
chans_in = len(CHANNEL_NAMES)  # set to number of active OPMs
refresh_rate_plot = 10  # in Hz
crop = 0  # number of seconds to drop at acquisition start before saving


plotter_grid_size = 5
# fname = 'test'
my_filename = folder + fname

print(' ')

print(my_filename)
print(' ')

filename = my_filename
if rewriteFlag == False:
    ii=0
    while exists(filename + '.csv'):
        filename = my_filename + str(ii)
        ii += 1

if fname == 'monitor':
    pass
else:
    with open(filename + '.csv', 'a') as f:
        f.write(','+','.join(CHANNEL_MAP) + '\n')

# Initialize data placeholders
buffer_in = np.zeros((chans_in, buffer_in_size))
data = np.zeros((chans_in, 0))
t = []

# Definitions of basic functions
def ask_user():
    global running
    input("Close window to stop acquisition.\n")
    running = False


def cfg_read_task():  # uses above parameters
    global task
    task = nidaqmx.Task()
    
    for ii in range(chans_in):
        task.ai_channels.add_ai_rtd_chan(CHANNEL_NAMES[ii],
            current_excit_source=constants.ExcitationSource.INTERNAL, 
        current_excit_val=0.001, 
        resistance_config=constants.ResistanceConfiguration.FOUR_WIRE,
        rtd_type=constants.RTDType.PT_3750)
    
    task.timing.cfg_samp_clk_timing(rate=sampling_freq_in, sample_mode=constants.AcquisitionType.CONTINUOUS,
        samps_per_chan=buffer_in_size_cfg)
    
    return task
                    


def reading_task_callback(task_idx, event_type, num_samples, callback_data):  # bufsize_callback is passed to num_samples
    global data
    global buffer_in
    global t
    if running:
        # It may be wiser to read slightly more than num_samples here, to make sure one does not miss any sample,
        # see: https://documentation.help/NI-DAQmx-Key-Concepts/contCAcqGen.html
        buffer_in = np.zeros((chans_in, num_samples))  # double definition ???
        stream_in.read_many_sample(buffer_in, num_samples, timeout=constants.WAIT_INFINITELY)

        data = np.append(data, buffer_in, axis=1)  # appends buffered data to total variable data
        t.append(time())
        if fname == 'monitor':
            pass
        else:
            with open(filename + '.csv', 'a') as f:
                f.write(str(t[-1] - t[0]) + ',')
                for ii in range(chans_in):
                    f.write(str(data[ii,-1])+', ')
                f.write('\n')

    return 0  # Absolutely needed for this callback to be well defined (see nidaqmx doc).


# Configure and setup the tasks
task = cfg_read_task()
stream_in = AnalogMultiChannelReader(task.in_stream)
task.register_every_n_samples_acquired_into_buffer_event(bufsize_callback, reading_task_callback)


# Start threading to prompt user to stop
thread_user = threading.Thread(target=ask_user)
thread_user.start()


# Main loop
running = True
task.start()
t0 = datetime.now()
acquisition_date = t0.strftime('%m/%d/%y')
acquisition_start_time = t0.strftime('%H:%M:%S')

# Save Metadata to <filename>_info.txt
if fname != 'monitor':
    with open(filename + '_info.txt', 'a') as f:
        f.write('Acquisition Date: ' + acquisition_date + '\n')
        f.write('Acquisition Start Time: ' + acquisition_start_time+ '\n')
        f.write('Sampling rate: ' + str(sampling_freq_in) + ' Hz'+ '\n')
        f.write('Number of RTD elements: ' + str(chans_in)+ '\n')
        f.write('\n')
        f.write('Channel Mapping:\n')
        for ii in range(chans_in):
            f.write('Channel '+str(CHANNEL_NAMES[ii])+' --> Well '+str(CHANNEL_MAP[ii]+'\n'))
        f.write('\n')

# Plot a visual feedback for the user's mental health
f, ax = plt.subplots(2,1)
while running and plt.get_fignums():
    ti = datetime.now()
    ax1 = ax[0]
    ax2 = ax[1]

    ax1.clear()

    ax1.plot(data.T[:,-PLOTTER_WINDOW:])
    ax1.legend(CHANNEL_MAP, loc='upper left', ncol=2)
    # Label and axis formatting
    # ax1.set_xlabel('time [s]')
    ax1.set_ylabel('Temperature [C]')
    
    xlim1 = ax1.get_xlim()
    xticks = np.arange( start=plotter_grid_size*floor(xlim1[0]/plotter_grid_size), 
                        stop =plotter_grid_size*ceil(xlim1[1] /plotter_grid_size), 
                        step =plotter_grid_size)
    # xticklabels = np.arange(0, xticks.size, 1)
    ax1.set_xticks(xticks)

    if data.shape[1] <= PLOTTER_WINDOW:
        ax1.set_xlim([0, PLOTTER_WINDOW-1])
        xlim1 = ax1.get_xlim()
        xticks = np.arange( start=plotter_grid_size*floor(xlim1[0]/plotter_grid_size), 
                            stop =plotter_grid_size*ceil(xlim1[1] /plotter_grid_size), 
                            step =plotter_grid_size)
        ax1.set_xticks(xticks)
    else:
        ax1.set_xlim([data.shape[1]-PLOTTER_WINDOW-1, data.shape[1]-1])
    
    
    if bool(sum(data[:, -1:].T.squeeze())):
        ax1.set_ylim([ floor(np.amin(data[:,-PLOTTER_WINDOW:], axis=(0,1))*plotter_grid_size)/plotter_grid_size, 
                        ceil(np.amax(data[:,-PLOTTER_WINDOW:], axis=(0,1))*plotter_grid_size)/plotter_grid_size])
    # print(data.shape)
    # ax1.set_xticklabels(xticklabels)
    ax1.grid(True)
    ax1.yaxis.set_ticks_position("right")

    ax2.clear()
    ax2.plot(data.T)
    ax2.set_xlabel('time [s]')
    ax2.set_ylabel('Temperature [C]')
    ax2.grid(True)
    ax2.yaxis.set_ticks_position("right")
    if data.shape[1] == 1:
        ax2.set_xlim([0, 1])
    else:
        ax2.set_xlim([0, data.shape[1]-1])
    
    f.suptitle(fname)
    
    plt.pause(0.01)  # required for dynamic plot to work (if too low, nulling performance bad)


duration = datetime.now() - t0
# Close task to clear connection once done
task.close()

#%%
# Final save data and metadata ... first in python reloadable format:

import pandas as pd
print(CHANNEL_MAP)
print(data.T)
df = pd.DataFrame(data.T, columns=CHANNEL_MAP, index=[(i-t[0]) for i in t])
# df.to_csv(filename + '.csv', sep=',')

# Some messages at the end
num_samples_acquired = data[0,:].size
print("\n")

print("Acquisition duration: {}.".format(duration))
print("Acquired samples: {}.".format(num_samples_acquired - 1))


# Final plot of whole time course the acquisition
plt.close('all')
f_tot, ax1 = plt.subplots(1, 1, sharex='all', sharey='none')
ax1.plot(np.arange(0, data.shape[1], 1)/60, data.T)  

# Label formatting ...
ax1.legend(CHANNEL_MAP)
ax1.set_ylabel('Temperature [C]')
ax1.set_xlabel('Time [m]')
ax1.grid(True)

print(df)
if savefigFlag and fname != 'monitor':
    plt.savefig(filename + '.png', format='png')

print("Close the window and press ENTER in the Terminal to close program.")

plt.show(block='False')

# %%
