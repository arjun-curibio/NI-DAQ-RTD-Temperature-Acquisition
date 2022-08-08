import pandas as pd
import matplotlib.pyplot as plt
import glob
import tkinter as tk
from tkinter import filedialog


root = tk.Tk()
root.withdraw()
filename = filedialog.askopenfilename()
root.destroy()
filename = filename[:-4]
# folder = 'C:/Users/15189/Desktop/MA 2.1.5 Board Thermal Testing/11_18_21 Testing/'
file_header = ''

filelist = glob.glob(filename + '*.csv')
isnumerics = [(file.split('.')[0][-1]).isnumeric() for file in filelist]
lastval = [(file.split('.')[0][-1]) for file in filelist]
filelistsorted = filelist.copy()
for i in range(len(filelist)):
    # print(filelist[i])
    if isnumerics[i] == False:  filelistsorted[0] = filelist[i]
    else:                       filelistsorted[int(lastval[i])+1] = filelist[i]

header = list(pd.read_csv(filelistsorted[0], header=0, index_col=False).columns)
df = pd.read_csv(filelistsorted[0], header=0, usecols=[i for i in range(1, len(header))], index_col=False)
for ii in range(1,len(filelistsorted)):
    df_temp = pd.read_csv(filelistsorted[ii], header=0, usecols=[i for i in range(1, len(header))], index_col=False)
    df = pd.concat([df, df_temp], ignore_index=True)

plt.ion()
df.plot()
df.to_csv(filename+'_total.csv', sep=',')