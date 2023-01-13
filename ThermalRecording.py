"""
Temperature Data Acquisition, for NIDAQ.  Data logger for thermal acquisition for Mantarray V1.  
Records data to .csv file, stored locally.
Acquisition information is stored in companion .txt file, stored locally.
If the recording exist normally, a snapshot figure is saved and stored locally.

The following assumes:
    A persistent task called "MyTemperatureTask" has been created in the NiMAX software, and stored locally.

The following must be changed in the file, locally:
    CHANNEL_MAP - well number or label for each channel
    CHANNEL_NAMES - must match the names of the CDAQs and channels in "MyTemperatureTask"
    fname and folder

"""

# setting fname to 'monitor' does not save any data or figures
#               to 'test' does not save figures, saves data, rewrites data in test.csv

# fname = 'monitor'
fname = 'LT stim 24_hours_trial 4' 
fname = 'saving_test'
folder = "test"

sampling_freq_in = 1  # in Hz, limited by hardware and number of channels (may collected duplicate data if to0 high)
taskName = "MyTemperatureTask"
PLOTTER_WINDOW = 10 # seconds
DATA_WINDOW = PLOTTER_WINDOW*sampling_freq_in
plotter_grid_size = 5
savefigFlag = True # save the final plot to a separate figure (RECOMMEND TO SET TO TRUE)
rewriteFlag = False # If you want to re-write file, otherwise append number to filename (RECOMMENDED TO SET TO FALSE)

# dontInclude = [0,1,9,11] 
dontInclude = ['B1','C3'] # do not include these channels (in case some are broken or reading false)
dontInclude = []
buffer_in_size = 1 # number of samples to collect on each channel to store in buffer before sending to computer

# Imports
import matplotlib.pyplot as plt
import numpy as np
from math import floor, ceil

import nidaqmx
from nidaqmx.stream_readers import AnalogMultiChannelReader
from nidaqmx import constants, system
from nidaqmx.system.storage.persisted_task import PersistedTask

# from nidaqmx import stream_readers  # not needed in this script
# from nidaqmx import stream_writers  # not needed in this script

import threading
from datetime import datetime
from time import time
from os.path import exists

import pandas as pd
from pyrsistent import b

import os
from nidaqmx_functions import *
# Parameters
bufsize_callback = buffer_in_size
buffer_in_size_cfg = round(buffer_in_size * 1)  # clock configuration

task, CHANNEL_ADDRESSES, CHANNEL_NAMES, TOTAL_CHANNELS, Include_idx = cfg_read_task(taskName, sampling_freq_in, buffer_in_size_cfg, dontInclude = dontInclude)

finalFileName, rewriteFlag = fullFileName(folder, fname, CHANNEL_ADDRESSES, CHANNEL_NAMES, sampling_freq_in)

chans_in = len(Include_idx)  # set to number of active OPMs
refresh_rate_plot = 10  # in Hz
crop = 0  # number of seconds to drop at acquisition start before saving

i=0

# Initialize data placeholders
buffer_in = np.zeros((TOTAL_CHANNELS, buffer_in_size))
data = np.zeros((chans_in, 0))
t = np.zeros((1,0))
re_index = []

t0 = time()
gotData = False
def reading_task_callback(task_idx, event_type, num_samples, callback_data):  # bufsize_callback is passed to num_samples
    global data
    global buffer_in
    global t
    global task
    global gotData
    global Include_idx
    if running: 
        num_available_channels = len(CHANNEL_NAMES)
        stream_in.read_many_sample(buffer_in, num_samples, timeout=constants.WAIT_INFINITELY)
        data    = np.append(data, buffer_in[Include_idx,:], axis=1)  # appends buffered data to total variable data
        t       = np.append(t,(time()-t0))
        if data.shape[1] >= DATA_WINDOW+1: # CIRCULAR BUFFER
            t = np.delete(t, 0)
            data = np.delete(data, 0, axis=1)

        while t.shape[0] > data.shape[1]:
            t = np.delete(t, 0)
            
        if fname != 'monitor':
            with open(finalFileName + '.csv', 'a') as f:
                string = "{}, ".format(round(t[-1],2))
                for ii in range(data.shape[0]):
                    string += "{}, ".format(data[ii,-1].round(2))
                string += "\n"
                f.write(string)
                
        
    gotData = True
    return 0  # Absolutely needed for this callback to be well defined (see nidaqmx doc).


stream_in = AnalogMultiChannelReader(task.in_stream)
task.register_every_n_samples_acquired_into_buffer_event(bufsize_callback, reading_task_callback)

# Start threading to prompt user to stop
thread_user = threading.Thread(target=ask_user)
thread_user.start()

# Main loop
running = True
task.start()
t0 = time()

# # Plot a visual feedback for the user's mental health
f, ax = plt.subplots(1,1)

print('\n\n')
print("{:>10}|".format('  t (s) '), end='')
for i in range(len(CHANNEL_NAMES)):
    print("{:^7.2}".format(CHANNEL_NAMES[i]), end='')
print('\n')
while running and plt.get_fignums():
    if len(t) > 0:
        if gotData == True: # gotData is set in reading callback
            ax = updatePlot(f, ax, t, data, CHANNEL_NAMES, plotter_grid_size = 5, ylims = [35, 39], window = PLOTTER_WINDOW)
            print("\033[F{:^10.2f}|".format(round(t[-1], 2)), end='')
            for i in range(data.shape[0]):
                print("{:^7.2f}".format(round(data[i,-1],2)), end='')
            print('\r')
            gotData = False # flip low to wait for new data to come in
            
        
    f.suptitle(fname)
    plt.pause(1/refresh_rate_plot)  # required for dynamic plot to work (if too low, nulling performance bad)
    ylims = ax.get_ylim()
        # print(str(round(t[-1]-t[0],2))+'\t'+'\t'.join(list(data[:,-1].round(2).astype(str))))

task.close()

# #%%
# # Final save data and metadata ... first in python reloadable format:
print('\n')
import pandas as pd
if fname != 'monitor':
    # CHANNEL_NAMES = ['C4','A1','D2','B3','B4','A5','D5','A6','D6']
    DATA = pd.read_csv(finalFileName+'.csv', sep=',', header=0, index_col = False, names=['t']+CHANNEL_NAMES)
    DATA.set_index('t', inplace=True)
    DATA.plot()
    plt.legend(loc='upper left')
    plt.xlabel('Time (s)')
    plt.ylabel('Temperature (C)')
    plt.axhline(DATA.iloc[:,0].mean(), linestyle='--', color='r',linewidth=1)
    print(DATA)

    
    if savefigFlag and fname != 'monitor' and fname != 'test':
        plt.savefig(finalFileName + '.png', format='png')
    plt.ion()
    plt.show(block='False')

print("Acquisition duration: {} s".format(time()-t0))
print("Acquired samples: {} samples | Fs = {} Hz".format(DATA.shape[1], sampling_freq_in))
if len(dontInclude) > 0:
    print("Excluding wells: {}".format(",".join(dontInclude)))

print("Close the window and press ENTER in the Terminal to close program.")