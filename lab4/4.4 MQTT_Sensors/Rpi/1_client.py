
from Client_tools import Client
import Adafruit_DHT
import time
import json

broker_address = "192.168.1.254"
broker_port = "1883"
dht_pin = 4
relay_pin = 26

if __name__ == '__main__':

	client1 = Client("1_client", broker_address, broker_port, relay_pin)

	client1.run()

	client1.mqttclient.mySubscribe("websensor/relay/set",2)

	while True:
		
		humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, dht_pin)
		obj_temp={}
		obj_temp["bn"]=("websensor/dht/temp")
		obj_temp["e"]=[]
		tmp={}
		tmp["n"]="DHT11"
		tmp["v"]=str(temperature)
		tmp["t"]=str(time.time())
		obj_temp["e"].append(tmp)
		payload_temp = json.dumps(obj_temp)
		client1.mqttclient.myPublish("websensor/dht/temp", payload_temp)
		print("\n\tTemperature: "+str(temperature))
		
		obj_hum={}
		obj_hum["bn"]=("websensor/dht/hum")
		obj_hum["e"]=[]
		tmp={}
		tmp["n"]="DHT11"
		tmp["v"]=str(humidity)
		tmp["t"]=str(time.time())
		obj_hum["e"].append(tmp)
		payload_hum = json.dumps(obj_hum)
		client1.mqttclient.myPublish("websensor/dht/hum", payload_hum)
		print("\n\tHumidity: "+str(humidity))

		time.sleep(30)

		humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, dht_pin)
		obj_temp={}
		obj_temp["bn"]=("websensor/dht/temp")
		obj_temp["e"]=[]
		tmp={}
		tmp["n"]=str("DHT11")
		tmp["v"]=str(temperature)
		tmp["t"]=str(time.time())
		obj_temp["e"].append(tmp)
		payload_temp = json.dumps(obj_temp)
		client1.mqttclient.myPublish("websensor/dht/temp", payload_temp)
		print("\n\tTemperature: "+str(temperature))

		time.sleep(30)