import random
import time
from configparser import ConfigParser

from enums import AttackType
from travian_webdriver import TravianWebDriver


class Bot:
    config = ConfigParser()

    def __init__(self, config_file):
        # Read config
        self.config.read(config_file)
        self.email = self.config.get('USER', 'email')
        self.password = self.config.get('USER', 'password')
        self.server = self.config.get('USER', 'server')
        self.url = self.config.get('WEBDRIVER', 'url')
        # Initialize webdriver
        self.twd = TravianWebDriver(self.url)
        # Initialize attributes
        self.farm_list = None
        self.building_queue = None
        self.stationary_troops = None
        self.village_buildings = None
        self.fields = []
        self.production = Production
        self.storage = Storage

    def login(self):
        self.twd.close_popups()
        if 'Europe' in self.server:
            self.twd.change_language_british()
        self.twd.login(self.email, self.password, self.server)

    def read_village_info(self):
        functions = [self.twd.click_resources(), self.read_resources(), self.read_fields(), self.twd.click_buildings(),
                     self.read_buildings(), self.twd.click_resources()]
        for f in functions:
            sleep_random()
            f()

    def read_troops(self):
        functions = [self.twd.click_buildings(), self.twd.click_rally_point(), self.twd.click_rp_overview(),
                     self.twd.click_stationary_troops_filter(), self.read_army(), self.twd.click_resources()]
        for f in functions:
            sleep_random()
            f()

    def send_troops(self, troops: list, attack_type: AttackType, coordinates: tuple):
        self.twd.send_troops(troops, attack_type, coordinates)

    def read_resources(self):
        self.storage.warehouse_capacity, self.storage.granary_capacity = self.twd.get_capacity()
        self.storage.wood, self.storage.clay, self.storage.iron, self.storage.crop = self.twd.get_resources()
        self.production.wood, self.production.clay, self.production.iron, self.production.crop = self.twd.get_production()

    def read_buildings(self):
        self.village_buildings = self.twd.get_buildings()

    def read_fields(self):
        fields_type = ['wood', 'crop', 'wood', 'iron', 'clay', 'clay', 'iron', 'crop', 'crop', 'iron', 'iron', 'crop',
                       'crop', 'wood', 'crop', 'clay', 'wood', 'clay']
        for index, f in enumerate(self.twd.get_fields()):
            self.fields.append((fields_type[index], f))

    def read_army(self):
        self.stationary_troops = self.twd.get_troops()

    def check_attack(self):
        return self.twd.get_first_incoming_attack_time()

    def load_farm_file(self, farm_list_file):
        farm_list = []
        with open(farm_list_file) as file:
            for line in file.read().splitlines():
                if line.startswith('#'):
                    continue
                data = line.split(';')
                coords = data[1].split(' ')
                coords = (int(coords[0]), int(coords[1]))
                troops = list(int(t) for t in data[0].split(' '))
                farm_list.append((troops, coords))
        self.farm_list = farm_list

    def load_build_queue_file(self, build_queue_file):
        building_queue = []
        with open(build_queue_file) as file:
            for line in file.read().splitlines():
                if line.startswith('#'):
                    continue
                data = line.split(':')
                building_name = data[0]
                desired_level = int(data[1])
                building_queue.append((building_name, desired_level))
        self.building_queue = building_queue


def sleep_random(min_t=0.5, max_t=3):
    time_to_sleep = random.uniform(min_t, max_t)
    time.sleep(time_to_sleep)
    return time_to_sleep


class Production:
    wood = 0
    clay = 0
    iron = 0
    crop = 0


class Storage:
    wood = 0
    clay = 0
    iron = 0
    crop = 0
    warehouse_capacity = 0
    granary_capacity = 0
