from irrigation_control import Irrigation_Control
from datetime import datetime
import schedule
import time


irrigation = Irrigation_Control()   # creation of the irrigation control object

def irrigation_routine():
    print ("Irrigation routine started at %s" %time.strftime("%H:%M"))
    irrigation.get_broker_infos()       # get all the infos about the broker
    irrigation.mqtt_client_creation()   # creation of the mqtt publisher and subscriber
    weather_time = irrigation.get_weather_and_water_topic()
    weather_topic = weather_time['weather']
    time_topic = weather_time['water']
    hum_th = weather_time['moisture']    # ground humidity threshold
    temp_th = weather_time['water_temp']   # water temperature threshold
    humtemp_topic = irrigation.get_device_topic('ard1')
    irrigation.pump_topic = irrigation.get_device_topic('pump1')
    irrigation.start_watering(humtemp_topic, weather_topic, time_topic, hum_th, temp_th)
    
    schedule.clear()
    schedule.every().day.at(irrigation.sunset_time).do(irrigation_routine)
    print "RE-schedule.every().day.at(%s).do(irrigation_routine)" %irrigation.sunset_time

    return


if  __name__ == "__main__":

    irrigation_routine()    #DEBUG

    while True:
        schedule.run_pending()
        time.sleep(60)
