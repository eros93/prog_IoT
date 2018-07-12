# -*- coding: utf-8 -*-

from telegramBot import TelegramBot
from MQTT_pub_sub import MySubscriber
import time
import datetime
import requests
import json
import os


TOKEN = "294196450:AAEdDwOslUfvqvw4uB1ovsDehGtirav0VDY"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
res_cat_ip = "192.168.1.73"
res_cat_port = "8080"

#TODO create a new button for give information on status of tomorrow (rain or not ?)
#and do a function that save the state for today (if rain or not)
#chiedere ad enrico il json giusto



def handle_updates(bot, updates, subscriber, last_update_id) :
    for update in updates["result"]:
        text = update["message"]["text"]
        chat = update["message"]["chat"]["id"]
        item1 = ['Water Temperature', 'Ground Humidity', 'Weather Forecast','Status information','DashBoard', 'Set Thresholds']
        keyboard1 = Bot.build_keyboard(item1)
        item2 =['Moisture [%]', 'Water temperature [C deg]', 'Precipitation intensity [mm/h]', 'Precipitation probability [%]', 'System Informations']
        keyboard2 = Bot.build_keyboard(item2)
        replied_text = None
        if update["message"].has_key("reply_to_message"):
            replied_text = update["message"]["reply_to_message"]["text"]
        if text == "/start":
            bot.send_message("Welcome to your personal SeeUlater_Bot",chat,keyboard1)
        elif text == "Water Temperature":
            text = "Please wait...\nRetrieving information..."
            bot.send_message(text,chat)
            (weather_topic, mqtt_topic, water_topic) = topic_update(res_cat_ip, res_cat_port)
            subscriber.mySubscribe(mqtt_topic[0])
            time.sleep(1)
            obj = subscriber.message
            subscriber.myUnsubscribe(str(mqtt_topic[0]))
            date = datetime.datetime.fromtimestamp(obj["timestamp"]).strftime('%d/%m/%Y %H:%M')
            text = "On %s the water temperature was %r degree " % (str(date), obj["temp"])
            bot.send_message(text,chat,keyboard1)
        elif text == "Ground Humidity":
            text = "Please wait...\nRetrieving information..."
            bot.send_message(text,chat)
            (weather_topic, mqtt_topic, water_topic) = topic_update(res_cat_ip, res_cat_port)
            subscriber.mySubscribe(mqtt_topic[0])
            time.sleep(1)
            obj = subscriber.message
            subscriber.myUnsubscribe(str(mqtt_topic[0]))
            date = datetime.datetime.fromtimestamp(obj["timestamp"]).strftime('%d/%m/%Y %H:%M')
            text = "At %s the ground moisture was %r " % (str(date), obj["hum_gr"]) + "%"
            bot.send_message(text,chat,keyboard1)
        elif text == "Weather Forecast":
            text = "Please wait...\nRetrieving information..."
            bot.send_message(text,chat)
            (weather_topic, mqtt_topic, water_topic) = topic_update(res_cat_ip, res_cat_port)
            subscriber.mySubscribe(weather_topic)
            time.sleep(1)
            obj = subscriber.message
            subscriber.myUnsubscribe(str(weather_topic))
            time_sunset = datetime.datetime.fromtimestamp(obj["sunset"]).strftime('%H:%M')
            time_sunrise = datetime.datetime.fromtimestamp(obj["sunrise"]).strftime('%H:%M')
            text = "The weather forecast for tomorrow:\n- Sunrise will be at %s\n- Sunset will be at %s\n- Precipitation probability is %r\n- Precipitation intensity will be  %r mm\n\nSummary: %s" % (str(time_sunrise),str(time_sunset), obj["precipProb"], obj["precipInt"], str(obj["summary"]))
            bot.send_message(text,chat,keyboard1)
        elif text == "Status information":
            text = "Please wait...\nRetrieving information..."
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
            if os.system("ping -c 1 192.168.1.65") == 0:
                text = "RaspberryPyBOT (192.168.1.65) is up "
            else:
                text = "RaspberryPyBOT (192.168.1.65) is down "
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
            bot.send_message(text,chat,keyboard1)
        elif text == "Freeboard":
            text = "Please wait...\nRetrieving information..."
            bot.send_message(text,chat)
            text = "The Freeboard link is: seeulaterirrigator.hopto.org:1880/freeboard/"+"%23"+"start-79054"
            bot.send_message(text,chat,keyboard1)
        elif text == "Set Thresholds":
            text = "Control Settings \n\nPlease wait...\nRetrieving information... "
            bot.send_message(text,chat)
            ths = get_thresholds(res_cat_ip, res_cat_port)
            message = build_th_message(ths)
            bot.send_message(message,chat,keyboard2)
        elif text == "System Informations":
            text = "System Informations \nWhich information are you looking for ?"
            bot.send_message(text,chat,keyboard1)

        elif text == "Moisture [%]":
            message = "Reply to this message with the new moisture threshold [%]"
            bot.send_message(message, chat)
        elif text == "Precipitation probability [%]":
            message = "Reply to this message with the new precipitation probability threshold [%]"
            bot.send_message(message, chat)
        elif text == "Water temperature [C deg]":
            message = "Reply to this message with the new water temperature threshold [C deg]"
            bot.send_message(message, chat)
        elif text == "Precipitation intensity [mm/h]":
            message = "Reply to this message with the new precipitation intensity threshold [mm/h]"
            bot.send_message(message, chat)

        elif replied_text != None:
            if replied_text == "Reply to this message with the new moisture threshold [%]":
                if is_float(text):
                    if float(text)>= 0.0 and float(text)<= 100.0:
                        # print(text)
                        json_put={}
                        json_put["moisture"] = float(text)
                        res_url = "http://" + res_cat_ip + ":" + res_cat_port + "/res_cat/upd_thresholds"
                        r = requests.put(res_url, json=json_put)
                        print(r.status_code)

                        if r.status_code == 200:
                            message = "The threshold has been correctly updated"
                            bot.send_message(message, chat)
                            ths = get_thresholds(res_cat_ip, res_cat_port)
                            message = build_th_message(ths)
                            bot.send_message(message, chat, keyboard2)
                        else:
                            message = "Error! Please try again in a few minutes..."
                            bot.send_message(message, chat, keyboard2)

                    else:
                        message = "The value must be between 0 and 100, please try again..."
                        bot.send_message(message, chat)
                else:
                    message = "The value must be a number, please try again..."
                    bot.send_message(message, chat)

            elif replied_text == "Reply to this message with the new precipitation probability threshold [%]":
                if is_float(text):
                    if float(text)>= 0.0 and float(text)<= 100.0:
                        # print(text)
                        json_put={}
                        json_put["precipprob"] = float(text)/100.0
                        res_url = "http://" + res_cat_ip + ":" + res_cat_port + "/res_cat/upd_thresholds"
                        r = requests.put(res_url, json=json_put)
                        print(r.status_code)

                        if r.status_code == 200:
                            message = "The threshold has been correctly updated"
                            bot.send_message(message, chat)
                            ths = get_thresholds(res_cat_ip, res_cat_port)
                            message = build_th_message(ths)
                            bot.send_message(message, chat, keyboard2)
                        else:
                            message = "Error! Please try again in a few minutes..."
                            bot.send_message(message, chat, keyboard2)

                    else:
                        message = "The value must be between 0 and 100, please try again..."
                        bot.send_message(message, chat)
                else:
                    message = "The value must be a number, please try again..."
                    bot.send_message(message, chat)

            elif replied_text == "Reply to this message with the new water temperature threshold [C deg]":
                if is_float(text):
                    # print(text)
                    json_put={}
                    json_put["watertemp"] = float(text)
                    res_url = "http://" + res_cat_ip + ":" + res_cat_port + "/res_cat/upd_thresholds"
                    r = requests.put(res_url, json=json_put)
                    print(r.status_code)

                    if r.status_code == 200:
                        message = "The threshold has been correctly updated"
                        bot.send_message(message, chat)
                        ths = get_thresholds(res_cat_ip, res_cat_port)
                        message = build_th_message(ths)
                        bot.send_message(message, chat, keyboard2)
                    else:
                        message = "Error! Please try again in a few minutes..."
                        bot.send_message(message, chat, keyboard2)

                else:
                    message = "The value must be a number, please try again..."
                    bot.send_message(message, chat)

            elif replied_text == "Reply to this message with the new precipitation intensity threshold [mm/h]":
                if is_float(text):
                    # print(text)
                    json_put={}
                    json_put["precipint"] = float(text)
                    res_url = "http://" + res_cat_ip + ":" + res_cat_port + "/res_cat/upd_thresholds"
                    r = requests.put(res_url, json=json_put)
                    print(r.status_code)

                    if r.status_code == 200:
                        message = "The threshold has been correctly updated"
                        bot.send_message(message, chat)
                        ths = get_thresholds(res_cat_ip, res_cat_port)
                        message = build_th_message(ths)
                        bot.send_message(message, chat, keyboard2)
                    else:
                        message = "Error! Please try again in a few minutes..."
                        bot.send_message(message, chat, keyboard2)

                else:
                    message = "The value must be a number, please try again..."
                    bot.send_message(message, chat)

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

