import datetime
import multiprocessing
import random
import time

from bot import Bot, sleep_random
from enums import AttackType
from telegram import send_telegram_text


class ProcessWrapper:

    def __init__(self, target, args=tuple()):
        self.p = None
        self.target = None
        self.args = tuple()
        self.is_running = False
        self.target = target
        self.args = args

    def start(self):
        if not self.is_running:
            self.p = multiprocessing.Process(target=self.target, args=self.args)
            self.p.start()
            self.is_running = True

    def terminate(self):
        self.p.terminate()
        self.is_running = False


def alert_process():
    send_telegram_text('Initializing attack notifications.')
    bot = Bot('config.ini')
    bot.login()
    send_telegram_text('Incoming attack notifications enabled.')
    while True:
        incoming_attack_time = bot.check_attack()
        if incoming_attack_time != 0:
            send_telegram_text(f'Incoming attack in {str(datetime.timedelta(seconds=incoming_attack_time))}')
            # Wait for the incoming attack
            time.sleep(incoming_attack_time)


# Necessary??
# def dodge_process():
#     bot = Bot('config.ini')
#     bot.login()
#     send_telegram_text('Dodge attacks enabled.')
#     while True:
#         incoming_attack_time = bot.check_attack()
#         if incoming_attack_time < 3:
#             bot.twd.send_troops()
#             # dodge_attack
#             pass


def farming_process(min_sleep_time, max_sleep_time):
    send_telegram_text('Initializing farming process.')
    bot = Bot('config.ini')
    bot.login()
    bot.load_farm_file('farm_list.txt')
    send_telegram_text(f'Farm list loaded. {bot.farm_list}')
    send_telegram_text('Farming process enabled.')
    random.shuffle(bot.farm_list)
    bot.twd.click_buildings()
    bot.twd.click_rally_point()
    while True:
        enough_troops = False
        for destination in bot.farm_list:
            # Unpack troops
            troops, coords = destination
            # enter rally point
            sleep_random(0, 1)
            bot.twd.click_rp_overview()
            sleep_random(0, 1)
            bot.twd.click_stationary_troops_filter()
            while not enough_troops:
                bot.read_army()
                # Get current troops
                # bot.read_troops()
                # If not enough troops -> sleep
                temp_list = []
                for i, _ in enumerate(bot.farm_list):
                    temp_list.append(bot.stationary_troops[i] - troops[i])
                if any(f < 0 for f in temp_list):
                    send_telegram_text(f'Not enough troops. Sleeping...')
                    sleep_random(min_sleep_time, max_sleep_time)
                else:
                    enough_troops = True
            # Send troops to coordinates
            # bot.twd.click_buildings()
            # sleep_random(0, 1)
            # bot.twd.click_rally_point()
            sleep_random(0, 1)
            bot.twd.click_rp_send_troops()
            sleep_random(0, 1)
            send_telegram_text(f'Sending {troops} troops to {coords}')
            bot.send_troops(troops, AttackType.Raid, coords)
            if not bot.twd.check_attack_possible():
                enough_troops = False
                send_telegram_text('Unable to send troops.')


def builder_process():
    # #initialize bot
    # load build queue file
    # check resources
    # build next building
    pass


def listener_process():
    # to manage bot through telegram process
    pass
