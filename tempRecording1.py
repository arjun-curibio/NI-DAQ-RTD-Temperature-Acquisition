import numpy as np, nidaqmx as ndm, time, threading
from nidaqmx.constants import Edge, AcquisitionType
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from datetime import datetime


# extract task from NI MAX, load in as a task
# # ptask = ndm.system.storage.persisted_task.PersistedTask('MyTemperatureTask')
# # task = ptask.load()
# # task.timing.cfg_samp_clk_timing(0.5, source="", active_edge=Edge.RISING, sample_mode=AcquisitionType.CONTINUOUS)
# # task.start()

# get user-defined filename and open as writeable


def StartRecording(val):
    sRate = 2 # seconds
    ii=0
    t_0 = time.time()


    try:
        while plt.get_fignums():
            # # RTDvalues = task.read()

            now = datetime.now().strftime("%H:%M:%S")
            time.sleep(sRate - (time.time() - t_0))
            print(round(time.time()-t_0, 2), ii)
            t_0 = time.time()
            ii += 1

    except KeyboardInterrupt:
        # # task.stop()   
        pass  

def EndRecording(val, t):
    raise KeyboardInterrupt
    t.join()
    
    
def StartRecordererFunctionBackground(val):
    t = threading.Thread(target=StartRecording, args=(val, ))
    t.start()

    return t


# start task
#task.start()

plt.ion()
plt.figure()
axStartButton = plt.axes([0.1, 0.25, 0.8, 0.1])
axEndButton = plt.axes([0.1, 0.1, 0.8, 0.1])

bStartButton = Button(axStartButton, "Start Recording.")
bStartButton.on_clicked(StartRecordererFunctionBackground)

bEndButton = Button(axEndButton, "End Recording.")
bEndButton.on_clicked(lambda x: EndRecording(x, bEndButton.label.get_text()))