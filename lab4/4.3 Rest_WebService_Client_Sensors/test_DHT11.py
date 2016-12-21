
import Adafruit_DHT
import time

if __name__ == "__main__":
	
	sensor=Adafruit_DHT.DHT11

	pin=raw_input("\n\tPlease insert the pin number (GPIO): ")

	if pin.isdigit():
		while True:
			humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
			
			if humidity is not None and temperature is not None:
				print('\n\tTemp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
			else:
				print('\n\tFailed to get reading. Try again!')
			
			time.sleep(30)
	else:
		print("\n\tPIN must be a number!")
