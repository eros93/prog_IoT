import irrigation_control
from datetime import datetime
import schedule

def do_this():
    irrigation = Irrigation_Control()   # creation of the irrigation control
    irrigation.get_broker_infos()       # get all the infos about the broker
    irrigation.mqtt_client_creation()   # creation of the mqtt publisher and subscriber
    weather_time = irrigation.get_weather_and_water_topic()
    weather_topic = weather_time['weather']
    time_topic = weather_time['water']
    humidity_topic = irrigation.get_device_topic('ard1')
    irrigation.start_watering(humidity_topic, weather_topic, time_topic, hum_th, temp_th)

hum_th = 0.3            # humidity threshold
temp_th = 10            # temperature threshold
total_days = 100        # for simplicity: how many days I want to keep the program running

# x=date.today()
# c = 0
# while c < total_days:
#     y=x.replace(day=x.day+1, hour=12)    # tomorrow at 12.00
#     delta_t=y-x
#     secs=delta_t.seconds+1
#     t = Timer(secs, do_this)
#     t.start()
#     c = c+1
#     x = datetime.today()

do_this()

schedule.every().day.at("12:00").do(do_this)
while True:
    schedule.run_pending()
    time.sleep(10)
