
from MQTT_Client import MyClient
import RPi.GPIO as GPIO
import time
import json


class Client():

	def __init__(self, clientid ,broker_address, broker_port, relay_pin):
		self.broker = broker_address
		self.port = broker_port
		self.relay_pin = relay_pin
		self.relay_stat = 0
		self.mqttclient = MyClient(clientid, self)

		# Initial setting Relay
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(relay_pin, GPIO.OUT)
		GPIO.output(relay_pin, GPIO.LOW)

	def create_senml(self, bn, nr, value):
		obj={}
		obj["bn"] = bn
		obj["e"] = []
		
		tmp={}
		tmp["n"] = nr
		tmp["v"] = value
		tmp["t"] = str(time.time())

		obj["e"].append(tmp)
		return json.dumps(obj)

	def run(self):
		self.mqttclient.start(self.broker,self.port)

	def end(self):
		self.mqttclient.stop()

	def notify(self, topic, msg):
		if topic=="websensor/relay/set":
			payload=json.loads(msg)
			if payload["e"][0]["v"]=="0":
				print("\n\tRelay set on OFF status")
				GPIO.output(self.relay_pin, GPIO.LOW)
				relay_stat = "0"
			elif payload["e"][0]["v"]=="1":
				print("\n\tRelay set on ON status")
				GPIO.output(self.relay_pin, GPIO.HIGH)
				relay_stat = "1"
			else:
				raise NameError("stat parameter can be only 0 --> OFF or 1 --> ON")
			
			json_msg = self.create_senml("websensor/relay/stat", "relay", self.relay_stat)
			self.mqttclient.myPublish("websensor/relay/stat",json_msg)

	# self.print_msg(msg.topic, str(msg.qos), msg.payload)
	# print ("\n\tMessage: "+msg.topic+" "+str(msg.qos)+" "+str(msg.payload))