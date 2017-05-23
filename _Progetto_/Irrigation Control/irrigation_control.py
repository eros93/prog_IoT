import mqtt_client
import requests
import json
import time

class Irrigation_Control(object):
    """Control checking everyday if it is necessary to irrigate and in case it is
    true it opens the irrigation pump at the right time for the right amount."""

    def __init__(self):
        self.broker = {}
        self.irrigation_time = 0

    def get_broker_infos(self):
        """Gets the broker ip and port through a web request."""
        r = requests.get('http://localhost:8080/res_cat/broker_info')
        infos = json.loads(r.text)
        self.broker['ip'] = infos['broker_ip']
        self.broker['port'] = infos['broker_port']

    def retrieve_broker_infos(self):
        """Retrieves broker information in json format"""
        return self.broker

    def get_weather_and_water_topic(self):
        """Retrieves thresholds for humidity and temperature."""
        r = requests.get('http://localhost:8080/res_cat/all')
        catalog = json.loads(r.text)
        output = {}
        output['weather'] = catalog['weath_mqtt_out_topic']
        output['water'] = catalog['usedwater_topic']
        return output

    def get_device_topic(self, device_name):
        """Retrieves the mqtt topic for a certain device"""
        r = requests.get('http://localhost:8080/res_cat/dev_list')
        devices_list = json.loads(r.text)
        for i in range(len(devices_list)):
            a = devices_list[i]
            if (a['rn'] == device_name):
                return a['mqtt_topic']
        return None

    def mqtt_client_creation(self):
        """Creates an mqtt client object inside the irrigation object."""
        self.mqtt = MQTTClient(self.broker)

#IMPORTANT: TO CHANGE! IRRIGATION NEEDS TO START AT SUNSET TIME
    def start_watering(self, humidity_topic, weather_topic, time_topic, hum_th, temp_th):
        """It's a cycle taking everyday information from the weather forecast,
        checks if there is need to water and retrieves the sunset time for the
        day. If there is need to water, it checks humidity and temperature to
        know the right moment to irrigate."""
        self.mqtt.start()
        #taking the sunset and news about irrigation
        self.mqtt.mySubscribe(weather_topic, 2)
        msg = json.loads(self.mqtt.message)
        self.mqtt.stop()
        watering_flag = msg['watering_flag']
        sunset_time = msg['sunset']
        if watering_flag == True:   # i need to irrigate
            self.mqtt.start()
            self.mqtt.mySubscribe(humidity_topic)
            hum_temp = json.loads(self.mqtt.message)
            self.mqtt.stop()
            counter = 0
            humidity = hum_temp['humidity']
            temperature = hum_temp['temperature']
            if humidity < hum_th:      # i irrigate
                while (temperature < temp_th and c <= 6):    #cycling until reaching the right temperature (or counter goes off)
                    time.sleep(600)  # 10 minutes of pause
                    c = c+1
                    self.mqtt.start()
                    self.mqtt.mySubscribe(humidity_topic)
                    self.mqtt.stop()
                    hum_temp = json.loads(self.mqtt.message)
                    temperature = hum_temp['temperature']
                self.mqtt.start()
                self.mqtt.myPublish('irrigation/control', 'on')
                start = time.time()
                self.mqtt.notifier = False
                while (humidity < hum_th):
                    while self.mqtt.notifier == False:
                        pass
                    self.mqtt.mySubscribe(humidity_topic)
                    hum_temp = json.loads(self.mqtt.message)
                    humidity = hum_temp['humidity']
                    self.mqtt.notifier = False
                self.mqtt.myPublish('irrigation/control', 'off')
                self.mqtt.stop()
                stop = time.time()
                self.irrigation_time = stop - start
        self.mqtt.myPublish(time_topic, str(self.irrigation_time), 2)   # IMPORTANT: time is measured in ticks
        self.mqtt.stop
