import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
folder = 'C:/Users/15189/Desktop/MA 2.1.5 Board Thermal Testing/11_09_21 Testing/'
WELL_POSITIONS = ['B1', 'C3', 'B4', 'C6']

# magnetometer and board only
file = 'Mag_90s.csv'
df = pd.read_csv(folder + file, sep=',', index_col=0)
base = df[df.index<30].mean()
df = df - base + 37

df.drop(range(540, df.shape[0]), inplace=True) # remove garbage data
df.set_index(pd.Series(df.index/60), inplace=True)

fig, ax1 = plt.subplots(nrows=1, ncols=4, sharey=True)
df.plot(subplots=True, ax=ax1, sharey=True, linewidth=3, color='red', legend=False, grid=True)

file = 'Board_540s.csv'
df = pd.read_csv(folder + file, sep=',', index_col=0)
base = df[df.index<30].mean()
df = df - base + 37

df.drop(range(540, df.shape[0]), inplace=True) # remove garbage data
df.set_index(pd.Series(df.index/60), inplace=True) 
df.plot(subplots=True, ax=ax1, sharey=True, color='blue', linewidth=3, legend=False, grid=True)

ax1[2].legend(['Magnetometers On', 'Magnetometers Off'])

for ii in range(4):
    ax1[ii].set_title('Well ' + WELL_POSITIONS[ii])
    ax1[ii].plot([50/60, 50/60], [36.5, 38], linewidth=1, linestyle='--', color='black')
    
ax1[0].set_ylim([36.95, 37.5])
fig.supxlabel('Time [m]')
fig.suptitle('Heating from Magnetometers/2.1.5 Board')
fig.supylabel('Temperature [C]')



##  5 minutes stim
file = 'Stim_6Hz_300s.csv'

df = pd.read_csv(folder + file, sep=',', index_col=0)
# base = df[df.index<100].mean()
# df = df - base + 37
base = df[df.index<100].mean()
t0 = df[df.index>480].mean()

print('Temperature change after 5 minutes stim (20 ms, 50 mA, 6 Hz):')
for ii in range(4):
    print(WELL_POSITIONS[ii] + ': ' + str(round((t0-base)[ii],2)) + ' C')

df.set_index(pd.Series(df.index/60), inplace=True)
plt.ion()
df.plot(xlabel='Time [m]', ylabel='Temperature [C]', grid=True, ylim=[37.0, 38.5],
        title='STIM: 20 ms, 50 mA, 6 Hz')
plt.savefig(folder + 'Stim_5-minutes_6Hz.png', format='png')
# %%



### long stim

file = 'Stim_6Hz_1800s.csv'
df = pd.read_csv(folder + file, sep=',', index_col=0)


df_selected = pd.DataFrame(df[(df.index>0)   & (df.index<60)].mean()).transpose()
df_selected = df_selected.append(pd.DataFrame(df[(df.index>645) & (df.index<661)].mean()).transpose(), ignore_index=True)
df_selected = df_selected.append(pd.DataFrame(df[(df.index>1280) & (df.index<1315)].mean()).transpose(), ignore_index=True)
df_selected = df_selected.append(pd.DataFrame(df[(df.index>2070) & (df.index<2120)].mean()).transpose(), ignore_index=True)
df_selected = df_selected.append(pd.DataFrame(df[(df.index>2730) & (df.index<2780)].mean()).transpose(), ignore_index=True)
df_selected = df_selected.append(pd.DataFrame(df[(df.index>3420) & (df.index<3450)].mean()).transpose(), ignore_index=True)
df_selected = df_selected.append(pd.DataFrame(df[(df.index>4080) & (df.index<4110)].mean()).transpose(), ignore_index=True)
df_selected = df_selected.append(pd.DataFrame(df[(df.index>4790) & (df.index<4830)].mean()).transpose(), ignore_index=True)
df_selected = df_selected.append(pd.DataFrame(df[(df.index>5680) & (df.index<5700)].mean()).transpose(), ignore_index=True)
df_selected.set_index(pd.Series([0, 675, 1280, 2070, 2730, 3420, 4080, 4790, 5680]), inplace=True)
base = df_selected[df_selected.index<30].mean()
df_selected = df_selected - base + 37
df_selected.set_index(pd.Series(df_selected.index/60), inplace=True)
df_selected.plot(xlabel='Time [m]', ylabel='Temperature [C]', title='STIM - 20 ms, 50 mA, 6 Hz - 90 minutes', markersize=10, marker='o', grid=True)

