import paho.mqtt.client as MQTT

class MQTTClient():
    """It works as an MQTT publisher and subscriber"""

    def __init__(self, broker):
        self.broker = broker['ip']
        self.port = broker['port']
        self.message = ''
        self.notifier = False
        self._paho_mqtt = MQTT.Client("clientid", False)
        self._paho_mqtt.on_connect = self.myOnConnect
        self._paho_mqtt.on_message = self.myOnMessageReceived

    def myOnConnect(self, paho_mqtt, userdata, flags, rc):
        print ("Connected to message broker with result code: " + str(rc))

    def myOnMessageReceived(self, paho_mqtt, userdata, msg):
        print ("Message: "+msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
        self.message = str(msg.payload)
        self.notifier = True

    def myPublish(self, topic, msg, qos = 2):
        self._paho_mqtt.publish(topic, msg, qos)

    def mySubscribe(self, topic, qos = 2):
        self._paho_mqtt.subscribe(topic, qos)

    def start(self):
        self._paho_mqtt.connect(self.broker, self.port)
        self._paho_mqtt.loop_start()

    def stop(self):
        self._paho_mqtt.loop_stop()
