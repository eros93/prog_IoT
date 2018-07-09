from telegramBot import TelegramBot
from MQTT_pub_sub import MySubscriber
import time
import datetime
import requests
import json
import os

TOKEN = "294196450:AAEv98AIlpUQ9Kb6QXD-RelIr2QVh8PI6YM"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
res_cat_ip = "192.168.1.73"
res_cat_port = "8080"

#TODO create a new button for give information on status of tomorrow (rain or not ?)
#and do a function that save the state for today (if rain or not)
#chiedere ad enrico il json giusto



def handle_updates(bot, updates, subscriber) :
    for update in updates["result"]:
        text = update["message"]["text"]
        chat = update["message"]["chat"]["id"]
        item = ['Water Temperature', 'Ground Humidity', 'Weather Forecast','Status information','Freeboard']
        keyboard = Bot.build_keyboard(item)
        if text == "/start":
            bot.send_message("Welcome to your personal SeeUlater_Bot",chat,keyboard)
        elif text == "Water Temperature":
            text = "Please wait....\nRetrieving information...."
            bot.send_message(text,chat)
            (weather_topic, mqtt_topic, water_topic) = topic_update(res_cat_ip, res_cat_port)
            subscriber.mySubscribe(mqtt_topic[0])
            time.sleep(1)
            obj = subscriber.message
            subscriber.myUnsubscribe(str(mqtt_topic[0]))
            date = datetime.datetime.fromtimestamp(obj["timestamp"]).strftime('%d/%m/%Y %H:%M')
            text = "On %s the water temperature was %r degree " % (str(date), obj["temp"])
            bot.send_message(text,chat,keyboard)
        elif text == "Ground Humidity":
            text = "Please wait....\nRetrieving information...."
            bot.send_message(text,chat)
            (weather_topic, mqtt_topic, water_topic) = topic_update(res_cat_ip, res_cat_port)
            subscriber.mySubscribe(mqtt_topic[0])
            time.sleep(1)
            obj = subscriber.message
            subscriber.myUnsubscribe(str(mqtt_topic[0]))
            date = datetime.datetime.fromtimestamp(obj["timestamp"]).strftime('%d/%m/%Y %H:%M')
            text = "At %s the ground moisture was %r " % (str(date), obj["hum_gr"]) + "%"
            bot.send_message(text,chat,keyboard)
        elif text == "Weather Forecast":
            text = "Please wait....\nRetrieving information...."
            bot.send_message(text,chat)
            (weather_topic, mqtt_topic, water_topic) = topic_update(res_cat_ip, res_cat_port)
            subscriber.mySubscribe(weather_topic)
            time.sleep(1)
            obj = subscriber.message
            subscriber.myUnsubscribe(str(weather_topic))
            time_sunset = datetime.datetime.fromtimestamp(obj["sunset"]).strftime('%H:%M')
            time_sunrise = datetime.datetime.fromtimestamp(obj["sunrise"]).strftime('%H:%M')
            text = "The weather forecast for tomorrow:\n- Sunrise will be at %s\n- Sunset will be at %s\n- Precipitation probability is %r\n- Precipitation intensity will be  %r mm\n\nSummary: %s" % (str(time_sunrise),str(time_sunset), obj["precipProb"], obj["precipInt"], str(obj["summary"]))
            bot.send_message(text,chat,keyboard)
        elif text == "Status information":
            text = "Please wait....\nRetrieving information...."
            bot.send_message(text,chat)
            if os.system("ping -c 1 192.168.1.100") == 0:
                text = "RaspberryPy2 (192.168.1.100) is up "
            else:
                text = "RaspberryPy2 (192.168.1.100) is down "
            bot.send_message(text,chat)
            if os.system("ping -c 1 192.168.1.151") == 0:
                text = "RaspberryPy3 (192.168.1.151) is up "
            else:
                text = "RaspberryPy3 (192.168.1.151) is down "
            bot.send_message(text,chat)
            if os.system("ping -c 1 192.168.1.66") == 0:
                text = "RaspberryPyBOT (192.168.1.66) is up "
            else:
                text = "RaspberryPyBOT (192.168.1.66) is down "
            bot.send_message(text,chat)
            if os.system("ping -c 1 192.168.1.10") == 0:
                text = "Arduino (192.168.1.10) is up "
            else:
                text = "Arduino (192.168.1.10) is down "
            bot.send_message(text,chat)

            (weather_topic, mqtt_topic, water_topic) = topic_update(res_cat_ip, res_cat_port)
            subscriber.mySubscribe(str(weather_topic))
            time.sleep(1)
            obj_weather = subscriber.message
            subscriber.myUnsubscribe(str(weather_topic))
            subscriber.mySubscribe(str(water_topic))
            time.sleep(1)
            obj_water = subscriber.message
            subscriber.myUnsubscribe(str(water_topic))
            #date = datetime.datetime.fromtimestamp(obj["timestamp"]).strftime('%d/%m/%Y %H:%M')
            #TODO watering topic to finisch -> ask to federica and obj_weather return TRUE -> so make an if to make the correct string
            #text = " Tomorrow the system will be %s , water consumption is about %s " % (obj_weather["watering_flag"], obj_water[""])
            if obj_weather["watering_flag"] == True:
                text = "Tomorrow watering process is needed. "
            else:
                text = "Tomorrow watering process is NOT needed. "  

            time_water_open = obj_water
            consumption_liter = time_water_open * 0.028
            text += "\nThe water consumption was about %s liters. " % str(round(consumption_liter,2))
            bot.send_message(text,chat,keyboard)
        elif text == "Freeboard":
            text = "Please wait....\nRetrieving information...."
            bot.send_message(text,chat)
            text = "The Freeboard link is: seeulaterirrigator.hopto.org:1880/freeboard/"+"%23"+"start-79054"
            bot.send_message(text,chat,keyboard)

        # elif text == "Status information":
        #     text = "Please wait....\nRetrieving information...."
        #     bot.send_message(text,chat)
        #     (weather_topic, mqtt_topic) = topic_update(res_cat_ip, res_cat_port)
        #     subscriber.mySubscribe(mqtt_topic[0])
        #     time.sleep(1)
        #     obj = subscriber.message
        #     subscriber.myUnsubscribe(str(mqtt_topic[0]))
        #     date = datetime.datetime.fromtimestamp(obj["timestamp"]).strftime('%d/%m/%Y %H:%M')
        #     text = " The System is ON \n The water consumtion was about %s \n tomorrow the irrigation system will be %s " % (obj["water_topic"], obj["out_pump"]) #CHIEDERE i topic corretti per la pompa e il consumo dell acqua
        #     bot.send_message(text,chat,keyboard)
        elif text.startswith("/"):
            continue
        else:
            message = "Not valid Command"
            bot.send_message(message, chat)
