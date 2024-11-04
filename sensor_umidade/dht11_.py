import machine
import time
import rele
import dht

def dht11():    
    sensor = dht.DHT11(machine.Pin(4))
    sensor.measure()
    t=sensor.temperature()
    h=sensor.humidity()
    while True:
        if t >= 29:
           print(t)
           rele()
        else:   
            print("Temperatura: {}º  Umidade: {}%".format(t, h))
            time.sleep(5)
