
from MQTT_Client import MyPublisher
import time

broker_address = "192.168.1.254"
broker_port = "1883"
topic_relay_set = "websensor/relay/set"

pub1 = MyPublisher("3_pub")

pub1.start(broker_address,broker_port)
time.sleep(2)

print ("\n\n\t----------> Relay Control Publisher <----------")
print ("\n\t------------> Powered by E&E <-------------")
print ("\n\t-------> COMMANDS: 0-->OFF and 1-->ON")
ans=True
while ans:
	ans=raw_input("\n\n\tWhat state for the relay?\t")
	if ans=="0":
		print("\n\t---> Relay will be set on OFF status")
		msg = pub1.create_senml(topic_relay_set, "relay", "0")
		pub1.myPublish(topic_relay_set, msg, 2)

	elif ans=="1":
		print("\n\t---> Relay will be set on ON status")
		msg = pub1.create_senml(topic_relay_set, "relay", "1")
		pub1.myPublish(topic_relay_set, msg, 2)

	else:
		print("\n\tNot Valid Choice Try again")
