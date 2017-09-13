import paho.mqtt.client as MQTT

class MQTTClient():
    """It works as an MQTT publisher and subscriber"""

    def __init__(self, clientid, broker, notifier):
        self.broker = broker['ip']
        self.port = broker['port']
        self.message = ''
        
        self.notifier = notifier

        self._paho_mqtt = MQTT.Client(clientid, False)

        self._paho_mqtt.on_connect = self.myOnConnect
        self._paho_mqtt.on_message = self.myOnMessage
        #self._paho_mqtt.on_publish = self.myOnPublish
        #self._paho_mqtt.on_subscribe = self.myOnSubscribe

        return

    def myPublish(self, topic, msg, qos=2):
        #POSSIBLE ERROR-CHECK
        self.msg = msg
        self._paho_mqtt.publish(topic, msg, qos, True)
        return

    def mySubscribe(self, topic, qos=2):
        #POSSIBLE ERROR-CHECK
        self._paho_mqtt.subscribe(topic, qos)

    def myOnConnect(self, paho_mqtt, userdata, flags, rc):
        print ("Connected to message broker with result code: " + str(rc))
        return

    def myOnMessage(self, clientid, userdata, msg):
        self.notifier.notify(msg.topic, msg.payload)
        #print ("\n\tMessage: "+msg.topic+" "+str(msg.qos)+" "+str(msg.payload))

    def myOnSubscribe(self, clientid, userdata, msg, qos):
        print ("Correctly suscribed")
        return

    def myOnPublish(self, clientid, userdata, mid):
        print ("\n\tMessage sent:")
        try:
            print ("\n\t"+self.msg)
        except (TypeError):
            print ("Impossible to publish")
            pass

        self.msg = None
        return

    def start(self):
        self._paho_mqtt.connect(self.broker, self.port)
        self._paho_mqtt.loop_start()
        return

    def stop(self):
        self._paho_mqtt.loop_stop()
        return
