
from MQTT_Client import MySubscriber
import time

broker_address = "192.168.1.254"
broker_port = "1883"

sub1 = MySubscriber("2_sub")

sub1.start(broker_address,broker_port)

sub1.mySubscribe("websensor/dht/temp",2)
sub1.mySubscribe("websensor/dht/hum",2)
sub1.mySubscribe("websensor/relay/stat",2)

while True:
	time.sleep(1)

# sub1.stop()