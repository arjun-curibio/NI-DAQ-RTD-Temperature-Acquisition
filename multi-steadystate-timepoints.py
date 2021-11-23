import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

folder = 'C:/Users/15189/Desktop/MA 2.1.5 Board Thermal Testing/11_18_21 Testing/'

plt.ion()

df = pd.read_csv(folder+'Board_TestingCoolingPlateValues_total.csv', sep=',', index_col=0)

t_starts = [82000, 3800, 7100, 14700, 20300, 24400]
t_ends   = [98000, 3900, 7200, 14800, 20400, 24500]

LABELS = ['Baseline', 'Cooling Plate\nOff', '37 C', '36 C', '35 C', '34 C']

df_values = pd.DataFrame(df.iloc[t_starts[0]:t_ends[0], :].mean()).transpose()
for ii in range(1,len(LABELS)):
    df_values = df_values.append(pd.DataFrame(df.iloc[t_starts[ii]:t_ends[ii], :].mean()).transpose(), ignore_index=True)

df_values.set_index(pd.Series(LABELS), inplace=True)

df_wells = df_values.iloc[:, [0, 2, 3]]
df_board = df_values.iloc[:, 1]

df_values_mean = df_wells.mean(axis=1)
df_values_std = df_wells.std(axis=1)




inds = np.arange(len(LABELS))
width = 0.4

fig, ax = plt.subplots()
rects1 = ax.bar(inds-width/2, df_values_mean,  width=width, yerr=df_values_std, capsize=5, label='In Wells (n=3)')
rects2 = ax.bar(inds+width/2, df_board, width=width, label='Beneath Well Plate')

# df_bvalues_mean.plot(kind='bar', legend=False, ylim=[36.5, 38.5], fontsize=12, width=0.8)
ax.set_xticks(np.arange(len(LABELS)))
ax.set_xticklabels(LABELS, fontsize=12)

ax.set_ylim([36.5, 39])
ax.set_yticklabels(ax.get_yticks(), fontsize=12)

plt.grid(axis='y')
plt.xticks(rotation=0)
plt.ylabel('Temperature [C]', fontsize=16)
plt.title('Steady state temperatures at \ndifferent cooling plate settings', fontsize=18)
ax.legend(fontsize=12)
