# Stim plate w/ and w/out cooling plate analysis
import pandas as pd
import matplotlib.pyplot as plt

plt.ion()

folder = 'C:/Users/15189/Desktop/MA 2.1.5 Board Thermal Testing/11_09_21 Testing/'
folder2 = 'C:/Users/15189/Desktop/MA 2.1.5 Board Thermal Testing/11_15_21 Testing/'
folder3 = 'C:/Users/15189/Desktop/MA 2.1.5 Board Thermal Testing/11_18_21 Testing/'

file_stim = 'Stim_6Hz_1800s.csv'
file_coolingplate = 'Stim_6Hz_90min_coolingplate.csv'
file_ionoptix = 'Stim_Ionoptix_90min.csv'
file_ionoptix_CM = 'Ionoptix_Steady_State_4V_4Hz_2ms_total.csv'
file_ionoptix_CM2 = 'Ionoptix_Steady_State_4V_6Hz_6.4ms.csv'

df = pd.read_csv(folder + file_stim, sep=',', index_col=0, usecols=[0, 1, 3, 4])
df_cp = pd.read_csv(folder + file_coolingplate, sep=',', index_col=0, usecols=[0, 1, 3, 4])
df_ion = pd.read_csv(folder2 + file_ionoptix, sep=',', index_col=0, usecols=[0, 1, 3, 4])
df_ion_cm = pd.read_csv(folder3 + file_ionoptix_CM, sep=',', index_col=0, usecols=[0, 1, 3, 4])
df_ion_cm2 = pd.read_csv(folder3 + file_ionoptix_CM2, sep=',', index_col=0, usecols=[0, 1, 3, 4])

t_starts = [ 0, 645, 1290, 2080, 2730, 3430, 4090, 4800, 5670]
t_ends =   [50, 660, 1310, 2100, 2760, 3450, 4110, 4830, 5700]

t_starts_cp = [ 0, 450, 870, 1570, 2155, 2770, 3370, 4020, 4655, 5275]
t_ends_cp =   [50, 470, 880, 1590, 2170, 2790, 3385, 4040, 4670, 5290]

t_starts_ion = [ 0, 520, 900, 1530, 2200, 2820, 3470, 4160, 4970, 5480]
t_ends_ion =   [50, 570, 940, 1580, 2230, 2860, 3500, 4200, 5000, 5520]

t_starts_ion_cm = [ 0, 360, 700, 1370, 2002, 2640, 3440, 4380, 6180]
t_ends_ion_cm =   [40, 390, 730, 1400, 2030, 2650, 3460, 4400, 6200]

t_starts_ion_cm2 = [ 0, 362, 680, 1272, 1910, 2515, 3060, 3692, 4193, 4805, 5440, 6105, 6685]
t_ends_ion_cm2 =   [60, 375, 690, 1282, 1920, 2525, 3070, 3702, 4203, 4815, 5450, 6115, 6595]

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

df_ion_cm_selected = pd.DataFrame(df_ion_cm[(df_ion_cm.index>t_starts_ion_cm[0])   & (df_ion_cm.index<t_ends_ion_cm[0])].mean()).transpose()
for ii in range(1,len(t_starts_ion_cm)):
    df_ion_cm_selected = df_ion_cm_selected.append(pd.DataFrame(df_ion_cm[(df_ion_cm.index>t_starts_ion_cm[ii]) & (df_ion_cm.index<t_ends_ion_cm[ii])].mean()).transpose(), ignore_index=True)
df_ion_cm_selected.set_index(pd.Series(t_starts_ion_cm)/60, inplace=True)

df_ion_cm2_selected = pd.DataFrame(df_ion_cm2[(df_ion_cm2.index>t_starts_ion_cm2[0])   & (df_ion_cm2.index<t_ends_ion_cm2[0])].mean()).transpose()
for ii in range(1,len(t_starts_ion_cm2)):
    df_ion_cm2_selected = df_ion_cm2_selected.append(pd.DataFrame(df_ion_cm2[(df_ion_cm2.index>t_starts_ion_cm2[ii]) & (df_ion_cm2.index<t_ends_ion_cm2[ii])].mean()).transpose(), ignore_index=True)
df_ion_cm2_selected.set_index(pd.Series(t_starts_ion_cm2)/60, inplace=True)

fig, ax1 = plt.subplots(1,5, sharey=True, sharex=True)
df_selected.plot(        ax=ax1[0], markersize=10, marker='o',               ylabel='Temperature [C]', title='2.1.5 STIMULATOR WITHOUT COOLING PLATE\n50mA / 6Hz / 20ms',    grid=True)
df_cp_selected.plot(     ax=ax1[1], markersize=10, marker='o', legend=False, ylabel='Temperature [C]', title='2.1.5 STIMULATOR WITH COOLING PLATE\n50mA / 6Hz / 20ms',       grid=True)
df_ion_selected.plot(    ax=ax1[2], markersize=10, marker='o', legend=False, ylabel='Temperature [C]', title='IONOPTIX C-PACE EM STIMULATOR\n10V / 6Hz / 6.4ms',             grid=True)
df_ion_cm_selected.plot( ax=ax1[3], markersize=10, marker='o', legend=False, ylabel='Temperature [C]', title='IONOPTIX C-PACE EM STIMULATOR\n4V / 4Hz / 2ms',                grid=True)
df_ion_cm2_selected.plot(ax=ax1[4], markersize=10, marker='o', legend=False, ylabel='Temperature [C]', title='IONOPTIX C-PACE EM STIMULATOR\n4V / 6Hz / 6.4ms',             grid=True)

# plt.suptitle('STIM - 6 Hz, 50 mA, 20 ms', fontsize=16)
fig.supxlabel('Time [min]')


fig, ax2 = plt.subplots(1,3, sharey=True, sharex=True)

for ii in range(3):
    ax2[ii].plot(df_selected.iloc[:,ii], markersize=8, marker='o', color='red')
    ax2[ii].plot(df_cp_selected.iloc[:,ii], markersize=8, marker='o', color='blue')
    ax2[ii].plot(df_ion_selected.iloc[:,ii], markersize=8, marker='o', color='green')
    ax2[ii].plot(df_ion_cm_selected.iloc[:,ii], markersize=8, marker='o', color='black')
    ax2[ii].plot(df_ion_cm2_selected.iloc[:,ii], markersize=8, marker='o')
    ax2[ii].grid(True)
    ax2[ii].set_title(list(df_selected.columns.values)[ii])

l = ax2[2].legend([ '2.1.5 Stimulator - without cooling plate', 
                '2.1.5 Stimulator - with cooling plate', 
                'Ionoptix EM Stimulator - 10 V, 6 Hz, 6.4 ms', 
                'Ionoptix EM Stimulator - 4 V, 4 Hz, 2 ms',
                'Ionoptix EM Stimulator - 4 V, 6 Hz, 6.4 ms',
                # 'Ionoptix EM Stimulator - 10 V, 1 Hz, 10 ms',
                # 'Ionoptix EM Stimulator - 4 V, 1 Hz, 10 ms',
                # 'Ionoptix EM Stimulator - 10 V, 4 Hz, 2 ms',
                ])

ax2[0].grid(True)
ax2[0].set_ylabel('Temperature [C]', fontsize=14)
fig.supxlabel('Time [min]', fontsize=14)
fig.suptitle('Heating from STIM', fontsize=16)