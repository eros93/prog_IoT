
import paho.mqtt.client as mqtt
import json

class MyPublisher():

	def __init__(self, clientid):
		self.client_mqtt = mqtt.Client(clientid, False)

		self.client_mqtt.on_connect = self.myOnConnect
		# self.client_mqtt.on_publish = self.myOnPublish

	def myOnConnect(self, clientid, userdata, flags, rc):
		print ("\n\tPublisher with clientid: "+str(clientid))
		print ("\n\tConnected to message Broker with result code (rc): "+str(rc))

	# def myOnPublish(self, clientid, userdata, mid):
	# 	print ("\n\tSomething has been sent...")

	def myPublish(self, topic, msg, qos=2):
		#POSSIBLE ERROR-CHECK
		self.client_mqtt.publish(topic, msg, qos)

	def start(self, broker, port):
		self.client_mqtt.connect(broker,port)
		self.client_mqtt.loop_start()

	def stop(self):
		self.client_mqtt.loop_stop()


class MySubscriber():

	def __init__(self, clientid):
		self.client_mqtt = mqtt.Client(clientid, False)

		self.client_mqtt.on_connect = self.myOnConnect
		self.client_mqtt.on_message = self.myOnMessage

	def print_time(self, string_topic, string_qos, json_payload):
		payload = json.loads(json_payload)
		print ("\n\tReceived MQTT message at topic: "+string_topic+" with QoS "+string_qos)
		print ("\n\tTime received: "+str(payload["time"]))

	def myOnConnect(self, clientid, userdata, flags, rc):
		print ("\n\tSubscriber with clientid: "+str(clientid))
		print ("\n\tConnected to message Broker with result code (rc): "+str(rc))

	def myOnMessage(self, clientid, userdata, msg):
		self.print_time(msg.topic, str(msg.qos), msg.payload)
		#print ("\n\tMessage: "+msg.topic+" "+str(msg.qos)+" "+str(msg.payload))

	def mySubscribe(self, topic, qos=2):
		#POSSIBLE ERROR-CHECK
		self.client_mqtt.subscribe(topic, qos)

	def start(self, broker, port):
		self.client_mqtt.connect(broker,port)
		self.client_mqtt.loop_start()

	def stop(self):
		self.client_mqtt.loop_stop()