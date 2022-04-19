from process_wrapper import *


def main():
    # bot = Bot('config.ini')
    # bot.login()
    # bot.read_village_info()
    # dodge = ProcessWrapper(dodge_process)
    # alert = ProcessWrapper(alert_process)
    # alert.start()
    # dodge.start()
    farmer = ProcessWrapper(farming_process)
    farmer.start()

    while True:
        pass


if __name__ == '__main__':
    main()
