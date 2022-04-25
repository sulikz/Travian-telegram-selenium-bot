import re

import requests


class TelegramBot:

    def __init__(self, config):
        self.token = config.get('TELEGRAM', 'token')
        self.chatid = config.get('TELEGRAM', 'chatid')

    def send_telegram_text(self, bot_message):
        send_text = 'https://api.telegram.org/bot' + self.token + '/sendMessage?chat_id=' + self.chatid + '&parse_mode=Markdown&text=' + bot_message
        response = requests.get(send_text)
        return response.json()

    def get_updates(self):
        received = 'https://api.telegram.org/bot' + self.token + '/getUpdates?offset=-1'
        return requests.get(received)

    def get_message_id(self):
        try:
            response = self.get_updates().text
            return int(re.search('(.*"message_id":)(.*)(,"from".*)', response).group(2))
        except AttributeError:
            return 0

    def get_telegram_text(self):
        response = self.get_updates().text
        try:
            return re.search('(.*"text":")(.*)(","entities".*)', response).group(2)
        except AttributeError:
            return ''
