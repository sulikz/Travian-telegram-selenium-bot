from bot import Bot


def main():
    bot = Bot('config.ini', 'farm_list.txt', 'build_queue.txt')
    bot.get_village_info()
    while True:
        pass


if __name__ == '__main__':
    main()
