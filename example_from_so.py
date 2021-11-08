"""
    Python script for accessing NI cDAQ instruments.  For RTD sensing for Mantarray heating during recording/stimulating
"""

# Imports
from msilib.schema import Error
import matplotlib.pyplot as plt
import numpy as np

import nidaqmx
from nidaqmx.stream_readers import AnalogMultiChannelReader
from nidaqmx import constants
# from nidaqmx import stream_readers  # not needed in this script
# from nidaqmx import stream_writers  # not needed in this script

import threading
import pickle
from datetime import datetime
import scipy.io

import sys

from pathlib import Path
downloads_path = str(Path.home() / "Downloads")

# Parameters
sampling_freq_in = 1  # in Hz
buffer_in_size = 1 # number of samples to keep in buffer before passing to memory
bufsize_callback = buffer_in_size
buffer_in_size_cfg = round(buffer_in_size * 1)  # clock configuration
chans_in = 1  # NEEDS TO CHANGE WITH NUMBER OF INPUTS
refresh_rate_plot = 1  # in Hz
crop = 10  # number of seconds to drop at acquisition start before saving

acquisition_date = datetime.now().strftime('%m/%d/%y')
acquisition_start_time = datetime.now().strftime('%H:%M:%S')

if len(sys.argv[0]) == 0:
    my_filename = downloads_path + '\\' + 'test_' + datetime.now().strftime('%m%d%y_%H%M%S')  # with full path if target folder different from current folder (do not leave trailing /)
else:
    my_filename = sys.argv[0]


# Initialize data placeholders
buffer_in = np.zeros((chans_in, buffer_in_size))
data = np.zeros((chans_in, 1))  # will contain a first column with zeros but that's fine


# Definitions of basic functions
def ask_user():
    global running
    input("Press ENTER/RETURN or close window to stop acquisition.")
    running = False


def cfg_read_task():  # uses above parameters
    task = nidaqmx.Task() # MANUALLY ADD CHANNELS, FOR GIVEN NUMBER OF AVAILABLE CHANNELS

    # MAKE SURE THE WIRE CONFIGURATION IS CORRECT!!
    # Formula goes:
    # task.ai_channels.add_ai_rtd_chan("Module/Channel", 
    #   current_excit_source=constants.ExcitationSource.INTERNAL, 
    #   resistance_config=constants.ResistanceConfiguration.<THREE_WIRE or FOUR_WIRE>)
    task.ai_channels.add_ai_rtd_chan("RTD4_1/ai0", 
        current_excit_source=constants.ExcitationSource.INTERNAL, 
        current_excit_val=0.001, 
        resistance_config=constants.ResistanceConfiguration.THREE_WIRE)
    # task.ai_channels.add_ai_rtd_chan("RTD4_1/ai1", 
    #     current_excit_source=constants.ExcitationSource.INTERNAL, 
    #     current_excit_val=0.001, 
    #     resistance_config=constants.ResistanceConfiguration.THREE_WIRE)
    # task.ai_channels.add_ai_rtd_chan("RTD4_1/ai2", 
    #     current_excit_source=constants.ExcitationSource.INTERNAL, 
    #     current_excit_val=0.001, 
    #     resistance_config=constants.ResistanceConfiguration.THREE_WIRE)
    # task.ai_channels.add_ai_rtd_chan("RTD4_1/ai3", 
    #     current_excit_source=constants.ExcitationSource.INTERNAL, 
    #     current_excit_val=0.001, 
    #     resistance_config=constants.ResistanceConfiguration.THREE_WIRE)
    
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
task.start() # start the task


# Plot a visual feedback
f, ax1 = plt.subplots(1, 1, sharex='all', sharey='none')
while running and plt.get_fignums(): 
    ax1.clear()
    ax1.plot(data[:, -sampling_freq_in * 10:].T)
    # Label and axis formatting
    ax1.set_xlabel('time [s]')
    ax1.set_ylabel('Temperature [C]')
    xticks = np.arange(0, data[0, -sampling_freq_in * 10:].size, sampling_freq_in)
    xticklabels = np.arange(0, xticks.size, 1)
    ax1.set_xticks(xticks)
    ax1.set_xticklabels(xticklabels)

    plt.pause(1/refresh_rate_plot)  # required for dynamic plot to work (if too low, nulling performance bad)


# Close task to clear connection once done
task.close()
duration = datetime.now() - time_start

#%%
# Final save data and metadata ... first in python reloadable format:
filename = my_filename
with open(filename, 'wb') as f:
    pickle.dump(data, f)
'''
Load this variable back with:
with open(name, 'rb') as f:
    data_reloaded = pickle.load(f)
'''
# Human-readable text file:
extension = '.csv'

timevector = np.arange(0,data.shape[0],sampling_freq_in)

# printdata = np.vstack((timevector, data))
np.set_printoptions(threshold=np.inf, linewidth=np.inf)  # turn off summarization, line-wrapping
with open(filename + extension, 'w') as f:
    f.write('Acquisition Date: ' + acquisition_date)
    f.write('Acquisition Start Time: ' + acquisition_start_time)
    f.write('Sampling rate: ' + str(sampling_freq_in) + ' Hz')
    f.write('Number of RTD elements: ' + str(chans_in))
    f.write(np.array2string(data.T, precision=4 ,separator=', '))  # improve precision here!
# Now in matlab:
# extension = '.mat'
# scipy.io.savemat(filename + extension, {'data':data})


# Some messages at the end
num_samples_acquired = data[0,:].size
print("\n")

print("Acquisition duration: {}.".format(duration))
print("Acquired samples: {}.".format(num_samples_acquired - 1))


# Final plot of whole time course the acquisition
plt.close('all')
plt.ion()
f_tot, ax1 = plt.subplots(1, 1, sharex='all', sharey='none')
ax1.plot(data[:, 2:].T)  # note the exclusion of the first 2 iterations (automatically zoomed in plot)
# Label formatting ...
ax1.set_ylabel('Temperature [C]')
ax1.set_xlabel('Time [s]')
xticks = np.arange(0, data[0, :].size, sampling_freq_in)
xticklabels = np.arange(0, xticks.size, 1)
ax1.set_xticks(xticks)
ax1.set_xticklabels(xticklabels)

plt.savefig(filename, format='png')