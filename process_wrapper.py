import datetime
import multiprocessing
import random
import sys
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


def notifier(config):
    """
    Notifies user through Telegram messages about:
    -incoming attacks
    -available adventures if hero is in the village
    -empty building queue status
    Parameters
    ----------
    config

    Returns
    -------

    """

    attack_notification_sent = False
    adventure_notification = False
    building_notification_ = False
    wood_notificaton = False
    clay_notification = False
    iron_notification = False
    crop_notification = False
    telebot = TelegramBot(config)
    last_msg_id = telebot.get_message_id()
    bot = Bot(config)
    last_msg_id = check_termination(bot, telebot, '/notifier', last_msg_id)
    bot.login()

    while True:
        last_msg_id = check_termination(bot, telebot, '/notifier', last_msg_id)
        r = random.randint(1, 100000)
        if r == 50:
            bot.twd.driver.refresh()
        # Check incoming attacks
        incoming_attack_time = bot.twd.get_first_incoming_attack_time()
        if incoming_attack_time != 0 and not attack_notification_sent:
            telebot.send_telegram_text(f'Incoming attack in {str(datetime.timedelta(seconds=incoming_attack_time))}')
            attack_notification_sent = True
        # Wait for the attack to pass so the new one will be detected
        if incoming_attack_time < 15 and attack_notification_sent:
            attack_notification_sent = False
            time.sleep(15)
        # Check adventure
        hero_in_village = bot.twd.check_hero()
        adventure_available = bot.twd.check_adventure()
        if hero_in_village and adventure_available and not adventure_notification:
            telebot.send_telegram_text(f'Hero adventure is available.')
            adventure_notification = True
        if adventure_notification and not hero_in_village:
            adventure_notification = False
        # Check building queue
        is_being_built = bot.twd.is_built()
        if not is_being_built and not building_notification_:
            telebot.send_telegram_text(f'Building queue free. Resources in the village: {bot.twd.get_resources()}')
            building_notification_ = True
        if building_notification_ and is_being_built:
            building_notification_ = False
        # Check if storage is almost full
        bot.read_resources()
        max_capacity = 0.95
        if bot.resources[0] > bot.warehouse_capacity * max_capacity and not wood_notificaton:
            telebot.send_telegram_text(f'Wood almost full: {bot.twd.get_resources()[0]}/{bot.warehouse_capacity}.')
        else:
            wood_notificaton = True
        if bot.resources[1] > bot.warehouse_capacity * max_capacity and not clay_notification:
            telebot.send_telegram_text(f'Clay almost full: {bot.twd.get_resources()[1]}/{bot.warehouse_capacity}.')
        else:
            clay_notification = True
        if bot.resources[2] > bot.warehouse_capacity * max_capacity and not iron_notification:
            telebot.send_telegram_text(f'Iron almost full: {bot.twd.get_resources()[2]}/{bot.warehouse_capacity}.')
        else:
            iron_notification = True
        if bot.resources[3] > bot.granary_capacity * max_capacity and not crop_notification:
            telebot.send_telegram_text(f'Granary almost full: {bot.twd.get_resources()[3]}/{bot.granary_capacity}.')
        else:
            crop_notification = True


def farmer(config, farm_file, min_sleep_time, max_sleep_time):
    """
    Raids destinations specified in farm_file. Shuffles raid list each time farmer is initialized for more random
    behavior. Skips destination if unable to attack. If there are not enough troops function sleeps for random
    <min_sleep_time, max_sleep_time> [s].
    Parameters
    ----------
    config
    farm_file
    min_sleep_time
    max_sleep_time

    Returns
    -------

    """

    telebot = TelegramBot(config)
    last_msg_id = telebot.get_message_id()
    bot = Bot(config)
    last_msg_id = check_termination(bot, telebot, '/farmer', last_msg_id)
    bot.login()
    bot.load_farm_file(farm_file)
    random.shuffle(bot.farm_list)
    # Enter rally point
    sleep_random(0, 1)
    bot.twd.click_buildings()
    sleep_random(0, 1)
    bot.twd.click_rally_point()
    sleep_random(0, 1)
    while True:
        for destination in bot.farm_list:
            last_msg_id = check_termination(bot, telebot, '/farmer', last_msg_id)
            sleep_random(0, 3)
            bot.twd.click_rp_send_troops()
            # Unpack troops
            troops, coords = destination
            # Send troops to coordinates
            sleep_random(0, 1)
            enough_troops = bot.twd.send_troops(troops, AttackType.Raid, coords)
            if not bot.twd.check_attack_possible():
                telebot.send_telegram_text(f'Unable to send troops to {coords}')
                continue
            sleep_random(0, 1)
            sleeping_time = random.uniform(min_sleep_time, max_sleep_time)
            start_time = time.perf_counter()
            while time.perf_counter() - start_time < sleeping_time and not enough_troops:
                last_msg_id = check_termination(bot, telebot, '/farmer', last_msg_id)
            while not enough_troops:
                bot.twd.driver.refresh()
                enough_troops = bot.twd.send_troops(troops, AttackType.Raid, coords)


def builder(config, build_file, min_sleep_time=600, max_sleep_time=2400):
    """
    Builds buildings specified in build_file. If upgrade button is unavailable due to lack of resources script will
    sleep for random <min_sleep_time, max_sleep_time> [s].
    Parameters
    ----------
    config
    build_file
    min_sleep_time
    max_sleep_time

    Returns
    -------

    """
    telebot = TelegramBot(config)
    last_msg_id = telebot.get_message_id()
    bot = Bot(config)
    last_msg_id = check_termination(bot, telebot, '/builder', last_msg_id)
    bot.login()
    bot.load_build_queue_file(build_file)
    bot.twd.click_buildings()
    telebot.send_telegram_text(f'Build queue: {bot.building_queue}')
    for b in bot.building_queue:
        last_msg_id = check_termination(bot, telebot, '/builder', last_msg_id)
        bot.twd.click_building(b)
        while not bot.twd.is_upgrade_button():
            sleeping_time = random.uniform(min_sleep_time, max_sleep_time)
            start_time = time.perf_counter()
            while time.perf_counter() - start_time < sleeping_time:
                last_msg_id = check_termination(bot, telebot, '/builder', last_msg_id)
            bot.twd.driver.refresh()
        bot.twd.click_upgrade()
    telebot.send_telegram_text(f'Builder finished!')


def check_termination(bot: Bot, telebot: TelegramBot, command, last_msg_id):
    if last_msg_id != telebot.get_message_id():
        last_msg_id = telebot.get_message_id()
        c = telebot.get_telegram_text()
        if c == command:
            bot.twd.driver.close()
            sys.exit()
    return last_msg_id
