import datetime
import multiprocessing
import time

from bot import Bot
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


def farming_process():
    send_telegram_text('Initializing farming process.')
    bot = Bot('config.ini')
    bot.login()
    send_telegram_text('Logged in.')
    bot.load_farm_file('farm_list.txt')
    send_telegram_text('Farm list loaded.')
    send_telegram_text('Farming process enabled.')
    bot.twd.click_buildings()
    bot.twd.click_rally_point()
    for farm in bot.farm_list:
        bot.twd.click_rp_send_troops()
        troops, coords = farm
        send_telegram_text(f'Sending {troops} troops to {coords}')
        bot.twd.send_troops(troops, AttackType.Raid, coords)
        send_telegram_text('Done.')
        if not bot.twd.check_attack_possible():
            send_telegram_text('Unable to send troops.')
            break

    # initialize bot
    # load farm file
    # run raider loop
    pass


def builder_process():
    # #initialize bot
    # load build queue file
    # check resources
    # build next building
    pass


def listener_process():
    # to manage bot through telegram process
    pass
