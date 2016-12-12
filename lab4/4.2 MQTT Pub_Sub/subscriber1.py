
from MQTT_pub_sub import MySubscriber
import time

broker_address = "192.168.1.254"
broker_port = "1883"

sub1 = MySubscriber("sub1")

sub1.start(broker_address,broker_port)

sub1.mySubscribe("time/unix/pub1",2)

while True:
	time.sleep(1)

# sub1.stop()