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


def notifier(config_file):
    """
    Notifies user through Telegram messages about:
    -incoming attacks
    -available adventures if hero is in the village
    -empty building queue status
    Parameters
    ----------
    config_file

    Returns
    -------

    """

    attack_notification_sent = False
    adventure_notification_sent = False
    building_notification_sent = False
    telebot = TelegramBot(config_file)
    bot = Bot(config_file)
    bot.login()
    telebot.send_telegram_text(f'Telegram notifier enabled. \n Logged into {bot.server}.')
    while True:
        # Check incoming attacks
        incoming_attack_time = bot.check_attack()
        if incoming_attack_time != 0 and not attack_notification_sent:
            telebot.send_telegram_text(f'Incoming attack in {str(datetime.timedelta(seconds=incoming_attack_time))}')
            attack_notification_sent = True
        # Wait for the attack to pass so the new one will be detected
        if incoming_attack_time < 30 and attack_notification_sent:
            attack_notification_sent = False
            time.sleep(30)
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


def farmer(config_file, farm_file, min_sleep_time, max_sleep_time):
    """
    Raids destinations specified in farm_file. Shuffles raid list each time farmer is initialized for more random
    behavior. Skips destination if unable to attack. If there are not enough troops function sleeps for random
    <min_sleep_time, max_sleep_time> [s].
    Parameters
    ----------
    farm_file
    config_file
    min_sleep_time
    max_sleep_time

    Returns
    -------

    """
    telebot = TelegramBot(config_file)
    bot = Bot(config_file)
    bot.login()
    bot.load_farm_file(farm_file)
    telebot.send_telegram_text('Farming process enabled. \n Logged into {bot.server}.')
    random.shuffle(bot.farm_list)
    # Enter rally point
    bot.twd.click_buildings()
    bot.twd.click_rally_point()
    while True:
        for destination in bot.farm_list:
            # Unpack troops
            troops, coords = destination
            # Send troops to coordinates
            sleep_random(0, 1)
            bot.twd.click_rp_send_troops()
            sleep_random(0, 1)
            enough_troops = bot.send_troops(troops, AttackType.Raid, coords)
            if not bot.twd.check_attack_possible():
                telebot.send_telegram_text(f'Unable to send troops to {coords}')
            if not enough_troops:
                telebot.send_telegram_text(f'Not enough troops. Sleeping...')
                sleep_random(min_sleep_time, max_sleep_time)
                bot.twd.driver.refresh()


def builder():
    # #initialize bot
    # load build queue file
    # check resources
    # build next building
    pass


def listener():
    # to manage bot through telegram process
    pass

# def dodger():
#     bot = Bot('config.ini')
#     bot.login()
#     send_telegram_text('Dodge attacks enabled.')
#     while True:
#         incoming_attack_time = bot.check_attack()
#         if incoming_attack_time < 3:
#             bot.twd.send_troops()
#             # dodge_attack
#             pass
