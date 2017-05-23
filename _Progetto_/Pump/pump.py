
import paho.mqtt.client as mqtt
import socket
import requests
import json
#import RPi.GPIO as GPIO


##################
# Pump class
##################
class Pump():

	def __init__(self, pumpname, resources, subnet, relay_pin):
		self.rn = pumpname
		self.resources = resources
		self.subnet = subnet
		self.mqtt_r = "s"
		self.pin = relay_pin
		self.ip = self.get_dev_ip()

		self.mqttSub = MySubscriber(pumpname, self)

		# # Initial setting Relay
		# GPIO.setmode(GPIO.BCM)
		# GPIO.setup(relay_pin, GPIO.OUT)
		# GPIO.output(relay_pin, GPIO.LOW)


	def get_dev_ip(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(("8.8.8.8", 80))
		#print(s.getsockname()[0])
		ip = s.getsockname()[0]
		s.close()
		return ip


	def get_broker_info(self, res_ip, res_port):
		r = requests.get("http://" + res_ip + ":" + str(res_port) + "/res_cat/broker_info")
		data = json.loads(r.text)
		self.broker_ip = data["broker_ip"]
		self.broker_port = data["broker_port"]
		print "\n\tBroker infos correctly retrieved...\n\n"
		return


	def build_mqtt_t(self):
		self.mqtt_t = "actuator/subnet/"+self.subnet+"/"+self.resources[0]


	def register(self, ip, port=8080):

		self.build_mqtt_t()

		url_req = "http://"+ip+":"+str(port)+"/res_cat/new_dev"
		body = {}
		body["rn"] = self.rn
		body["resources"] = self.resources
		body["subnet"] = self.subnet
		body["mqtt_role"] = self.mqtt_r
		body["mqtt_topic"] = self.mqtt_t
		body["ip_address"] = self.ip

		print("\n\tContacting Resource Catalog...\n")
		print url_req
		print json.dumps(body)
		
		r=requests.post(url_req, data=json.dumps(body))

		if r.status_code == 200:
			print("\t--> REQUEST SUCCESS!")
			print "\n\Devices now registered:\n"
			print r.text
			return 0
		else:
			print("\n\tBad Response from Web Server")
			return 1


	def run(self):
		self.mqttSub.start(self.broker_ip, self.broker_port)
		self.mqttSub.mySubscribe(self.mqtt_t, 2)


	def end(self):
		self.mqttSub.stop()


	def notify(self, topic, msg):
		if topic == self.mqtt_t:
			#payload = json.loads(msg)
			if msg.upper() == "OFF":
				print("\n\tRelay set on OFF status")
				#GPIO.output(self.relay_pin, GPIO.LOW)
			elif msg.upper() == "ON":
				print("\n\tRelay set on ON status")
				#GPIO.output(self.relay_pin, GPIO.HIGH)
			else:
				raise NameError("Pump commands can be only \"OFF\" or \"ON\"")



##############################
# Mysubscriber class
##############################
class MySubscriber():

	def __init__(self, clientid, notifier):

		self.notifier = notifier	# See slide 31 MQTT lesson

		self.client_mqtt = mqtt.Client(clientid, False)

		self.client_mqtt.on_connect = self.myOnConnect
		self.client_mqtt.on_message = self.myOnMessage

	def myOnConnect(self, clientid, userdata, flags, rc):
		print ("\n\tSubscriber with clientid: "+str(clientid))
		print ("\n\tConnected to message Broker with result code (rc): "+str(rc))

	def myOnMessage(self, clientid, userdata, msg):
		self.notifier.notify(msg.topic, msg.payload)	# See slide 31 MQTT lesson
		#print ("\n\tMessage: "+msg.topic+" "+str(msg.qos)+" "+str(msg.payload))

	def mySubscribe(self, topic, qos=2):
		#POSSIBLE ERROR-CHECK
		self.client_mqtt.subscribe(topic, qos)

	def start(self, broker, port):
		self.client_mqtt.connect(broker,port)
		self.client_mqtt.loop_start()

	def stop(self):
		self.client_mqtt.loop_stop()