import json
import requests

class TelegramBot():


    def __init__(self,url):
        self.url=url

    def get_me(self):
        url_get = self.url + "getme"
        js = get_json_from_url(url_get)
        # prettyprint_json(js)
        return js


    def prettyprint_json(self,js):
        print json.dumps(js, sort_keys=True, indent=4, separators=(',', ': '))
        return

    def get_updates(self, offset=None):
        url_req = self.url + "getUpdates?timeout=1"
        if offset:
            url_req += "&offset={}".format(offset)
        self.updates = get_json_from_url(url_req)
        #    print prettyprint_json(js)
        return self.updates

    def get_last_chat_id_and_text(self):
        self.get_updates()
        num_updates = len(self.updates["result"])
        last_update = num_updates - 1  # perche abbiamo la numerazione da 0
        text = self.updates["result"][last_update]["message"]["text"]
        chat_id = self.updates["result"][last_update]["message"]["chat"]["id"]
        # print (text,chat_id)
        return (text, chat_id)

    def send_message(self,text, chat_id, reply_markup=None):
        url_req = self.url + "sendMessage?text={}&chat_id={}".format(text, chat_id)
        if reply_markup:
            url_req += "&reply_markup={}".format(reply_markup)
        return get_json_from_url(url_req)

    def get_last_update_id(self):
        self.get_updates()
        update_ids = []
        for update in self.updates["result"]:
            update_ids.append(int(update["update_id"]))
        return max(update_ids)

    def build_keyboard(self,items):
        keyboard = [[item] for item in items]
        reply_markup = {"keyboard": keyboard, "one_time_keyboard": True}
        return json.dumps(reply_markup)



def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


