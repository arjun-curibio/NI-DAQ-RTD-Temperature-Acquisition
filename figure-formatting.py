import pickle
import matplotlib.pyplot as plt
import pandas as pd
from tkinter import Tk, filedialog

root = Tk()
root.withdraw()
filepath = filedialog.askopenfilename(filetypes=[('pickle file','*.pickle')])
root.destroy()


with open(filepath, 'rb') as f:
    fig = pickle.load(f)

fig.set_size_inches(7.5,5.5)
# fig.axes[0].set_frame_on(False)
plt.grid(True)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
fig.suptitle('Incubator Baseline', fontsize=18)
fig.axes[0].set_xlabel('Time (Hours)', fontsize=16)
fig.axes[0].set_ylabel('Temperature (C)', fontsize=16)
fig.axes[0].set_xlim([0, 12])

fig.show()
plt.savefig(fig, 'COOLING PLATE OFF_Power only.png')

