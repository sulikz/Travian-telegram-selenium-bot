import datetime
import multiprocessing
import random
import time

from bot import Bot, sleep_random
from enums import AttackType
from telegram import TelegramBot


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


def notification_process(config_file):
    attack_notification_sent = False
    adventure_notification_sent = False
    building_notification_sent = False
    telebot = TelegramBot(config_file)
    bot = Bot(config_file)
    bot.login()
    telebot.send_telegram_text('Telegram notifications enabled.')
    while True:
        # Check incoming attacks
        incoming_attack_time = bot.check_attack()
        if incoming_attack_time != 0 and not attack_notification_sent:
            telebot.send_telegram_text(f'Incoming attack in {str(datetime.timedelta(seconds=incoming_attack_time))}')
            attack_notification_sent = True
        # Wait for the attack to pass so the new one will be detected
        if incoming_attack_time < 5 and attack_notification_sent:
            attack_notification_sent = False
            time.sleep(5)
        # Check adventure
        hero_in_village = bot.twd.check_hero()
        adventure_available = bot.twd.check_adventure()
        if hero_in_village and adventure_available and not adventure_notification_sent:
            telebot.send_telegram_text(f'Hero is in the village and adventure is available.')
            adventure_notification_sent = True
        if adventure_notification_sent and not hero_in_village:
            adventure_notification_sent = False
        # Check building queue
        is_being_built = bot.twd.check_if_building()
        if not is_being_built and not building_notification_sent:
            telebot.send_telegram_text(f'Building queue free. Resources in the village: {bot.twd.get_resources()}')
            building_notification_sent = True
        if building_notification_sent and is_being_built:
            building_notification_sent = False


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


def farming_process(config_file, min_sleep_time, max_sleep_time):
    telebot = TelegramBot(config_file)
    telebot.send_telegram_text('Initializing farming process.')
    bot = Bot(config_file)
    bot.login()
    bot.load_farm_file('farm_list.txt')
    telebot.send_telegram_text(f'Farm list loaded. {bot.farm_list}')
    telebot.send_telegram_text('Farming process enabled.')
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
                # If not enough troops -> sleep
                temp_list = []
                for i, _ in enumerate(bot.farm_list):
                    temp_list.append(bot.stationary_troops[i] - troops[i])
                if any(f < 0 for f in temp_list):
                    telebot.send_telegram_text(f'Not enough troops. Sleeping...')
                    sleep_random(min_sleep_time, max_sleep_time)
                else:
                    enough_troops = True
            # Send troops to coordinates
            sleep_random(0, 1)
            bot.twd.click_rp_send_troops()
            sleep_random(0, 1)
            bot.send_troops(troops, AttackType.Raid, coords)
            if not bot.twd.check_attack_possible():
                enough_troops = False
                telebot.send_telegram_text(f'Unable to send troops to {coords}')


def builder_process():
    # #initialize bot
    # load build queue file
    # check resources
    # build next building
    pass


def listener_process():
    # to manage bot through telegram process
    pass
