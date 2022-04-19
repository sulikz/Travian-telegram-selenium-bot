from process_wrapper import *


def main():
    # bot = Bot('config.ini')
    # bot.login()
    # bot.read_village_info()
    alert = ProcessWrapper(alert_process)
    alert.start()
    farmer = ProcessWrapper(farming_process, args=(1800, 5400))
    farmer.start()

    # while True:
    #     pass


if __name__ == '__main__':
    main()
