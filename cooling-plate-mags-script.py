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
df.drop(range(120), inplace=True)
df.set_index(pd.Series(df.index)/60, inplace=True)

df_cp = pd.read_csv(folder + file_cp, index_col=0)
df_cp.drop(range(860, df_cp.shape[0]), inplace=True)
df_cp.drop(range(120), inplace=True)
df_cp.set_index(pd.Series(df_cp.index)/60, inplace=True)

temp_increase = df.max() - df.iloc[0,:]
temp_increase_cp = df_cp.max() - df_cp.iloc[0,:]

df.plot(ax=ax1[0], ylabel='Temperature [C]', title='Without Cooling Plate\nTemperature Change = '+str(round(temp_increase.mean(), 2))+' C', grid=True)
df_cp.plot(ax=ax1[1], title='With Cooling Plate\nTemperature Change = '+str(round(temp_increase_cp.mean(), 2))+' C', grid=True, legend=False)


fig.suptitle('Well Temperature with 2.1.5 Board Powered', fontsize=16)
fig.supxlabel('Time [m]')

