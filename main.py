from process_wrapper import *


def main():
    alert = ProcessWrapper(notification_process, args=('config.ini',))
    alert.start()
    # farmer = ProcessWrapper(farming_process, args=(1800, 5400))
    # farmer.start()

    # while True:
    #     pass


if __name__ == '__main__':
    main()
