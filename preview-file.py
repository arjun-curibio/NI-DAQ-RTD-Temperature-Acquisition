import pandas as pd
import matplotlib.pyplot as plt

folder = 'C:/Users/15189/Desktop/MA 2.1.5 Board Thermal Testing/11_18_21 Testing/'

df = pd.read_csv(folder+'Board_TestingCoolingPlateValues.csv', sep=',', index_col=0)

df.set_index(pd.Series(df.index)/60, inplace=True)

df.plot()