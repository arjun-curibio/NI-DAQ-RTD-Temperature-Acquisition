import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
from math import floor, ceil
import pickle

normalized = True
rolling_window = 30 # [seconds]


root = tk.Tk()
root.withdraw()
filepath = filedialog.askopenfilename(filetypes=[('CSV','*.csv')])
root.destroy()

data = pd.read_csv(filepath, index_col=False)
data.set_index('t', inplace=True)
# removing_indices = ['D5','A6','B3','C3']
# removing_indices = ['D6','C4', 'C3', 'A6','D5', 'B3']
removing_indices = []
for ii in removing_indices:
    data.pop(ii)
data.plot()

if normalized==True:
    data = data - data.iloc[0,:]
    center = 0
else:
    center = 37

if data.index[-1] < 120:
    data.set_index(data.index, inplace=True)
    label='seconds'
elif data.index[-1] < 20000:
    data.set_index(data.index/60, inplace=True)
    label='minutes'
else:
    data.set_index(data.index/3600, inplace=True)
    label='hours'

data = data.rolling(rolling_window).mean().dropna()
mean_data = data.mean(axis=1)
std_data = data.std(axis=1)
max_data = data.max(axis=1)
min_data = data.min(axis=1)


plt.ion()
fig, ax = plt.subplots(1,1)
ax.axhline(center, linestyle='-', color='black', lw=0.5, label='_nolegend_')
ax.fill_between(data.index, (center-0.5)*(np.ones((1, len(data.index))).squeeze()), (center+0.5)*(np.ones((1, len(data.index))).squeeze()),color='green', alpha=0.1, label='_nolegend_')
ax.axhline(36.5, color='green', lw=1, label='_nolegend_')
ax.axhline(37.5, color='green', lw=1, label='_nolegend_')
# ax.fill_between(data.index/60, 0*(np.ones((1, len(data.index))).squeeze()), 36.5*(np.ones((1, len(data.index))).squeeze()),color='red', alpha=0.1, label='_nolegend_')
# ax.fill_between(data.index/60, 37.5*(np.ones((1, len(data.index))).squeeze()), 50*(np.ones((1, len(data.index))).squeeze()),color='red', alpha=0.1, label='_nolegend_')
ax.plot(data.index, mean_data, lw=2, color='blue')
ax.fill_between(data.index, mean_data-std_data, mean_data+std_data, color='blue', alpha=0.25)
ax.plot(data.index, min_data, color='black', linestyle='--', lw=1)
ax.plot(data.index, max_data, color='black', linestyle='--', lw=1, label='_nolegend_')
ax.set_ylim([min([center-1, ceil(min_data.min()-1)]), max([center+1, floor(max_data.max() + 1)])])
ax.set_xlim([0, max(data.index)])
plt.legend(['mean (n = '+str(data.shape[1])+')','standard deviation','maximum/minimum'], loc='lower center')
plt.xlabel('Time ('+label+')')
plt.ylabel('Temperature (C)')

plt.show()

with open(filepath[:-4]+'.pickle', 'wb') as f:
    pickle.dump([fig, label, data, center], f)
