import matplotlib.pyplot as plt
from csv import reader
from dateutil import parser
import numpy as np
import datalogger1 as dl

date = "2022-10-26"

dl.convert(date)

file = open("data/data-"+date+".csv", "r")
data = reader(file, delimiter=",")
data = list(data)

x_time = [parser.parse(i[1]) for i in data[1::]]
y_bmp_temp = [float(i[6]) for i in data[1::]]

fig, ax = plt.subplots()

ax.set_yticks(np.arange(0, 130, 1))
ax.set_yticks(np.arange(0, 130, 0.1), minor=True)

ax.plot(x_time, y_bmp_temp, marker=".", label="heat_index")
ax.legend()
ax.grid(which='both')
ax.grid(True)
plt.show()