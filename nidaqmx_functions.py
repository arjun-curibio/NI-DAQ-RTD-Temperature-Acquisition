import numpy as np
from math import floor, ceil

import nidaqmx
from nidaqmx import constants, errors
# from nidaqmx import stream_readers  # not needed in this script
# from nidaqmx import stream_writers  # not needed in this script
from nidaqmx.system.storage.persisted_task import PersistedTask
from datetime import datetime
from time import time
from os.path import exists

import pandas as pd
from pyrsistent import b

import os
def cfg_read_task(taskName, sampling_freq_in = 1, buffer_in_size_cfg = 1, ADCTimingMode = constants.ADCTimingMode.HIGH_SPEED, ResistanceConfiguration = constants.ResistanceConfiguration.FOUR_WIRE, dontInclude = []): 
    # Read persisted task from NI MAX, open, configure, and 
    
    global task
    # task = nidaqmx.Task()
    task = PersistedTask(taskName).load()
    # except errors.DaqError:
    #     print("DaqError")
    # except:
    #     print(type(Exception).__name__)
        
    chans = list(task.ai_channels)
    task.timing.cfg_samp_clk_timing(rate=sampling_freq_in, sample_mode=constants.AcquisitionType.CONTINUOUS,
      samps_per_chan=buffer_in_size_cfg)
    
    CHANNEL_ADDRESSES = [chan.physical_channel.name for chan in chans]
    CHANNEL_NAMES = [chan.name for chan in chans]
    
    print(dontInclude)
    for chan in chans:
        if chan.name not in dontInclude:
            print("{}: {}".format(chan.physical_channel.name,chan.name))
        chan.ai_adc_timing_mode = ADCTimingMode
        chan.ai_resistance_cfg = ResistanceConfiguration
    

        
    TOTAL_CHANNELS = len(CHANNEL_NAMES)
    Include_idx = list(range(TOTAL_CHANNELS))

    dontInclude.sort(reverse=True)

    for well in dontInclude:
        if well in CHANNEL_NAMES:
            idx = CHANNEL_NAMES.index(well)
            Include_idx.remove(idx)

    for well in dontInclude:
        if well in CHANNEL_NAMES:
            idx = CHANNEL_NAMES.index(well)
            CHANNEL_NAMES.remove(well)
            CHANNEL_ADDRESSES.remove(CHANNEL_ADDRESSES[idx])

    return task, CHANNEL_ADDRESSES, CHANNEL_NAMES, TOTAL_CHANNELS, Include_idx
def fullFileName(folder = '', fname = 'monitor', CHANNEL_ADDRESSES = [], CHANNEL_NAMES = [], sampling_freq_in = 1):
    if not os.path.exists(os.getcwd()+'/recordings/'+folder):
        os.mkdir("{}/recordings/{}".format(os.getcwd(),folder))
    folder = "{}/recordings/{}".format(os.getcwd(),folder)
    
    if fname == 'test': rewriteFlag = True
    else:               rewriteFlag = False
    
    my_filename = "{}/{}".format(folder, fname)
    finalFileName = my_filename
    if rewriteFlag == False:
        ii=0
        while exists(finalFileName + '.csv'):
            finalFileName = my_filename + str(ii)
            ii += 1

    if fname == 'monitor':
        pass
    else:
        with open(finalFileName + '.csv', 'w') as f:
            f.write('t,'+','.join(CHANNEL_NAMES) + '\n')

    t0 = datetime.now()
    acquisition_date = t0.strftime('%m/%d/%y')
    acquisition_start_time = t0.strftime('%H:%M:%S')

    if fname != 'monitor':
        with open(finalFileName + '_info.txt', 'w') as f:
            f.write('Acquisition Date: ' + acquisition_date + '\n')
            f.write('Acquisition Start Time: ' + acquisition_start_time+ '\n')
            f.write('Sampling rate: ' + str(sampling_freq_in) + ' Hz'+ '\n')
            f.write('Number of RTD elements: ' + str(len(CHANNEL_NAMES))+ '\n')
            f.write('\n')
            f.write('Channel Mapping:\n')
            [f.write("Channel {} --> Well {}\n".format(CHANNEL_ADDRESSES[i], CHANNEL_NAMES[i])) for i in range(len(CHANNEL_NAMES))]
            f.write('\n')

    print(finalFileName)

    return finalFileName, rewriteFlag
def cfg_devices():
    devices = nidaqmx.system.System.local().devices
    # print(list(devices))
    for i in devices:
        i.ai_min_rate = 1
        # print(i.ai_physical_chans)
        for j in i.ai_physical_chans:
            # print(j.name)
            j.ai_adc_timing_mode = constants.ADCTimingMode.HIGH_SPEED
    return devices
def ask_user():
    global running
    input("Close window to stop acquisition.")
    running = False
def updatePlot(fig, ax, t, data, CHANNEL_NAMES, **kwargs):
    plotter_grid_size = 5
    ylims = [35, 39]
    PLOTTER_WINDOW = 30
    for key, value in kwargs.items():
        # print(value)
        if key == 'ylims':
            ylims = value
        if key == 'plotter_grid_size':
            plotter_grid_size = value
        if key == 'window':
            PLOTTER_WINDOW = value
        pass
    ax.clear()
    pgs = plotter_grid_size
    # print("\033[F{}: {}, {}".format(data.shape, round(t[-1], 2), data[:,-1].round(2))

    # print("{}, {}".format(len(t), data.shape[1]))
    ax.plot(t.T, data.T)
    # print(t)
    # print(data.T)
    # ax.set_ylim(ylims)
    ax.legend(CHANNEL_NAMES, loc='upper left', ncol=2)
    # Label and axis formatting
    # ax1.set_xlabel('time [s]')
    ax.set_ylabel('Temperature [C]')

    ax.set_xlim([t[0]-1, max([t[-1],PLOTTER_WINDOW ])])
    xlim1 = ax.get_xlim()
    xticks = np.arange( start = floor(xlim1[0]/pgs)*pgs,
                        stop = max([ceil(xlim1[1]/pgs)*pgs, PLOTTER_WINDOW+(pgs*0.5)]),
                        step = pgs)
    # print("[{},{}], {}, {}, {}".format(t[0], t[-1], xlim1, xticks, ceil(t[-1]/pgs)*pgs))
    ax.set_xticks(xticks)
    ax.set_xlim([t[0], max([t[-1],PLOTTER_WINDOW ])])
        
        
    return ax



