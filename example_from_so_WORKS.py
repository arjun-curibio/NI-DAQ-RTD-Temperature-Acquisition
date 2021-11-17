"""
Analog data acquisition for QuSpin's OPMs via National Instruments' cDAQ unit
The following assumes:
"""
folder = "C:/Users/Nanosurface/Desktop/2.1.5-Board-Thermal-Testing/11_15_21 Testing/"

fname = 'test'

WELL_POSITIONS = ['B1', 'Under Well Plate', 'B4', 'C6']

PLOTTER_WINDOW = 15 # seconds
savefigFlag = True
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
import pickle
from datetime import datetime
import scipy.io
from os.path import exists

# Parameters
sampling_freq_in = 1  # in Hz
buffer_in_size = 1
bufsize_callback = buffer_in_size
buffer_in_size_cfg = round(buffer_in_size * 1)  # clock configuration
chans_in = 4  # set to number of active OPMs (x2 if By and Bz are used, but that is not recommended)
refresh_rate_plot = 1  # in Hz
crop = 0  # number of seconds to drop at acquisition start before saving

plotter_grid_size = 10
# fname = 'test'
my_filename = folder + fname

print(' ')

print(my_filename)
print(' ')
rewriteFlag = False
acquisition_date = datetime.now().strftime('%m/%d/%y')
acquisition_start_time = datetime.now().strftime('%H:%M:%S')

# Initialize data placeholders
buffer_in = np.zeros((chans_in, buffer_in_size))
data = np.zeros((chans_in, 0))


# Definitions of basic functions
def ask_user():
    global running
    input("Close window to stop acquisition.\n")
    running = False


def cfg_read_task():  # uses above parameters
    task = nidaqmx.Task()
    
    task.ai_channels.add_ai_rtd_chan("RTD4_1/ai0", 
        current_excit_source=constants.ExcitationSource.INTERNAL, 
        current_excit_val=0.001, 
        resistance_config=constants.ResistanceConfiguration.FOUR_WIRE)
    
    task.ai_channels.add_ai_rtd_chan("RTD4_1/ai1", 
        current_excit_source=constants.ExcitationSource.INTERNAL, 
        current_excit_val=0.001, 
        resistance_config=constants.ResistanceConfiguration.FOUR_WIRE)
    task.ai_channels.add_ai_rtd_chan("RTD4_1/ai2", 
        current_excit_source=constants.ExcitationSource.INTERNAL, 
        current_excit_val=0.001, 
        resistance_config=constants.ResistanceConfiguration.FOUR_WIRE)
    task.ai_channels.add_ai_rtd_chan("RTD4_1/ai3", 
        current_excit_source=constants.ExcitationSource.INTERNAL, 
        current_excit_val=0.001, 
        resistance_config=constants.ResistanceConfiguration.FOUR_WIRE)
    
    task.timing.cfg_samp_clk_timing(rate=sampling_freq_in, sample_mode=constants.AcquisitionType.CONTINUOUS,
        samps_per_chan=buffer_in_size_cfg)
    
    return task
                    


def reading_task_callback(task_idx, event_type, num_samples, callback_data):  # bufsize_callback is passed to num_samples
    global data
    global buffer_in

    if running:
        # It may be wiser to read slightly more than num_samples here, to make sure one does not miss any sample,
        # see: https://documentation.help/NI-DAQmx-Key-Concepts/contCAcqGen.html
        buffer_in = np.zeros((chans_in, num_samples))  # double definition ???
        stream_in.read_many_sample(buffer_in, num_samples, timeout=constants.WAIT_INFINITELY)

        data = np.append(data, buffer_in, axis=1)  # appends buffered data to total variable data

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
time_start = datetime.now()
task.start()


# Plot a visual feedback for the user's mental health
f, ax = plt.subplots(1, 2)

