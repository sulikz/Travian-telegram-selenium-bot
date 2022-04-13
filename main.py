from configparser import ConfigParser

from travian_webdriver import login


def main():
    config = ConfigParser()
    config.read('config.ini')
    email = config.get('USER', 'email')
    password = config.get('USER', 'password')
    server = config.get('USER', 'server')

    login(email, password, server)
    while True:
        pass


if __name__ == '__main__':
    main()
