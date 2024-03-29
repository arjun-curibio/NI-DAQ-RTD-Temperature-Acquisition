import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
from math import floor, ceil
import pickle

normalized = True
rolling_window = 1 # [seconds]

root = tk.Tk()
root.withdraw()
filepath = filedialog.askopenfilename(filetypes=[('CSV','*.csv')])
root.destroy()

data = pd.read_csv(filepath, index_col=False)
data = pd.read_csv(filepath, index_col=0)
data.set_index('t', inplace=True)
data = data.rolling(rolling_window).mean().dropna()
removing_indices = []
removing_indices = ['A6','A1','A5']
# removing_indices = []
for ii in removing_indices:
    data.pop(ii)

plt.ion()

data.plot()

data_clusters = [ # file #1
    50, 670, 1270, 1850, 2450, 3040, 3620, 4220, 4810, 5400, 5990, 6580, 7170]

data_clusters = [ # file #2
    0, 720, 1090, 2005, 3480, 3840, 4735, 5695, 6845]

data_clusters = [
    0,730, 1225, 1905, 2390, 3120, 3620, 4065, 4655, 5280, 6065, 6920
]

data_clusters = [0,610, 1200, 1800, 2400, 3000, 3600, 4190, 4790, 5390, 5990, 6580, 7170, 7770, 8370, 8960, 9560, 10150, 10750, 11340, ]
data_clusters = [i+202 for i in [0,610, 1200, 1790, 2390, 2990, 3580, 4180, 4770, 5950, 6550] ]
for i in [7340, 7940, 8530, 9120,10310,10910,11500,12100,12700,13290,13880,14480,15670,16270,16870,17460,18050,18650,19240,19840,20435,21030,21550,22000,23000,24000,25000,26000,27000]:
    data_clusters.append(i)
kk=0

ii=data_clusters[0]
indices = np.all(np.vstack((data.index >= (ii+0), data.index <= (ii+10))), axis=0)
thermal_stim = pd.DataFrame(data.loc[data.index[indices], :].mean()).transpose()
# plt.figure(1)
for ii in data_clusters[1:]:
    indices = np.all(np.vstack((data.index >= (ii+0), data.index <= (ii+10))), axis=0)
    thermal_stim = pd.concat((thermal_stim, pd.DataFrame(data.loc[data.index[indices], :].mean()).transpose()))
    # thermal_stim.plot()

thermal_stim.index = data_clusters
data = thermal_stim.copy()
# for ii in np.arange(start_stim, data.shape[0], interval):
#     thermal_stim.append(data.loc[data.index[data.index <= ii]])

# data.plot()
# fig, ax = plt.subplots(1,1)
# for ii in clusters:
#     ii.plot(ax=ax)


# data.drop(axis=0, index=data.index[data.index > 115], inplace=True)

if normalized==True:
    data = data - data.iloc[0,:]
    center = 0
else:
    center = 37

data.plot(marker='o')

if data.index[-1] < 120:
    data.set_index(data.index, inplace=True)
    label='seconds'
elif data.index[-1] < 20000:
    data.set_index(data.index/60, inplace=True)
    label='minutes'
else:
    data.set_index(data.index/3600, inplace=True)
    label='hours'

mean_data = data.mean(axis=1)
std_data = data.std(axis=1)
max_data = data.max(axis=1)
min_data = data.min(axis=1)

plt.ion()
# data.plot()

fig, ax = plt.subplots(1,1)
ax.axhline(center, linestyle='-', color='black', lw=0.5, label='_nolegend_')
ax.fill_between(data.index, (center-0.5)*(np.ones((1, len(data.index))).squeeze()), (center+0.5)*(np.ones((1, len(data.index))).squeeze()),color='green', alpha=0.1, label='_nolegend_')
ax.axhline(36.5, color='green', lw=1, label='_nolegend_')
ax.axhline(37.5, color='green', lw=1, label='_nolegend_')
# ax.fill_between(data.index/60, 0*(np.ones((1, len(data.index))).squeeze()), 36.5*(np.ones((1, len(data.index))).squeeze()),
#                 color='red', alpha=0.1, label='_nolegend_')
# ax.fill_between(data.index/60, 37.5*(np.ones((1, len(data.index))).squeeze()), 50*(np.ones((1, len(data.index))).squeeze()),
#                 color='red', alpha=0.1, label='_nolegend_')
ax.errorbar(data.index, mean_data, std_data, fmt='none', capsize=8)
ax.plot(data.index, mean_data, 'bo', color='blue', linestyle='-')

# ax.fill_between(data.index, mean_data-std_data, mean_data+std_data, color='blue', alpha=0.25)
# ax.plot(data.index, min_data, color='black', linestyle='--', lw=1)
# ax.plot(data.index, max_data, color='black', linestyle='--', lw=1, label='_nolegend_')
ax.set_ylim([min([center-1, ceil(min_data.min()-1)]), max([center+1, floor(max_data.max() + 1)])])
ax.set_xlim([0, max(data.index)])
ax.plot(data.index, data.min(axis=1), color='black', linestyle='--', linewidth=1)
ax.plot(data.index, data.max(axis=1), color='black', linestyle='--', linewidth=1)

plt.legend(['mean (n = '+str(data.shape[1])+')','standard deviation','maximum/minimum'], loc='lower center')
plt.xlabel('Time ('+label+')')
plt.ylabel('Temperature (C)')

plt.show()

with open(filepath[:-4]+'.pickle', 'wb') as f:
    pickle.dump([fig, label, data, center], f)
