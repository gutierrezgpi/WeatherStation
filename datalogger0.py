import board
import adafruit_bmp280
import adafruit_dht

from os import path
from os import popen
from os import mkdir
from datetime import datetime
from time import sleep

def receive() :
    
    i2c = board.I2C()
    
    bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x76)

    bmp280.sea_level_pressure = 1013.25
    bmp280.mode = adafruit_bmp280.MODE_NORMAL
    bmp280.standby_period = adafruit_bmp280.STANDBY_TC_500
    bmp280.iir_filter = adafruit_bmp280.IIR_FILTER_X16
    bmp280.overscan_pressure = adafruit_bmp280.OVERSCAN_X16
    bmp280.overscan_temperature = adafruit_bmp280.OVERSCAN_X2

    dht22 = adafruit_dht.DHT22(board.D4)

    prev_timestamp = datetime.now()

    sleep(2)
    
    if (not path.exists("log")) :
        mkdir("log")
    if (not path.exists("data")) :
        mkdir("data")

    # Log
    timestamp = str(datetime.now())
    print(timestamp+" -> Captura iniciada!\n")
    log_file = open("log/receivelog-"+timestamp[0:10]+".txt", "a")
    log_file.write(timestamp+" -> Captura iniciada\n\n")
    log_file.close()

    while True :

        timestamp = datetime.now()
        prev_duration = timestamp - prev_timestamp
        prev_timestamp = timestamp
        timestamp = str(timestamp)
        str_prev_duration = str(prev_duration)

        try :

            # DHT22
            dht_temp = dht22.temperature
            dht_temp = str(dht_temp)

            humidity = dht22.humidity
            humidity = str(humidity)

            # BMP280
            bmp_temp = bmp280.temperature
            bmp_temp = str(bmp_temp)

            pressure = bmp280.pressure
            pressure = str(pressure)

            altitude = bmp280.altitude
            altitude = str(altitude)
            
            # Board
            cpu_use = popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline()
            cpu_use = cpu_use.replace(",", ".")
            cpu_use = cpu_use.rstrip('\n')
            
            cpu_temp = popen("vcgencmd measure_temp").readline()
            cpu_temp = cpu_temp.replace("temp=", "")
            cpu_temp = cpu_temp.replace("'C", "")
            cpu_temp = cpu_temp.rstrip('\n')
            
            mem_used = popen("top -n1 | awk '/MB mem :/ {print $8}'").readline()
            mem_used = mem_used.replace(",", ".")
            mem_used = mem_used.rstrip("\n")

            # print
            print(timestamp+
                " -> Previous Duration: "+str_prev_duration+
                ", BMP Temperature: "+bmp_temp+
                "ºC, DHT Temperature: "+dht_temp+
                "ºC, Humidity: "+humidity+
                "%, Pressure: "+pressure+
                " Pa, Altitude: "+altitude+
                " m, CPU Use: "+cpu_use+
                "%, CPU Temp: "+cpu_temp+
                "ºC, Mem Used: "+mem_used+"MB de 922 MB"
                )

            # csv
            if(path.isfile("data/rawdata-"+timestamp[0:10]+".csv")):
                csv_file = open("data/rawdata-"+timestamp[0:10]+".csv", "a", newline='')
                csv_file.write(timestamp+","+
                            str_prev_duration+","+
                            bmp_temp+","+
                            dht_temp+","+
                            humidity+","+
                            pressure+","+
                            altitude+","+
                            cpu_use+","+
                            cpu_temp+","+
                            mem_used+"\n"
                            )
                csv_file.close()
            else :
                csv_file = open("data/rawdata-"+timestamp[0:10]+".csv", "w", newline='')
                csv_file.write("timestamp,prev_duration,bmp_temp,dht_temp,humidity,pressure,altitude,cpu_use,cpu_temp,mem_used\n")
                csv_file.write(timestamp+","+
                            str_prev_duration+","+
                            bmp_temp+","+
                            dht_temp+","+
                            humidity+","+
                            pressure+","+
                            altitude+","+
                            cpu_use+","+
                            cpu_temp+","+
                            mem_used+"\n"
                            )
                csv_file.close()

            # log
            log_file = open("log/receivelog-"+timestamp[0:10]+".txt", "a")
            log_file.write(timestamp+
                        " -> Previous Duration: "+str_prev_duration+
                        ", BMP Temperature: "+bmp_temp+
                        "ºC, DHT Temperature: "+dht_temp+
                        "ºC, Humidity: "+humidity+
                        "%, Pressure: "+pressure+
                        " Pa, Altitude: "+altitude+
                        " m, CPU Use: "+cpu_use+
                        "%, CPU Temp: "+cpu_temp+
                        "ºC, Mem Used: "+mem_used+"MB de 922 MB\n"
                        )
            log_file.close()

        except RuntimeError as e:

            # print
            print(timestamp+
                " -> Previous Duration: "+str_prev_duration+
                ", DHT Erro: "+e.args[0]+
                ", BMP Temperature: "+bmp_temp+
                "°C, Pressure: "+pressure+
                " Pa, Altitude: "+altitude+
                " m, CPU Use: "+cpu_use+
                "%, CPU Temp: "+cpu_temp+
                "ºC, Mem Used: "+mem_used+"MB de 922 MB"
                )
            
            # csv
            if(path.isfile("data/rawdata-"+timestamp[0:10]+".csv")):
                csv_file = open("data/rawdata-"+timestamp[0:10]+".csv", "a", newline='')
                csv_file.write(timestamp+","+
                            str_prev_duration+","+
                            bmp_temp+","+
                            "0"+","+
                            "0"+","+
                            pressure+","+
                            altitude+","+
                            cpu_use+","+
                            cpu_temp+","+
                            mem_used+"\n"
                            )
                csv_file.close()
            else :
                csv_file = open("data/rawdata-"+timestamp[0:10]+".csv", "w", newline='')
                csv_file.write("timestamp,prev_duration,bmp_temp,dht_temp,humidity,pressure,altitude,cpu_use,cpu_temp,mem_used\n")
                csv_file.write(timestamp+","+
                            str_prev_duration+","+
                            bmp_temp+","+
                            "0"+","+
                            "0"+","+
                            pressure+","+
                            altitude+","+
                            cpu_use+","+
                            cpu_temp+","+
                            mem_used+"\n"
                            )
                csv_file.close()
            
            # log
            log_file = open("log/receivelog-"+timestamp[0:10]+".txt", "a")
            log_file.write(timestamp+
                        " -> Previous Duration: "+str_prev_duration+
                        ", DHT Erro: "+e.args[0]+
                        ", BMP Temperature: "+bmp_temp+
                        "°C, Pressure: "+pressure+
                        " Pa, Altitude: "+altitude+
                        " m, CPU Use: "+cpu_use+
                        "%, CPU Temp: "+cpu_temp+
                        "ºC, Mem Used: "+mem_used+"MB de 922 MB\n"
                        )
            log_file.close()
            
            duration = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
            duration = datetime.now()-duration
            duration = duration.total_seconds()
            sleep(2-0.2)
            
            continue

        except Exception as e:

            dht22.exit()
            raise e
        
        duration = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
        duration = datetime.now()-duration
        duration = duration.total_seconds()
        sleep(2-0.6)

receive()