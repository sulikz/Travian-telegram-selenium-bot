from process_wrapper import *


def main():
    farmer_process = ProcessWrapper(farmer, args=('config.ini', 'farm_list.txt', 1800, 4800,))
    farmer_process.start()


if __name__ == '__main__':
    main()
