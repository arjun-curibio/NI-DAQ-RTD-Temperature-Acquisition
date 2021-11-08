
#task = ndm.Task()
#task.ai_channels.add_ai_rtd_chan("RTD4_1/ai0", current_excit_source=ES.INTERNAL, current_excit_val=0.001, resistance_config=RC.THREE_WIRE)
#task.ai_channels.add_ai_rtd_chan("RTD4_1/ai1", current_excit_source=ES.INTERNAL, current_excit_val=0.001, resistance_config=RC.THREE_WIRE)
#task.ai_channels.add_ai_rtd_chan("RTD4_1/ai2", current_excit_source=ES.INTERNAL, current_excit_val=0.001, resistance_config=RC.THREE_WIRE)
#task.ai_channels.add_ai_rtd_chan("RTD4_1/ai3", current_excit_source=ES.INTERNAL, current_excit_val=0.001, resistance_config=RC.THREE_WIRE)

#task.start()
#value = task.read()
#print(value)

#task.stop()
#task.close()

#task.ai_channels

#%%
import nidaqmx as ndm
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from nidaqmx.constants import ExcitationSource as ES, ResistanceConfiguration as RC

# Read from DAQ Device
def readdaq():
    task = ndm.Task()
    task.ai_channels.add_ai_rtd_chan("RTD4_1/ai0", current_excit_source=ES.INTERNAL, current_excit_val=0.001, resistance_config=RC.THREE_WIRE)
    task.ai_channels.add_ai_rtd_chan("RTD4_1/ai1", current_excit_source=ES.INTERNAL, current_excit_val=0.001, resistance_config=RC.THREE_WIRE)
    task.ai_channels.add_ai_rtd_chan("RTD4_1/ai2", current_excit_source=ES.INTERNAL, current_excit_val=0.001, resistance_config=RC.THREE_WIRE)
    task.ai_channels.add_ai_rtd_chan("RTD4_1/ai3", current_excit_source=ES.INTERNAL, current_excit_val=0.001, resistance_config=RC.THREE_WIRE)

    task.start()
    value = task.read()
    print(value)
    task.stop()
    task.close()
    return value

# Write Data Function
def writefiledata(t, x, filename):
    # Open File
    file = open(filename, "a")
    # Write Data
    time = str(t)
    file.write(time)
    for i in x:
        file.write("\t" + str(round(i, 3)))
    file.write("\n")
    # Close File
    file.close()
# Initialize Logging
filename = "tempdata.txt"
Ts = 2 # Sampling Time [seconds]
N = 100
k = 1
x_len = N # Number of points to display
Tmin = 5; Tmax = 42
y_range = [Tmin, Tmax] # Range of possible Y values to display
data = []

file = open(filename, 'a')
file.write('Time')

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = list(range(0, N))
ys = [0] * x_len
ax.set_ylim(y_range)

task = ndm.Task()

# Create a blank line. We will update the line in animate
line, = ax.plot(xs, ys)
# Configure Plot
plt.title('Temperature')
plt.xlabel('t [s]')
plt.ylabel('Temp [degC]')
plt.grid()

#Logging Temperature Data from DAQ Device
def logging(i, ys):
    value = readdaq()
    print("T =", value, "[degC]")
    data.append(value)
    time.sleep(Ts)
    global k
    k = k + 1
    writefiledata(k*Ts, value, filename)
    # Add y to list
    ys.append(value)
    # Limit y list to set number of items
    ys = ys[-x_len:]
    # Update line with new Y values
    line.set_ydata(ys)
    return line,

ani = animation.FuncAnimation(fig,
    logging,
    fargs=(ys,),
    interval=100,
    blit=True)
plt.show()