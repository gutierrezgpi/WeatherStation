from os import popen
from datetime import datetime
from time import sleep

while True :
    
    timestamp = datetime.now()
    timestamp = str(timestamp)
    
    cpu_use = popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline()
    cpu_use = cpu_use.rstrip('\n')
    
    cpu_temp = popen("vcgencmd measure_temp").readline()
    cpu_temp = cpu_temp.replace("temp=", "")
    cpu_temp = cpu_temp.replace("'C", "")
    cpu_temp = cpu_temp.rstrip('\n')
    
    mem_used = popen("top -n1 | awk '/MB mem :/ {print $8}'").readline()
    mem_used = mem_used.rstrip("\n")
    
    mem_total = "922"
    
    print(timestamp+" -> CPU Use: "+cpu_use+"%, CPU Temp: "+cpu_temp+"°C, Mem used: "+mem_used+" MB de "+mem_total+" MB")
    
    sleep(1)