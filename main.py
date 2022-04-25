import datetime
from configparser import ConfigParser

from bot import Bot
from process_wrapper import ProcessWrapper, builder, farmer, notifier
from telegram import TelegramBot

if __name__ == '__main__':
    config = ConfigParser()
    config.read('config.ini')
    tbot = TelegramBot(config)
    tbot.get_updates()
    last_msg_id = tbot.get_message_id()
    farmer_enabled = False
    builder_enabled = False
    notifier_enabled = False
    tbot.send_telegram_text('Bot enabled.')
    bot = Bot(config)
    bot.login()

    while True:
        if last_msg_id < tbot.get_message_id() and last_msg_id != 0:
            last_msg_id = tbot.get_message_id()
            command = tbot.get_telegram_text()

            if command == '/info':
                bot.read_resources()
                build_queue = bot.twd.is_built()
                build_queue = 'Busy' if build_queue else 'Free'
                attack_in = str(datetime.timedelta(seconds=bot.twd.get_first_incoming_attack_time()))
                tbot.send_telegram_text(
                    f'Warehouse: {bot.resources[0]}, {bot.resources[1]}, {bot.resources[2]} / {bot.warehouse_capacity} '
                    f'\nGranary: {bot.resources[3]}/{bot.granary_capacity}'
                    f'\nAttack in: {attack_in}'
                    f'\nBuilding queue: {build_queue}')

            if command == '/army':
                bot.read_troops()
                tbot.send_telegram_text(
                    f'{bot.stationary_troops}')

            if command == '/farmer':
                if not farmer_enabled:
                    farmer_process = ProcessWrapper(farmer, args=(config, 'farm_list.txt', 1800, 3600,))
                    farmer_process.start()
                    tbot.send_telegram_text('Farmer enabled.')
                    farmer_enabled = True
                else:
                    tbot.send_telegram_text('Farmer disabled.')
                    farmer_enabled = False

            if command == '/builder':
                builder_process = ProcessWrapper(builder, args=(config, 'build_queue.txt',))
                if not builder_enabled:
                    builder_process.start()
                    tbot.send_telegram_text('Builder enabled.')
                    builder_enabled = True
                else:
                    tbot.send_telegram_text('Builder disabled.')
                    builder_enabled = False

            if command == '/notifier':
                notifier_process = ProcessWrapper(notifier, args=(config,))
                if not notifier_enabled:
                    notifier_process.start()
                    tbot.send_telegram_text('Notifier enabled.')
                    notifier_enabled = True
                else:
                    tbot.send_telegram_text('Notifier disabled.')
                    notifier_enabled = False
