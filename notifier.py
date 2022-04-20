from process_wrapper import *


def main():
    notifier_process = ProcessWrapper(notifier, args=('config.ini',))
    notifier_process.start()


if __name__ == '__main__':
    main()
