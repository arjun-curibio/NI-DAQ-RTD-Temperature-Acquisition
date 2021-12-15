import pandas as pd
import matplotlib.pyplot as plt
import glob

plt.close('all')

folder = 'C:/Users/15189/Desktop/MA 2.1.5 Board Thermal Testing/12_14_21 Testing/'


filenames = [
    '2.1.5_100mA_6Hz_10ms_CoolingPlate_36.0C.csv',
            ]

titleStrings = [
    '100 mA / 6 Hz / 10 ms // Cooling Plate',
    
]

fig, ax = plt.subplots(1,3, sharex=True, sharey=True)
fig2, ax2 = plt.subplots(1,len(filenames), sharex=True, sharey=True)

# T_steady_state = pd.DataFrame(data=[0,0,0], index=['0'], columns=['B1', 'B4', 'C6'])
# T_60 = pd.DataFrame([0,0,0], index=['0 0 0'], columns=['B1', 'B4', 'C6'])

ifile = 0
for file in filenames:
    file_sep = file.split(sep='_')
    # titleString = ' / '.join(file_sep[-3:])[:-4]
    titleString = titleStrings[ifile]
    df = pd.read_csv(folder + file, sep=',', index_col=0, usecols=[0,3,4])
    ts = pd.read_csv(folder + file[:-4] + '_info.txt', skiprows=5, names=[ii for ii in range(100)]).dropna(axis=1).transpose()

    
    idx60 = (ts.iloc[:,1]-(60*60)).abs().idxmin()

    df_tps = pd.DataFrame(
                df[(df.index > ts.iloc[0,0]) & 
                (df.index < ts.iloc[0,1])]
                .mean()).transpose()
    for ii in range(1, ts.shape[0]):
        df_tps = df_tps.append(
                    pd.DataFrame(
                        df[(df.index > ts.iloc[ii,0]) & 
                        (df.index < ts.iloc[ii,1])]
                        .mean()).transpose(),
                    ignore_index=True
                )

    df_tps = df_tps - df_tps.iloc[0,:]
    df_tps.set_index(pd.Series(ts.iloc[:,0])/60, inplace=True)
    
    df_tps.plot(
        markersize=10, 
        marker='o', 
        xlabel='Time [m]', 
        ylabel='Temperature Rise [C]', 
        title='Mantarray Stimulator\n'+titleString,
        grid=True)

    for ii in range(3):
        df_tps.iloc[:,ii].plot(
            ax=ax[ii], 
            markersize=10, 
            marker='o', 
            xlabel='Time [m]', 
            ylabel='Temperature Rise [C]', 
            title=('Well '+list(df_tps.columns.values)[ii]), 
            label=titleString, 
            grid=True)
    
    df.plot(ax=ax2[ifile], title=titleString)
    ifile += 1

    """
    T_steady_state = T_steady_state.append(
                        pd.DataFrame(
                            df_tps.iloc[-1, :]).transpose().rename(
                                    {pd.DataFrame(df_tps.iloc[-1,:]).transpose().index.values[0]:titleString}, 
                                axis='index'),
                        ignore_index=True
                     )   
    T_60 = T_60.append(
                pd.DataFrame(
                    df_tps.iloc[-1, :]).transpose().rename(
                            {pd.DataFrame(df_tps.iloc[-1,:]).transpose().index.values[0]:titleString}, 
                        axis='index'),
                ignore_index=True
            )
            """
ax[0].legend(titleStrings)
fig.suptitle('Mantarray Stimulator\n')