time_keeper=0
while running and plt.get_fignums():  # make this adapt to number of channels automatically
    t0 = datetime.now()
    ax1 = ax[0]
    ax2 = ax[1]

    ax1.clear()

    ax1.plot(data.T)
    ax1.legend(WELL_POSITIONS, loc='upper left')
    # Label and axis formatting
    ax1.set_xlabel('time [s]')
    ax1.set_ylabel('Temperature [C]')
    
    xlim1 = ax1.get_xlim()
    xticks = np.arange( start=plotter_grid_size*floor(xlim1[0]/plotter_grid_size), 
                        stop=plotter_grid_size*ceil(xlim1[1]/plotter_grid_size), 
                        step=plotter_grid_size)
    # xticklabels = np.arange(0, xticks.size, 1)
    ax1.set_xticks(xticks)

    ax1.set_xlim([max([0, time_keeper-PLOTTER_WINDOW-1]), data.shape[1]-1])
    if bool(sum(data[:, -1:].T.squeeze())):
        ax1.set_ylim([floor(np.amin(data[:,-15:], axis=(0,1))*10)/10, ceil(np.amax(data[:,-15:], axis=(0,1))*10)/10])
    
    # ax1.set_xticklabels(xticklabels)
    ax1.grid(True,axis='x')
    ax1.yaxis.set_ticks_position("right")
    ax1.grid(True,axis='y')
    print(data[:,-1:].T.squeeze())
    
    ax2.clear()
    ax2.plot(data.T)
    ax2.set_xlabel('time [s]')
    ax2.set_ylabel('Temperature [C]')
    ax2.grid(True)
    ax2.yaxis.set_ticks_position("right")
    # ax2.set_xticks( np.arange(0, plotter_grid_size*ceil(data.shape[1]/plotter_grid_size), plotter_grid_size))
    if bool(sum(data[:, -1:].T.squeeze())):
        ax2.set_ylim([floor(np.amin(data, axis=(0,1))*10)/10, ceil(np.amax(data, axis=(0,1))*10)/10])
    
    plt.pause(1/refresh_rate_plot-(datetime.now()-t0).total_seconds())  # required for dynamic plot to work (if too low, nulling performance bad)

    time_keeper += 1

# Close task to clear connection once done
task.close()
duration = datetime.now() - time_start

#%%
# Final save data and metadata ... first in python reloadable format:
filename = my_filename

if rewriteFlag == False:
    ii=0
    while exists(filename + '.csv'):
        filename = my_filename + str(ii)
        ii += 1

import pandas as pd

df = pd.DataFrame(data.T, columns=WELL_POSITIONS, )
df.to_csv(filename + '.csv', sep=',')

print(df)

with open(filename + '_info.txt', 'w') as f:
    f.write('Acquisition Date: ' + acquisition_date + '\n')
    f.write('Acquisition Start Time: ' + acquisition_start_time+ '\n')
    f.write('Sampling rate: ' + str(sampling_freq_in) + ' Hz'+ '\n')
    f.write('Number of RTD elements: ' + str(chans_in)+ '\n')


"""
print(df)
with open(filename, 'wb') as f:
    pickle.dump(data, f)
'''
Load this variable back with:
with open(name, 'rb') as f:
    data_reloaded = pickle.load(f)
'''
# Human-readable text file:
extension = '.txt'
np.set_printoptions(threshold=np.inf, linewidth=np.inf)  # turn off summarization, line-wrapping
with open(filename + extension, 'w') as f:
    f.write('Acquisition Date: ' + acquisition_date + '\n')
    f.write('Acquisition Start Time: ' + acquisition_start_time+ '\n')
    f.write('Sampling rate: ' + str(sampling_freq_in) + ' Hz'+ '\n')
    f.write('Number of RTD elements: ' + str(chans_in)+ '\n')
    f.write(np.array2string(data.T, separator=', '))  # improve precision here!
# Now in matlab:
# extension = '.mat'
# scipy.io.savemat(filename + extension, {'data':data})

"""
# Some messages at the end
num_samples_acquired = data[0,:].size
print("\n")

print("Acquisition duration: {}.".format(duration))
print("Acquired samples: {}.".format(num_samples_acquired - 1))


print("Close the window and press ENTER in the Terminal to close program.")

# Final plot of whole time course the acquisition
plt.close('all')
f_tot, ax1 = plt.subplots(1, 1, sharex='all', sharey='none')
ax1.plot(np.arange(0, data.shape[1], 1)/60, data.T)  

# Label formatting ...
ax1.legend(WELL_POSITIONS, loc='upper left')
ax1.set_ylabel('Temperature [C]')
ax1.set_xlabel('Time [m]')
ax1.grid(True)
#xticks = np.arange(0, data[0, :].size, sampling_freq_in)
#xticklabels = np.arange(0, xticks.size, 1)
# ax1.set_xticks(xticks)
# ax1.set_xticklabels(xticklabels)
print(df)
if savefigFlag:
    plt.savefig(filename + '.png', format='png')

plt.show()
# %%
