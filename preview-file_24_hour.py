import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
from math import floor, ceil
import pickle
import datetime

normalized = True
# rolling_window = 5 # [seconds]

root = tk.Tk()
root.withdraw()
filepaths = filedialog.askopenfilenames(filetypes=[('CSV','*.csv')])
root.destroy()


removing_indices = ['B4','A5','A6']
removing_indices = ['A6', 'A1','C4']
fnames = [i.split('/')[-1] for i in filepaths]
indices = [i[24:-4] for i in fnames]

new_indices = []
for i in indices:
    if i == '':
        new_indices.append(0)
    else:
        new_indices.append(int(i) + 1)

idx = sorted(range(len(new_indices)), key=lambda k: new_indices[k])

filepaths = [filepaths[i] for i in idx]
fnames = [fnames[i] for i in idx]

info_files = [file[:-4]+'_info.txt' for file in filepaths]

t_analysis = []
t_files = []
for ifile in info_files:
    with open(ifile,'r') as f:
        for i, line in enumerate(f):
            if i==0:
                date = line[-9:-1]
            if i == 1:
                t_files.append(datetime.datetime.strptime(date+'_'+line[-9:-1], "%m/%d/%y_%H:%M:%S"))
            if i == 16:
                t_analysis.append(int(line))

t_start = t_files[0]
tfiles = []
for ii in range(len(t_files)):
    tfiles.append((t_files[ii]-t_start).total_seconds())



# mean_data = []
def extract_data(filepaths, k, t_analysis, mean_data=[], FIRST=False):
    data = pd.read_csv(filepaths[k], index_col=False)
    data.set_index('t', inplace=True)
    # data = data.rolling(rolling_window).mean().dropna()
    # data.plot()
    # removing_indices = ['D5','A6','C3']
    for ii in removing_indices:
        data.pop(ii)
    points = np.all(np.vstack((data.index >= (t_analysis[k]+0), data.index <= (t_analysis[k]+10))), axis=0)
    print(k)
    print(data.index[points])
    # print(points)
    if FIRST:
        mean_data = pd.DataFrame(data.loc[data.index[points], :].mean()).transpose()
    else:
        mean_data = pd.concat((mean_data, pd.DataFrame(data.loc[data.index[points], :].mean()).transpose()))
    
    k=k+1
    return mean_data, k
    
k = 0
mean_data, k = extract_data(filepaths, k, t_analysis, FIRST=True)

for file in filepaths[1:]:
    mean_data, k = extract_data(filepaths, k, t_analysis, mean_data, False)
    # data.plot()
    # k += 1

mean_data.index = [i/3600 for i in tfiles[:]]

# end_data = pd.read_csv(filepaths[k], index_col=False)
# end_data.set_index('t', inplace=True)
# # data = data.rolling(rolling_window).mean().dropna()
# # removing_indices = ['A5','A6']
# # removing_indices = ['D5','A6','C3']
# for ii in removing_indices:
#     end_data.pop(ii)

# # drop_data_clusters = [100, 135, 205, 270, 382, 1120, 1346, 1363, 1491, 1500, 1849, 3517, 190, 95, 118, 1068, 1113, 1130, 1517, 1760, 1668]
# # drop_data_clusters = [70,134,272, 176,235,434,765, 797,808,918,1485,1724,3281,3311,3324,2285,2052]
# drop_data_clusters = []
# drop_data_clusters.sort(reverse=True)
# for ii in drop_data_clusters:
#     indices = np.all(np.vstack((end_data.index >= (ii-5), end_data.index <= (ii+5))), axis=0)
#     end_data.drop(end_data.index[indices], inplace=True)
# end_data.drop(end_data.index[end_data.index >= max(drop_data_clusters)], inplace=True)
# # end_data.plot()
# end_data.index = [i+tfiles[-1] for i in end_data.index]
if normalized==True:
    # mean_data = mean_data - end_data.iloc[-200,:].mean(axis=0)
    mean_data = mean_data - mean_data.iloc[0,:]
    # end_data = end_data - end_data.iloc[-200:,:].mean(axis=0)
    center = 0

# mean_data = mean_data.drop(0)
plt.axhline(0.5, 0, tfiles[-1]/3600, color='red', label='_nolegend_')
plt.errorbar([i/3600 for i in tfiles[:]], mean_data['A2'], mean_data.std(axis=1), capsize=6, fmt='o-', linewidth=2, markersize=8, color='blue')
# plt.fill_between([i/3600 for i in end_data.index], end_data.mean(axis=1) - end_data.std(axis=1), end_data.mean(axis=1) + end_data.std(axis=1), color='blue', alpha=0.25)
# plt.plot([i/3600 for i in end_data.index], end_data.mean(axis=1), color='blue', linewidth=2)
# plt.plot([i/3600 for i in end_data.index], end_data.mean(axis=1) - end_data.std(axis=1), color='blue', linewidth=1)
# plt.plot([i/3600 for i in end_data.index], end_data.mean(axis=1) + end_data.std(axis=1), color='blue', linewidth=1)
plt.xlabel('Time (hours)', fontsize=16)
plt.ylabel('Temperature difference (degrees C)', fontsize=16)
plt.title('Long Term Stim\n5 Hz, 10 ms, 50 mA\n07-16-22', fontsize=16)


# end_data.mean(axis=1).plot()
# (end_data.mean(axis=1) - end_data.std(axis=1)).plot()
# (end_data.mean(axis=1) + end_data.std(axis=1)).plot()
