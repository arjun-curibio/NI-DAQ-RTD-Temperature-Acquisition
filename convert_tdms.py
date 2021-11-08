from nptdms import TdmsFile
import numpy as np

tdms_file = TdmsFile.read("test.tdms")

all_data = np.array([])

for group in tdms_file.groups():
    group_name = group.name
    for channel in group.channels():
        
        channel_name = channel.name
        # Access dictionaries of properties
        properties = channel.properties
        # Access numpy array of data for channel
        data = channel[:]
        print(channel_name, data)

        # Access a subset of data

all_groups = tdms_file.groups()
