import pickle
import matplotlib.pyplot as plt
import pandas as pd
from tkinter import Tk, filedialog

root = Tk()
root.withdraw()
filepath = filedialog.askopenfilename(filetypes=[('pickle file','*.pickle')])
root.destroy()

supname = 'Thermal Management'
name = 'Magnetometer Recording with Stim'
labels = {
    65: 'Mag\nON',
    665: 'Mag\nOFF',
    
}
labels = {85: 'Mag\nON',
          400: 'Mag\nOFF',
          115: 'Stim\nON',
          145: 'Stim\nOFF',
          185: 'Stim\nON',
          215: 'Stim\nOFF',
          245: 'Stim\nON',
          285: 'Stim\nOFF',
          315: 'Stim\nON',
          345: 'Stim\nOFF',
          
          # 1300: '3' #'Board\nOFF'
         }

with open(filepath, 'rb') as f:
    fig, label, data, center = pickle.load(f)

if center == 0:
    plt.ylabel('Temperature Difference, from Baseline (C)', fontsize=14)
elif center == 37:
    plt.ylabel('Absolute Temperature (C)', fontsize=14)


fig.set_size_inches(7.5, 5.5)
ax = plt.gca()
ax.set_title(name, fontsize=16)
# fig.axes[0].set_frame_on(False)
plt.grid(True)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.xlabel('Time ('+label+')', fontsize=14)
fig.suptitle(supname, fontsize=18)
# fig.axes[0].set_xlabel('Time (Hours)', fontsize=16)
# fig.axes[0].set_ylabel('Temperature (C)', fontsize=16)
# fig.axes[0].set_xlim([0, 80])
if label == 'seconds':
    divisor = 1
elif label == 'minutes':
    divisor = 60
elif label == 'hours':
    divisor = 3600
else:
    divisor = 60
for ii in list(labels.keys()):
    if 'Stim' in labels[ii]:
        plt.axvline(ii/divisor, 0.1, 0.9, label='_nolegend_', color='orange')
        plt.text(ii/divisor, (plt.ylim()[1]-plt.ylim()[0])*0.9+plt.ylim()[0], labels[ii],  fontsize=12, ha='center', va='bottom', color='black')

    elif 'Mag' in labels[ii]:
        plt.axvline(ii/divisor, 0.1, 0.9, label='_nolegend_', color='red')
        plt.text(ii/divisor, (plt.ylim()[1]-plt.ylim()[0])*0.9+plt.ylim()[0], labels[ii],  fontsize=14, ha='center', va='bottom', color='black')

fig.show()

plt.savefig('recordings/'+name+'.png', format='png')


