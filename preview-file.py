# Script to view files
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

filepath = filedialog.askopenfilename(filetypes=[('CSV','*.csv')])
df = pd.read_csv(filepath, index_col=False)
df.set_index('t', inplace=True)
plt.ion()
df.set_index(pd.Series(df.index), inplace=True)
df.plot()
plt.title(filepath.split('/')[-1])