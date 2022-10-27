import matplotlib.pyplot as plt
from csv import reader
from dateutil import parser
import numpy as np
import datalogger1 as dl

date = "2022-10-25"

dl.convert(date)

file = open("data/data-"+date+".csv", "r")
data = reader(file, delimiter=",")
data = list(data)

x_time = [parser.parse(i[1]) for i in data[1::]]
y_bmp_temp = [float(i[3]) for i in data[1::]]
y_dht_temp = [float(i[4]) for i in data[1::]]
y_humidity = [float(i[5]) for i in data[1::]]

fig, ax = plt.subplots()

ax.set_yticks(np.arange(0, 100, 1))
ax.set_yticks(np.arange(0, 100, 0.1), minor=True)

ax.plot(x_time, y_humidity, marker=".", label="humidity")
ax.plot(x_time, y_bmp_temp, marker=".", label="bmp_temp")
ax.plot(x_time, y_dht_temp, marker=".", label="dht_temp")
ax.legend()
ax.grid(which='both')
ax.grid(True)
plt.show()