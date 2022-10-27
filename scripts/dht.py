import time
import board
import adafruit_dht

dht22 = adafruit_dht.DHT22(board.D4)

time.sleep(2)

while True :

    try :

        temperature = dht22.temperature
        humidity = dht22.humidity

        print("DHT22 Temp: "+str(temperature)+" °C Humi: "+str(humidity)+" %")
        
    except RuntimeError as e:

        print(e.args[0])
        time.sleep(2.0)
        continue

    except Exception as e:

        dht22.exit()
        raise e

    time.sleep(2)