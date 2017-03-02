from telegramBot import TelegramBot
import time

TOKEN = "294196450:AAEv98AIlpUQ9Kb6QXD-RelIr2QVh8PI6YM"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

def handle_updates(bot, updates) :
    for update in updates["result"]:
        text = update["message"]["text"]
        chat = update["message"]["chat"]["id"]
        if text == "/start":
            item = []
            item = ['water Temperature', 'ground Umidity', 'weather information']
            keyboard = Bot.build_keyboard(item)
            bot.send_message("Welcome to your personal SeeUlater_Bot",chat,keyboard)
        elif text == "water Temperature":
            tmp = 20
            text = "the water temperature is %r degree " % tmp
            bot.send_message(text,chat)
        elif text == "ground Umidity":
            tmp = 20
            text = "the water temperature is %r degree " % tmp
            bot.send_message(text,chat)
        elif text == "weather information":
            tmp = 20
            text = "the water temperature is %r degree " % tmp
            bot.send_message(text,chat)
        elif text.startswith("/"):
            continue
        else:
            message = "comando non esistente"
            bot.send_message(message, chat)


Bot = TelegramBot(URL)

#(text_rx,chatID)=Bot.get_last_chat_id_and_text()
#text_tx = "ciao dal bot"
#Bot.send_message(text_tx,chatID)

Bot.prettyprint_json(Bot.get_updates())

last_update_id = None
while True:
    updates = Bot.get_updates(last_update_id)
    Bot.prettyprint_json(updates)
    if len(updates["result"]) > 0:
        last_update_id = Bot.get_last_update_id() + 1
        Bot.prettyprint_json(updates)
        #Bot.send_message("Risposta DEBUG", updates["message"]["chat"]["id"])
        handle_updates(Bot,updates)
    time.sleep(0.5)




#while True:
#    updateID =Bot.get_last_update_id()
#    updates = Bot.get_updates(updateID)
#    if len(updates["result"]) > 0:
#        handle_updates(Bot)
#    time.sleep(0.5)

#Bot.prettyprint_json(Bot.send_message(text_tx,chatID))