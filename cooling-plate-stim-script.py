# Stim plate w/ and w/out cooling plate analysis
import pandas as pd
import matplotlib.pyplot as plt

plt.ion()

fig, ax1 = plt.subplots(1,3, sharey=True, sharex=True)
folder = 'C:/Users/15189/Desktop/MA 2.1.5 Board Thermal Testing/11_09_21 Testing/'
folder2 = 'C:/Users/15189/Desktop/MA 2.1.5 Board Thermal Testing/11_15_21 Testing/'

file_stim = 'Stim_6Hz_1800s.csv'
file_coolingplate = 'Stim_6Hz_90min_coolingplate.csv'
file_ionoptix = 'Stim_Ionoptix_90min.csv'

df = pd.read_csv(folder + file_stim, sep=',', index_col=0, usecols=[0, 1, 3, 4])
df_cp = pd.read_csv(folder + file_coolingplate, sep=',', index_col=0, usecols=[0, 1, 3, 4])
df_ion = pd.read_csv(folder2 + file_ionoptix, sep=',', index_col=0, usecols=[0, 1, 3, 4])

t_starts = [ 0, 645, 1290, 2080, 2730, 3430, 4090, 4800, 5670]
t_ends =   [50, 660, 1310, 2100, 2760, 3450, 4110, 4830, 5700]

t_starts_cp = [ 0, 450, 870, 1570, 2155, 2770, 3370, 4020, 4655, 5275]
t_ends_cp =   [50, 470, 880, 1590, 2170, 2790, 3385, 4040, 4670, 5290]

t_starts_ion = [ 0, 500, 870, 1530, 2180, 2810, 3460, 4160, 4970, 5470]
t_ends_ion =   [50, 570, 940, 1580, 2230, 2870, 3500, 4200, 5000, 5500]

df_selected = pd.DataFrame(df[(df.index>t_starts[0])   & (df.index<t_ends[0])].mean()).transpose()
for ii in range(1,len(t_starts)):
    df_selected = df_selected.append(pd.DataFrame(df[(df.index>t_starts[ii]) & (df.index<t_ends[ii])].mean()).transpose(), ignore_index=True)

df_selected.set_index(pd.Series(t_starts)/60, inplace=True)

df_cp_selected = pd.DataFrame(df_cp[(df_cp.index>t_starts_cp[0])   & (df_cp.index<t_ends_cp[0])].mean()).transpose()
for ii in range(1,len(t_starts_cp)):
    df_cp_selected = df_cp_selected.append(pd.DataFrame(df_cp[(df_cp.index>t_starts_cp[ii]) & (df_cp.index<t_ends_cp[ii])].mean()).transpose(), ignore_index=True)

df_cp_selected.set_index(pd.Series(t_starts_cp)/60, inplace=True)

df_ion_selected = pd.DataFrame(df_ion[(df_ion.index>t_starts_ion[0])   & (df_ion.index<t_ends_ion[0])].mean()).transpose()
for ii in range(1,len(t_starts_ion)):
    df_ion_selected = df_ion_selected.append(pd.DataFrame(df_ion[(df_ion.index>t_starts_ion[ii]) & (df_ion.index<t_ends_ion[ii])].mean()).transpose(), ignore_index=True)

df_ion_selected.set_index(pd.Series(t_starts_ion)/60, inplace=True)

df_selected.plot(    ax=ax1[0], markersize=10, marker='o', ylabel='Temperature [C]', title='WITHOUT COOLING PLATE', grid=True)
df_cp_selected.plot( ax=ax1[1], markersize=10, marker='o', legend=False, ylabel='Temperature [C]', title='WITH COOLING PLATE', grid=True)
df_ion_selected.plot(ax=ax1[2], markersize=10, marker='o', legend=False, ylabel='Temperature [C]', title='WITH COOLING PLATE', grid=True)

plt.suptitle('STIM - 6 Hz, 50 mA, 20 ms', fontsize=16)
fig.supxlabel('Time [min]')
