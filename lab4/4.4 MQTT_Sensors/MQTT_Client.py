
import paho.mqtt.client as mqtt
import json
import time

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

	def start(self, broker, port):
		self.broker=broker
		self.port=port
		self.client_mqtt.connect(self.broker,self.port)
		self.client_mqtt.loop_start()

	def stop(self):
		self.client_mqtt.loop_stop()


class MySubscriber():

	def __init__(self, clientid):
		self.client_mqtt = mqtt.Client(clientid, False)

		self.client_mqtt.on_connect = self.myOnConnect
		self.client_mqtt.on_message = self.myOnMessage

	def print_msg(self, string_topic, string_qos, json_payload):
		print ("\n\tReceived MQTT message at topic: "+string_topic+" with QoS "+string_qos)
		payload = json.loads(json_payload)

		if payload["bn"]=="/temp":
			print("\n\tTemperature: "+payload["e"][0]["v"]+"*C")
		elif payload["bn"]=="/hum":
			print("\n\tHumidity: "+payload["e"][0]["v"]+"%")
		elif payload["bn"]=="/relay_stat":
			print("\n\tRelay status: "+payload["e"][0]["v"])

		print("\tTime (linux): "+payload["e"][0]["t"])

	def myOnConnect(self, clientid, userdata, flags, rc):
		print ("\n\tSubscriber with clientid: "+str(clientid))
		print ("\n\tConnected to message Broker with result code (rc): "+str(rc))

	def myOnMessage(self, clientid, userdata, msg):
		#self.print_msg(msg.topic, str(msg.qos), msg.payload)
		print ("\n\tMessage: "+msg.topic+" "+str(msg.qos)+" "+str(msg.payload))

	def mySubscribe(self, topic, qos=2):
		#POSSIBLE ERROR-CHECK
		self.client_mqtt.subscribe(topic, qos)

	def start(self, broker, port):
		self.broker=broker
		self.port=port
		self.client_mqtt.connect(self.broker,self.port)
		self.client_mqtt.loop_start()

	def stop(self):
		self.client_mqtt.loop_stop()


class MyClient():

	def __init__(self, clientid, notifier):
		
		self.notifier=notifier	# See slide 31 MQTT lesson
		
		self.client_mqtt = mqtt.Client(clientid, False)

		self.client_mqtt.on_connect = self.myOnConnect
		self.client_mqtt.on_message = self.myOnMessage

	def myOnConnect(self, clientid, userdata, flags, rc):
		print ("\n\tClient with clientid: "+str(clientid))
		print ("\n\tConnected to message Broker with result code (rc): "+str(rc))

	# def myOnPublish(self, clientid, userdata, mid):
	# 	print ("\n\tSomething has been sent...")

	def myPublish(self, topic, msg, qos=2):
		#POSSIBLE ERROR-CHECK
		self.client_mqtt.publish(topic, msg, qos)

	def mySubscribe(self, topic, qos=2):
		#POSSIBLE ERROR-CHECK
		self.client_mqtt.subscribe(topic, qos)

	def myOnMessage(self, clientid, userdata, msg):
		self.notifier.notify(msg.topic, msg.payload)	# See slide 31 MQTT lesson
		#print ("\n\tMessage: "+msg.topic+" "+str(msg.qos)+" "+str(msg.payload))

	def start(self, broker, port):
		self.broker=broker
		self.port=port
		self.client_mqtt.connect(self.broker,self.port)
		self.client_mqtt.loop_start()

	def stop(self):
		self.client_mqtt.loop_stop()