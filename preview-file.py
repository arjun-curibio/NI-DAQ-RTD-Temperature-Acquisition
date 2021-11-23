import pandas as pd
import matplotlib.pyplot as plt

folder = 'C:/Users/15189/Desktop/MA 2.1.5 Board Thermal Testing/11_09_21 Testing/'

df = pd.read_csv(folder+'test10.csv', sep=',', index_col=0).plot()
