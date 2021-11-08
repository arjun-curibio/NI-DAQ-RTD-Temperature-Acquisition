import numpy as np
import nidaqmx as ndm
import matplotlib.pyplot as plt

from nidaqmx.constants import ExcitationSource as ES, ResistanceConfiguration as RC

ptask =  ndm.system.storage.persisted_task.PersistedTask('MyTemperatureTask')
task = ptask.load()
task.start()

plt.ion()
plt.show()
ii=0
while bool(plt.get_fignums()):
    value = task.read()
    print(value)
    
    
    ii+=1
    plt.plot([1,1,1,1],value)

task.stop()
task.close()
