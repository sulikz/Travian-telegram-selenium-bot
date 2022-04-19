import requests


def send_telegram_text(bot_message):
    bot_token = '5333694606:AAFisDSoeKLk0pgnrH9Vhkaq4zp8ZKkoIxM'
    bot_chatID = '1406431884'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()
