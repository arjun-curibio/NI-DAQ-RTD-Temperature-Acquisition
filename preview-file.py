# Script to view files
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

filepath = filedialog.askopenfilename()
df = pd.read_csv(filepath, sep=',', index_col=0, header=3)

df.set_index(pd.Series(df.index)/60, inplace=True)
df.plot()