from mqtt_client import MQTTClient
import requests
import json
import time
import datetime

class Irrigation_Control(object):
    """Control checks if it is necessary to irrigate and in case it is
    true it opens the irrigation pump at the right time for how much time it is needed."""

    def __init__(self, rcip, rcport):
        
        # NEW ###################
        self.rescatip = rcip
        self.rescatport = rcport
        #########################
        
        self.broker = {}
        self.irrigation_time = 0.0
        self.pump_topic = ''
        self.watering_flag = False
        self.sunset_time = '18:00'
        self.humidity = 0.0
        self.temperature = 0.0
        self.weather_topic = ''
        self.humtemp_topic = ''
        self.hum_th = 0.0
        self.temp_th = 0.0

    def get_broker_infos(self):
        """Gets the broker ip and port through a web request."""
        #print "I'm in get_broker_infos"

        r = requests.get('http://'+self.rescatip+':'+str(self.rescatport)+'/res_cat/broker_info')
        # r = requests.get('http://192.168.1.71:8080/res_cat/broker_info')
        infos = json.loads(r.text)
        self.broker['ip'] = infos['broker_ip']
        self.broker['port'] = infos['broker_port']

    def get_weather_and_water_topic(self):
        """Retrieves thresholds for humidity and temperature."""
        #print "I'm in get_weather_and_water_topic"

        r = requests.get('http://'+self.rescatip+':'+str(self.rescatport)+'/res_cat/all')
        # r = requests.get('http://192.168.1.71:8080/res_cat/all')
        catalog = json.loads(r.text)
        output = {}
        output['weather'] = catalog['weath_mqtt_out_topic']
        output['water'] = catalog['usedwater_topic']
        output['moisture'] = catalog['moisture_thresh']
        output['water_temp'] = catalog['watertemp_thresh']
        return output

    def get_device_topic(self, device_name):
        """Retrieves the mqtt topic for a certain device"""
        #print "I'm in get_device_topic"

        r = requests.get('http://'+self.rescatip+':'+str(self.rescatport)+'/res_cat/dev_list')
        # r = requests.get('http://192.168.1.71:8080/res_cat/dev_list')
        devices_list = json.loads(r.text)
        for i in range(len(devices_list)):
            a = devices_list[i]
            if (a['rn'] == device_name):
                return a['mqtt_topic']
        return None

    def mqtt_client_creation(self):
        """Creates an mqtt client object inside the irrigation object."""
        #print "I'm in mqtt_client_creation"
        self.mqtt = MQTTClient("irrigation", self.broker, self)

    def notify(self, topic, payload):
        """Function called every time that a message is received as subscriber"""

        print ("Notify function on topic: "+topic)
        if (topic == self.weather_topic):
            # print "I'm in notify topic weather"
            msg = json.loads(payload)
            
            self.watering_flag = False
            if (msg["watering_flag"]=="True"):
                self.watering_flag = True
                self.sunset_time = datetime.datetime.fromtimestamp(int(msg['sunset'])).strftime('%H:%M')    # from unix timestamp --> format h:m
                #self.sunset_time = msg['sunset']   # only unix timestamp
                #print self.sunset_time
                time.sleep(5)
            else:
                self.watering_flag = False
                self.sunset_time = datetime.datetime.fromtimestamp(int(msg['sunset'])).strftime('%H:%M')    # from unix timestamp --> format h:m
                time.sleep(5)

        elif (topic == self.humtemp_topic):
            # update the ground humidity and water temperature measurements
            hum_temp = json.loads(payload)
            self.humidity = hum_temp['hum_gr']
            #print self.humidity
            self.temperature = hum_temp['temp']
            #print self.temperature

    def start_watering(self, humtemp_topic, weather_topic, time_topic, hum_th, temp_th):
        """It's a function which checks if there is need to water. If there is need to water, it checks humidity
        and temperature to know the right moment to irrigate, then it acts on irrigation pump.
        Moreover it measures how much the watering has lasted."""

        #print "I'm in start_watering"
        self.weather_topic = weather_topic
        self.humtemp_topic = humtemp_topic

        self.mqtt.start()

        self.mqtt.mySubscribe(weather_topic, 2)
        time.sleep(10)
        try:
            self.mqtt.mySubscribe(humtemp_topic, 2)
            time.sleep(10)
        except (ValueError):
            print "\"No topic specified for moisture and water temperature, or incorrect topic type.\""
            print "out_pump is set OFF"
            self.mqtt.myPublish(self.pump_topic, 'OFF')
            return

        print "out_pump is set OFF at beginning"
        self.mqtt.myPublish(self.pump_topic, 'OFF')
        if self.watering_flag == True:    #irrigation possible based on weather forecasts
            print "watering flag TRUE"
            c = 0
            start_flag = True   # to start the timecounter only once
            while self.humidity < hum_th:     # check periodically the moisture
                print "moisture (%s%%) is too low (th = %s)" %(str(self.humidity), str(hum_th))
                # wait for temperature reaches threshold or or counter goes off = 1 hr
                if (self.temperature < temp_th and c <= 6):
                    print "water temperature (%s) not yet ready to irrigate (th = %s)" %(str(self.temperature), str(hum_th))
                    time.sleep(600)  # 10 min
                    c = c+1
                elif (start_flag == True):
                    print "water is OK so out_pump is set ON"
                    self.mqtt.myPublish(self.pump_topic, 'ON')
                    #self.mqtt.myPublish("actuator/subnet/1/out_pump", 'ON')
                    start = time.time()
                    start_flag = False
                else:
                    print "wait 100 sec to check again the measured ground humidity" #DEBUG
                    time.sleep(100) #DEBUG
                    #print "wait 5 min to check again the measured ground humidity"
                    #time.sleep(300)     # wait 5 min to compare the measured ground humidity
            # humidity threshold reached so the irrigation pump os switched off
            print "out_pump is set OFF"
            self.mqtt.myPublish(self.pump_topic, 'OFF')
            #self.mqtt.myPublish("actuator/subnet/1/out_pump", 'OFF')
            stop = time.time()
            try:
                self.irrigation_time = stop - start
                try:
                    self.mqtt.myPublish(time_topic, str(self.irrigation_time), retain=True)   # IMPORTANT: time is measured in ticks
                    print ("watering duration "+str(self.irrigation_time))
                except (TypeError):
                    print ("Impossible to publish on "+time_topic)
                    pass
            except (UnboundLocalError):
                print "Time of start not exists because irrigation doesn't even start today"
                pass
            self.mqtt.stop()
        else:
            print "watering flag FALSE --> DO NOTHING"
        
        return