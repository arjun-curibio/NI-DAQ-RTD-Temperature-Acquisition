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

header = list(pd.read_csv(filelist[0], header=0, index_col=False).columns)
df = pd.read_csv(filelist[0], header=0, usecols=[i for i in range(1, len(header))], index_col=False)
for ii in range(1,len(filelist)):
    df_temp = pd.read_csv(filelist[ii], header=0, usecols=[i for i in range(1, len(header))], index_col=False)
    df = pd.concat([df, df_temp], ignore_index=True)

df.to_csv(filename+'_total.csv', sep=',')