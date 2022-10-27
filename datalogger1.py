from os import path
from datetime import datetime
import csv

def convert(date) :
    """Converte os valores da tabela rawdata de uma data especifica e gera uma nova tabela convertida

    Args:
        date (str): String de data no formato 0000-00-00
    """

    rawdata_file = open("data/rawdata-"+date+".csv", "r")
    data = csv.reader(rawdata_file, delimiter=",")
    data = list(data)
    rawdata_file.close()

    if(path.isfile("data/data-"+date+".csv")):
        data_file = open("data/data-"+date+".csv", "r")
        data_file = csv.reader(data_file, delimiter=",")
        data_file = list(data_file)
        data_file_size = len(data_file)
    else :
        csv_file = open("data/data-"+date+".csv", "w", newline='')
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["id", 
                            "timestamp",
                            "prev_duration",
                            "bmp_temp",
                            "dht_temp",
                            "humidity",
                            "heat_index",
                            "pressure",
                            "altitude",
                            "cpu_use",
                            "cpu_temp",
                            "mem_used"
                            ])
        csv_file.close()
        data_file_size = 0

    if (data_file_size < len(data)) :

        # Log: Conversao de dados iniciada
        timestamp = str(datetime.now())
        convertlog_file = open("log/convertlog-"+date+".txt", "a")
        convertlog_file.write(timestamp+" : Conversao de dados iniciada\n")
        convertlog_file.close()

        for i in range(data_file_size+1, len(data)) :

            # Convert
            id = str(i)
            
            timestamp = data[i][0]
            
            prev_duration = data[i][1]

            bmp_temp = float(data[i][2])
            bmp_temp = round(bmp_temp, 2)
            
            dht_temp = data[i][3]
            
            humidity = data[i][4]
            
            heat_index = getHeatIndex(bmp_temp, float(humidity))
            
            pressure = float(data[i][5])
            pressure = round(pressure, 2)
            
            altitude = float(data[i][6])
            altitude = round(altitude, 2)
            
            cpu_use = data[i][7]
            
            cpu_temp = data[i][8]
            
            mem_used = data[i][9]
            
            bmp_temp = str(bmp_temp)
            heat_index = str(heat_index)
            pressure = str(pressure)
            altitude = str(altitude)

            # Save Log
            convertlog_file = open("log/convertlog-"+date+".txt", "a")
            convertlog_file.write(timestamp+
                                  " -> Previous Duration: "+prev_duration+
                                  ", BMP Temperature: "+bmp_temp+
                                  "ºC, DHT Temperature: "+dht_temp+
                                  "ºC, Humidity: "+humidity+
                                  "%, Heat Index: "+heat_index+
                                  "ºF, Pressure: "+pressure+
                                  " Pa, Altitude: "+altitude+
                                  " m, CPU Use: "+cpu_use+
                                  "%, CPU Temp: "+cpu_temp+
                                  "ºC, Mem Used: "+mem_used+"MB de 922 MB\n"
                                  )
            convertlog_file.close()

            # Save CSV
            csv_file = open("data/data-"+date+".csv", "a", newline='')
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([id,
                                 timestamp,
                                 prev_duration,
                                 bmp_temp,
                                 dht_temp,
                                 humidity,
                                 heat_index,
                                 pressure,
                                 altitude,
                                 cpu_use,
                                 cpu_temp,
                                 mem_used
                                 ])
            csv_file.close()

        # Log: Conversao de dados finalizada
        timestamp = str(datetime.now())
        convertlog_file = open("log/convertlog-"+date+".txt", "a")
        convertlog_file.write(timestamp+" : Conversao de dados finalizada\n")
        convertlog_file.close()

    else :
        timestamp = str(datetime.now())
        convertlog_file = open("log/convertlog-"+date+".txt", "a")
        convertlog_file.write(timestamp+" : Sem dados para converter\n")
        convertlog_file.close()

def getHeatIndex(temp_c, humidity) :
    """Gerar o valor do índice de calor em fahrenheit a partir da temperatura e humidade

    Args:
        temp_c (float): Temperatura em grau celsius
        humidity (float): Humidade em porcentagem

    Returns:
        float: Índice de calor em fahrenheit
    """
    
    temp_f = (temp_c*1.8)+32
    
    temp_f2 = pow(temp_f, 2)
    humidity2 = pow(humidity, 2)
    
    ic = -42.379 + (2.04901523*temp_f) + (10.14333127*humidity) - (0.22475541*temp_f*humidity) - (0.00683783*temp_f2) - (0.05481717*humidity2) + (0.00122874*temp_f2*humidity) + (0.00085282*temp_f*humidity2) - (0.00000199*temp_f2*humidity2)
    ic = round(ic, 2)
    
    return ic
