import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('C:/Users/Nanosurface/Desktop/2.1.5-Board-Thermal-Testing/11_08_21 Testing/test7.csv',sep=',', index_col=0)

plt.ion()
df.plot()