def get_thresholds (res_cat_ip, res_cat_port):
    res_url = "http://" + res_cat_ip + ":" + res_cat_port + "/res_cat/all"
    response_res_cat = requests.get(res_url)
    obj = json.loads(response_res_cat.text)
    moist_th = obj["moisture_thresh"]
    water_temp_th = obj["watertemp_thresh"]
    int_prec_th = obj["precipintensity_thresh"]
    prob_prec_th = obj["precipprobability_thresh"]
    th = {"moist_th": moist_th, "water_temp_th": water_temp_th, "int_prec_th": int_prec_th, "prob_prec_th": prob_prec_th}
    return th

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
def build_th_message(ths):
    text = """The current thresholds are:\n
Moisture = %s [%%]
Water temperature = %s [°C]
Precipitation intensity = %s [mm/h]
Precipitation probability = %s [%%]\n
Select a threshold to change the value:""" %(ths['moist_th'], ths['water_temp_th'], ths['int_prec_th'], str(float(ths['prob_prec_th'])*100))
    return text

Bot = TelegramBot(URL)

(broker_ip, broker_port) = broker_info(res_cat_ip, res_cat_port)

sub = MySubscriber("Botsub")
sub.start(broker_ip, broker_port)

last_update_id = None
while True:
### try to avoid Exception given from bad answer from Telegram APIs       

    try:
        updates = Bot.get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = Bot.get_last_update_id() + 1
            handle_updates(Bot, updates, sub, last_update_id)
            #Bot.prettyprint_json(updates)
        time.sleep(0.5)
    except Exception as e:
        print(e)
        time.sleep(0.5)
        continue
                  
        
