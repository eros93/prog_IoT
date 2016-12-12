
from MQTT_pub_sub import MyPublisher
import time
import json

broker_address = "192.168.1.254"
broker_port = "1883"

pub1 = MyPublisher("pub1")

pub1.start(broker_address,broker_port)

while True:

	time_unix = time.time()
	payload1 = json.dumps({"time":time_unix})
	pub1.myPublish("time/unix/pub1", payload1)
	print("\n\t"+str(time_unix))

	time_format = time.strftime("%d-%m-%y %H:%M", time.gmtime())
	payload2 = json.dumps({"time":time_format})
	pub1.myPublish("time/format/pub1", payload2)
	print("\n\t"+time_format)

	time.sleep(30)

	time_unix = time.time()
	payload1 = json.dumps({"time":time_unix})
	pub1.myPublish("time/unix/pub1", payload1)
	print("\n\t"+str(time_unix))

	time.sleep(30)