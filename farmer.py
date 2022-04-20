from process_wrapper import *


def main():
    farmer_process = ProcessWrapper(farmer, args=('farm_list.txt', 1800, 5400,))
    farmer_process.start()


if __name__ == '__main__':
    main()
