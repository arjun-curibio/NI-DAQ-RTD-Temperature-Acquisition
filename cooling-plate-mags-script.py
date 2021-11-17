# Board heating with and without cooling plate
import pandas as pd
import matplotlib.pyplot as plt

folder = 'C:/Users/15189/Desktop/MA 2.1.5 Board Thermal Testing/11_09_21 Testing/'
file = 'Mag_1C.csv'
file_cp = 'Mag_10minutes_coolingplate.csv'

plt.ion()
fig, ax1 = plt.subplots(1,2, sharey=True)

df = pd.read_csv(folder + file, index_col=0, usecols=[0, 2, 3, 4])
df.drop(range(860, df.shape[0]), inplace=True)
df.set_index(pd.Series(df.index)/60, inplace=True)

df_cp = pd.read_csv(folder + file_cp, index_col=0)
df_cp.drop(range(860, df_cp.shape[0]), inplace=True)
df_cp.set_index(pd.Series(df_cp.index)/60, inplace=True)


df.plot(ax=ax1[0], ylabel='Temperature [C]', xlabel='Time [min]', title='MAGS', grid=True)
df_cp.plot(ax=ax1[1], xlabel='Time [min]', title='MAGS - COOLING PLATE', grid=True)

temp_increase = df.max() - df.iloc[df.index < 1].mean()
temp_increase_cp = df_cp.max() - df_cp.iloc[df_cp.index < 1].mean()
