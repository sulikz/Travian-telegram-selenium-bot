from travian_webdriver import TravianWebDriver


def main():
    twd = TravianWebDriver('config.ini')
    twd.remove_popups()
    twd.switch_language()
    twd.login()
    while True:
        pass


if __name__ == '__main__':
    main()
