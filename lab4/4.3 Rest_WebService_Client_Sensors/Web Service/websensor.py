
import json
import Adafruit_DHT
import RPi.GPIO as GPIO

class WebSensor(object):

	exposed=True

	def __init__(self, id):
		self.id = id
		
		self.temp_hum_sens_pin = 4
		
		# Relay initially set to LOW
		self.relay_pin = 17
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.relay_pin, GPIO.OUT)
		GPIO.output(self.relay_pin, GPIO.LOW)
		self.relstat = "0"

	def dht_getinfo(self, pin):
		# self.humidity = 57
		# self.temperature = 21
		self.humidity, self.temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, pin)

	def GET (self, *uri, **params):
		result = {}

		if uri[0]=="temp":
			self.dht_getinfo(self.temp_hum_sens_pin)
			result["temp"] = str(self.temperature)
			return json.dumps(result)

		elif uri[0]=="hum":
			self.dht_getinfo(self.temp_hum_sens_pin)
			result["hum"] = str(self.humidity)
			return json.dumps(result)

		elif uri[0]=="all":
			self.dht_getinfo(self.temp_hum_sens_pin)
			result["hum"] = str(self.humidity)
			result["temp"] = str(self.temperature)
			return json.dumps(result)
		
		elif uri[0]=="relay_stat":
			# self.relstat = GPIO.inpu(self.relay_pin)
			result["relay_stat"] = self.relstat
			return json.dumps(result)

		elif uri[0]=="relay_set":
			if params["stat"].isdigit:
				if params["stat"]=="0":
					GPIO.output(self.relay_pin, GPIO.LOW)
				elif params["stat"]=="1":
					GPIO.output(self.relay_pin, GPIO.HIGH)
				else:
					raise NameError("stat parameter can be only 0 --> OFF or 1 --> ON")
				# self.relstat = GPIO.inpu(self.relay_pin)
				self.relstat = params["stat"]
				result["relay_stat"] = self.relstat 
				return json.dumps(result)
			else:
				raise NameError ("Need a number as parameter: 0 --> OFF, 1 --> ON")

		else:
			raise NameError ("Not valid command in uri [temp/hum/all/relay_stat/relay_set]")