def broker_info (res_cat_ip, res_cat_port):
    res_url = "http://" + res_cat_ip + ":" + res_cat_port + "/res_cat/broker_info"
    response_res_cat = requests.get(res_url)
    obj = json.loads(response_res_cat.text)
    broker_ip = obj["broker_ip"]
    broker_port = obj["broker_port"]
    return broker_ip, broker_port


def topic_update (res_cat_ip, res_cat_port):
    res_url = "http://" + res_cat_ip + ":" + res_cat_port + "/res_cat/all"
    response_res_cat = requests.get(res_url)
    obj = json.loads(response_res_cat.text)
    weather_topic = obj["weath_mqtt_out_topic"]
    water_topic = obj["usedwater_topic"]
    int = len(obj["dev_list"])
    mqtt_topic = []
    for i in range(int):
        if obj["dev_list"][i]["mqtt_role"] == "p":
            mqtt_topic.append(obj["dev_list"][i]["mqtt_topic"])
    return weather_topic, mqtt_topic, water_topic


Bot = TelegramBot(URL)

(broker_ip, broker_port) = broker_info(res_cat_ip, res_cat_port)

sub = MySubscriber("Botsub")
sub.start(broker_ip, broker_port)

last_update_id = None
while True:
    updates = Bot.get_updates(last_update_id)
    if len(updates["result"]) > 0:
        last_update_id = Bot.get_last_update_id() + 1
        #Bot.prettyprint_json(updates)
        handle_updates(Bot, updates, sub)
    time.sleep(0.5)
