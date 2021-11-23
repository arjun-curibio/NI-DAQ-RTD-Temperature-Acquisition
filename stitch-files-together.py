import pandas as pd
import matplotlib.pyplot as plt
import glob

folder = 'C:/Users/15189/Desktop/MA 2.1.5 Board Thermal Testing/11_18_21 Testing/'
file_header = 'Board_TestingCoolingPlateValues'

filelist = glob.glob(folder + file_header + '*.csv')

df = pd.read_csv(filelist[0], sep=',', index_col=0)
for ii in range(1,len(filelist)):
    df_temp = pd.read_csv(filelist[ii], sep=',', index_col=0)
    df = df.append(df_temp, ignore_index=True)

df.to_csv(folder+file_header+'_total.csv', sep=',')