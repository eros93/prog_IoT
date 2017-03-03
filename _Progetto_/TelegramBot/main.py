from telegramBot import TelegramBot
from MQTT_pub_sub import MySubscriber
import time
import datetime
import requests
import json

TOKEN = "294196450:AAEv98AIlpUQ9Kb6QXD-RelIr2QVh8PI6YM"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
res_cat_ip = "192.168.1.70"
res_cat_port = "8080"



def handle_updates(bot, updates, subscriber) :
    for update in updates["result"]:
        text = update["message"]["text"]
        chat = update["message"]["chat"]["id"]
        item = ['Water Temperature', 'Ground Humidity', 'Weather Forecast']
        keyboard = Bot.build_keyboard(item)
        if text == "/start":
            bot.send_message("Welcome to your personal SeeUlater_Bot",chat,keyboard)
        elif text == "Water Temperature":
            text = "Please wait....\nRetrieving information...."
            bot.send_message(text,chat)
            (weather_topic, mqtt_topic) = topic_update(res_cat_ip, res_cat_port)
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
            (weather_topic, mqtt_topic) = topic_update(res_cat_ip, res_cat_port)
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
            (weather_topic, mqtt_topic) = topic_update(res_cat_ip, res_cat_port)
            subscriber.mySubscribe(weather_topic)
            time.sleep(1)
            obj = subscriber.message
            subscriber.myUnsubscribe(str(weather_topic))
            time_sunset = datetime.datetime.fromtimestamp(obj["sunset"]).strftime('%H:%M')
            time_sunrise = datetime.datetime.fromtimestamp(obj["sunrise"]).strftime('%H:%M')
            text = "The weather forecast for tomorrow:\n- Sunrise will be at %s\n- Sunset will be at %s\n- Precipitation probability is %r\n- Precipitation intensity will be is %r mm\n\nSummary: %s" % (str(time_sunrise),str(time_sunset), obj["precipProb"], obj["precipInt"], str(obj["summary"]))
            bot.send_message(text,chat,keyboard)
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
    int = len(obj["dev_list"])
    mqtt_topic = []
    for i in range(int):
        if obj["dev_list"][i]["mqtt_role"] == "p":
            mqtt_topic.append(obj["dev_list"][i]["mqtt_topic"])
    return weather_topic, mqtt_topic


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



