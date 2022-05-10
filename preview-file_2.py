import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
from math import floor, ceil
import pickle

root = tk.Tk()
root.withdraw()
filepath = filedialog.askopenfilename(filetypes=[('CSV','*.csv')])
root.destroy()

data = pd.read_csv(filepath, header=0, index_col=0, usecols=[i for i in range(11)], names=['t','A2','A5','A6','B3','B4','C2','C3','C5','D1','D6'])
data = data.rolling(60).mean().dropna()
mean_data = data.mean(axis=1)
std_data = data.std(axis=1)
max_data = data.max(axis=1)
min_data = data.min(axis=1)


data.set_index(data.index/3600, inplace=True)
plt.ion()
fig, ax = plt.subplots(1,1)
ax.axhline(37, linestyle='-', color='black', lw=1, label='_nolegend_')
ax.fill_between(data.index, 36.5*(np.ones((1, len(data.index))).squeeze()), 37.5*(np.ones((1, len(data.index))).squeeze()),
                color='green', alpha=0.1, label='_nolegend_')
ax.axhline(36.5, color='green', lw=1, label='_nolegend_')
ax.axhline(37.5, color='green', lw=1, label='_nolegend_')
# ax.fill_between(data.index/60, 0*(np.ones((1, len(data.index))).squeeze()), 36.5*(np.ones((1, len(data.index))).squeeze()),
#                 color='red', alpha=0.1, label='_nolegend_')
# ax.fill_between(data.index/60, 37.5*(np.ones((1, len(data.index))).squeeze()), 50*(np.ones((1, len(data.index))).squeeze()),
#                 color='red', alpha=0.1, label='_nolegend_')
ax.plot(data.index, mean_data, lw=2, color='blue')
ax.fill_between(data.index, mean_data-std_data, mean_data+std_data, color='blue', alpha=0.25)
ax.plot(data.index, min_data, color='black', linestyle='--', lw=1, label='_nolegend_')
ax.plot(data.index, max_data, color='black', linestyle='--', lw=1, label='_nolegend_')
ax.set_ylim([min([35, ceil(min_data.min()-1)]), max([39, floor(max_data.max() + 1)])])
ax.set_xlim([0, max(data.index)])
plt.legend(['mean','standard deviation','maximum/minimum'])
plt.show()

with open(filepath[:-4]+'.pickle', 'wb') as f:
    pickle.dump(fig, f)
