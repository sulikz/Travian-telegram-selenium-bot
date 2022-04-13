import random
import time

from travian_webdriver import TravianWebDriver


class Production():
    wood = 0
    clay = 0
    iron = 0
    crop = 0


class Storage():
    wood = 0
    clay = 0
    iron = 0
    crop = 0
    warehouse_capacity = 0
    granary_capacity = 0


class Bot():

    def __init__(self, config_file, farm_file, build_file):
        self.farm_data = self.read_farm_file(farm_file)
        self.build_queue = self.read_build_queue_file(build_file)
        self.config_file = config_file
        self.twd = TravianWebDriver(self.config_file)
        self.twd.close_popups()
        self.twd.change_language()
        self.twd.login()
        self.troops = None
        self.village_buildings = None
        self.production = Production
        self.storage = Storage

    def get_resources_info(self):
        self.storage.warehouse_capacity, self.storage.granary_capacity = self.twd.get_capacity()
        self.storage.wood, self.storage.clay, self.storage.iron, self.storage.crop = self.twd.get_resources()
        self.production.wood, self.production.clay, self.production.iron, self.production.crop = self.twd.get_production()

    def get_buildings_info(self):
        self.twd.click_buildings()
        self.village_buildings = self.twd.get_buildings()

    def get_resources_info(self):
        pass

    def get_army_info(self):
        self.twd.click_buildings()
        self.twd.click_rally_point()
        self.twd.click_rp_overview()
        self.troops = self.twd.get_troops()

    def read_build_queue_file(self, build_queue_file):
        building_queue = []
        with open(build_queue_file) as file:
            for line in file.read().splitlines():
                if line.startswith('#'):
                    continue
                data = line.split(':')
                building_name = data[0]
                desired_level = int(data[1])
                building_queue.append((building_name, desired_level))
        return building_queue

    def read_farm_file(self, farm_list_file):
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
        return farm_list

    def sleep(self, min_t=1, max_t=5):
        time_to_sleep = random.uniform(min_t, max_t)
        time.sleep(time_to_sleep)
        return time_to_sleep
