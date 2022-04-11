from configparser import ConfigParser

from webdriver import login

config = ConfigParser()
config.read('config.ini')
email = config.get('USER', 'email')
password = config.get('USER', 'password')
server = config.get('USER', 'server')

login(email, password, server)

while True:
    pass
