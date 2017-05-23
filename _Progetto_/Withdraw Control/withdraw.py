import urllib2
import time
import json
import paho.mqtt.client as mqtt

############################################################
# Withdraw Classes
############################################################

class Withdraw():

	def __init__(self, clientid):

		self.mqtt_sub_weather = MySubscriber("weathersub"+clientid, self)
		self.mqtt_sub_usedwater = MySubscriber("usedwatersub"+clientid, self)
		
	def get_all_data(self, IP, port):
		response=urllib2.urlopen("http://" + str(IP) + ":" + str(port) + "/res_cat/all")
		data=response.read()
		obj=json.loads(data)

		self.broker_ip = obj["broker_ip"]
		self.broker_port = obj["broker_port"]
		self.topic_weather = obj["weath_mqtt_out_topic"]
		self.topic_usedwater = obj["usedwater_topic"]

		return obj

	def search_topic_inpump(self, all_res_cat):
		for dev in all_res_cat["dev_list"]:
			if dev["resources"][0]=="in_pump":
				self.topic_inpump = dev["mqtt_topic"]
				return

	def run(self):
		self.mqtt_sub_weather.start(self.broker_ip, self.broker_port)
		self.mqtt_sub_weather.mySubscribe(self.topic_weather)


	def end(self):
		self.mqtt_sub_weather.stop()
		self.mqtt_sub_usedwater.stop()

	def notify(self, topic, payload):
		
		if (topic == self.topic_weather):
			#print "Sono in notify topic weather"
			msg = json.loads(payload)
			
			if (msg["watering_flag"]=="True"):
				self.mqtt_sub_usedwater.start(self.broker_ip, self.broker_port)
				self.mqtt_sub_usedwater.mySubscribe(self.topic_usedwater)
				time.sleep(3)

			self.mqtt_sub_weather.stop()
			#self.mqtt_sub_weather.client_mqtt.disconnect()
	
		elif (topic == self.topic_usedwater):
			#print "Sono in notify topic usedwater"
			self.mqtt_sub_usedwater.stop()
			#self.mqtt_sub_usedwater.client_mqtt.disconnect()
			#print "Publish pump ON for time "+payload
			pub = MyPublisher("Withdraw")
			pub.start(self.broker_ip,self.broker_port)
			time.sleep(2)
			pub.myPublish(self.topic_inpump, "ON")
			time.sleep(int(payload))
			pub.myPublish(self.topic_inpump, "OFF")
			pub.stop()
			#pub.client_mqtt.disconnect()
		return


############################################################
# MQTT Classes
############################################################

class MyPublisher():

	def __init__(self, clientid):
		self.client_mqtt = mqtt.Client(clientid, False)

		self.client_mqtt.on_connect = self.myOnConnect
		self.client_mqtt.on_publish = self.myOnPublish
		return

	def myOnConnect(self, clientid, userdata, flags, rc):
		print ("\n\tPublisher with clientid: "+str(clientid))
		print ("\n\tConnected to message Broker with result code (rc): "+str(rc))
		return

	def myOnPublish(self, clientid, userdata, mid):
	 	print ("\n\tMessage sent:")
	 	print ("\n\t"+self.msg)
	 	self.msg = None
	 	return

	def myPublish(self, topic, msg, qos=2):
		#POSSIBLE ERROR-CHECK
		self.msg = msg
		self.client_mqtt.publish(topic, msg, qos)
		return

	def start(self, broker, port):
		self.broker=broker
		self.port=port
		self.client_mqtt.connect(self.broker,self.port)
		self.client_mqtt.loop_start()
		return

	def stop(self):
		self.client_mqtt.loop_stop()
		return


class MySubscriber():

	def __init__(self, clientid, notifier):

		self.notifier = notifier

		self.client_mqtt = mqtt.Client(clientid, False)

		self.client_mqtt.on_connect = self.myOnConnect
		self.client_mqtt.on_message = self.myOnMessage


	def myOnConnect(self, clientid, userdata, flags, rc):
		print ("\n\tSubscriber with clientid: "+str(clientid))
		print ("\n\tConnected to message Broker with result code (rc): "+str(rc))

	def myOnMessage(self, clientid, userdata, msg):
		self.notifier.notify(msg.topic, msg.payload)
		#print ("\n\tMessage: "+msg.topic+" "+str(msg.qos)+" "+str(msg.payload))

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
