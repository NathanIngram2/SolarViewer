import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import time

# Create figure for plotting
fig = plt.figure()
plt.ion()
plt.show()

def plot_live(x, y):
        plt.clf()
        plt.xlabel('Time')
        plt.ylabel('Power (dB)')
        plt.ylim(0,10)
        plt.plot(x, y, 'b.')
        plt.draw()

x = np.linspace(0,1,10)
y = x*10
xTest = []
yTest = []

for i in range(0, len(x)):
    xTest.append(x[i])
    yTest.append(y[i])
    plot_live(xTest, yTest)
    plt.pause(1)

plt.ioff()
plt.show()