import time

from webdriver import login
from configparser import ConfigParser


config = ConfigParser()
config.read('config.ini')
email = config.get('USER', 'email')
password = config.get('USER', 'password')
server = config.get('USER', 'server')

login(email, password, server)
