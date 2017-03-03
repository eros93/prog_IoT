
import requests
import json
import paho.mqtt.client as mqtt


class ResourceCatalog(object):
	"""Class used to retrieve informations from a given Resource Catalog"""

	def __init__(self, ip, port):
		self.ip_res_cat = ip
		self.port_res_cat = port
		self.get_weather_adpt_info()
		self.get_broker_info()
		return

	def get_weather_adpt_info(self):
		r = requests.get("http://" + self.ip_res_cat + ":" + str(self.port_res_cat) + "/res_cat/weather_adaptor")
		self.data = json.loads(r.text)
		self.api_key = self.data["api_key"]
		self.lat = self.data["latitude"]
		self.lng = self.data["longitude"]
		self.mqtt_t_out = self.data["mqtt_t_out"]
		print "\n\tLocaltion infos correctly retrieved..."
		return

	def get_broker_info(self):
		r = requests.get("http://" + self.ip_res_cat + ":" + str(self.port_res_cat) + "/res_cat/broker_info")
		self.data = json.loads(r.text)
		self.broker_ip = self.data["broker_ip"]
		self.broker_port = self.data["broker_port"]
		print "\n\tBroker infos correctly retrieved...\n\n"
		return


class WeatherInfo(object):
	"""Core class, works as adaptor for Dark Sky Weather API.
	Produce JSON strings to be sent """

	def __init__(self, api_key, lat, lng):
		self.api_key = api_key
		self.lat=lat
		self.lng=lng
		return
	
	# If it would be necessary to save on a file!
	def save_on_file(self, filename, string):
		rc = open("./"+filename, "w")
		rc.truncate()
		rc.write(self.rc_json)
		rc.close()
		return


	def contact_api(self):
		r = requests.get("https://api.darksky.net/forecast/"+self.api_key+"/"+str(self.lat)+","+str(self.lng)+"/?units=si")
		self.rc_json = r.content
		self.rc_obj = json.loads(self.rc_json)
		# self.save_on_file("forecast.json", self.rc_json)
		self.currently = self.rc_obj["currently"]
		self.hourly = self.rc_obj["hourly"]
		self.daily = self.rc_obj["daily"]
		return


	def tomorrow_forecast(self):

		self.contact_api()

		tmp_obj={}
		tmp_obj["request"] = "tomorrow_forecast"
		tmp_obj["summary"] = self.daily["data"][1]["summary"]
		
		tmp_obj["sunrise"] =  self.daily["data"][1]["sunriseTime"]
		tmp_obj["sunset"] =  self.daily["data"][1]["sunsetTime"]
		
		tmp_obj["precipProb"] = self.daily["data"][1]["precipProbability"]
		tmp_obj["precipInt"] = self.daily["data"][1]["precipIntensity"]
		
		#return json.dumps(tmp_obj, sort_keys=True, indent=4, separators=(',', ': '))	#prettyprint
		return json.dumps(tmp_obj)


#MQTT Publisher
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

	def myPublish(self, topic, msg, qos=2, retain=False):
		#POSSIBLE ERROR-CHECK
		self.msg = msg
		self.client_mqtt.publish(topic, msg, qos, retain)
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