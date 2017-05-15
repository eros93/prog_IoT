
import paho.mqtt.client as mqtt
import json


class MySubscriber():

	def __init__(self, clientid):
		self.client_mqtt = mqtt.Client(clientid, False)

		self.client_mqtt.on_connect = self.myOnConnect
		self.client_mqtt.on_message = self.myOnMessage


	def myOnConnect(self, clientid, userdata, flags, rc):
		print ("\n\tSubscriber with clientid: "+str(clientid))
		print ("\n\tConnected to message Broker with result code (rc): "+str(rc))

	def myOnMessage(self, clientid, userdata, msg):
		#print ("\n\tMessage: "+msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
		self.message = json.loads(msg.payload)

	def mySubscribe(self, topic, qos=2):
		#POSSIBLE ERROR-CHECK
		self.client_mqtt.subscribe(topic, qos)

	def myUnsubscribe(self, topic):
		#POSSIBLE ERROR-CHECK
		self.client_mqtt.unsubscribe(topic)

	def start(self, broker, port):
		self.client_mqtt.connect(broker,port)
		self.client_mqtt.loop_start()

	def stop(self):
		self.client_mqtt.loop_stop()