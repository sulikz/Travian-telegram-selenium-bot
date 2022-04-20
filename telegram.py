from configparser import ConfigParser

import requests


class TelegramBot:
    config = ConfigParser()

    def __init__(self, config_file):
        self.config.read(config_file)
        self.token = self.config.get('TELEGRAM', 'token')
        self.chatid = self.config.get('TELEGRAM', 'chatid')

    def send_telegram_text(self, bot_message):
        send_text = 'https://api.telegram.org/bot' + self.token + '/sendMessage?chat_id=' + self.chatid + '&parse_mode=Markdown&text=' + bot_message
        response = requests.get(send_text)
        return response.json()
