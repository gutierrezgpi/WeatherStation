from ast import For
import csv
from datetime import datetime

date = "2022-10-24"

data_file = open("data/data-"+date+".csv", "r")
data_file = csv.reader(data_file, delimiter=",")
data_file = list(data_file)
data_file_size = len(data_file)

for i in range(2, len(data_file)):
    
    
    s = datetime.strptime(data_file[i-1][1], "%Y-%m-%d %H:%M:%S.%f")
    p = datetime.strptime(data_file[i][1], "%Y-%m-%d %H:%M:%S.%f")
    
    print(p-s)