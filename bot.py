import random
import time
from configparser import ConfigParser

from travian_webdriver import TravianWebDriver


class Bot:
    config = ConfigParser()

    def __init__(self, config_file):
        self.config.read(config_file)
        self.farm_list = None
        self.building_queue = None
        self.twd = TravianWebDriver(self.config)
        self.troops = None
        self.village_buildings = None
        self.fields = []
        self.production = Production
        self.storage = Storage
        self.dodge_attacks = bool(self.config.get('USER', 'dodge_attacks'))

    # def dodge(self):
    #     self.twd.click_buildings()
    #     self.twd.click_rally_point()
    #     self.twd.click_rp_send_troops()
    #     self.twd.send_troops()
    #     self.twd.click_rp_overview()
    #     pass

    def login(self):
        # self.twd = TravianWebDriver(self.config)
        self.twd.close_popups()
        self.twd.change_language()
        self.twd.login()

    def read_village_info(self):
        functions = [self.read_resources, self.read_fields, self.twd.click_buildings,
                     self.read_buildings, self.twd.click_resources]
        # self.read_buildings, self.twd.click_rally_point,
        # self.twd.click_rp_overview, self.read_army, self.twd.click_resources]
        for f in functions:
            sleep_random()
            f()

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
        self.troops = self.twd.get_troops()

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
