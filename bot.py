import random
import time

from travian_webdriver import TravianWebDriver


class Bot:

    def __init__(self, config):
        # Read config
        self.email = config.get('USER', 'email')
        self.password = config.get('USER', 'password')
        self.server = config.get('USER', 'server')
        self.url = config.get('WEBDRIVER', 'url')
        # Initialize webdriver
        self.twd = TravianWebDriver(self.url)
        # Initialize attributes
        self.farm_list = []
        self.building_queue = []
        self.stationary_troops = []
        self.village_buildings = {}
        self.fields = []
        self.production = []
        self.resources = []
        self.granary_capacity = None
        self.warehouse_capacity = None

    def login(self):
        self.twd.close_popups()
        if 'Europe' in self.server:
            self.twd.change_language_british()
        self.twd.login(self.email, self.password, self.server)
        time.sleep(1)

    def read_village_info(self):
        functions = [self.twd.click_resources, self.read_resources, self.read_fields, self.twd.click_buildings,
                     self.read_buildings, self.twd.click_resources]
        for f in functions:
            sleep_random()
            f()

    def read_troops(self):
        functions = [self.twd.click_buildings, self.twd.click_rally_point, self.twd.click_rp_overview,
                     self.twd.click_stationary_troops_filter, self.read_army, self.twd.click_resources]
        for f in functions:
            sleep_random()
            f()

    def read_resources(self):
        self.warehouse_capacity, self.granary_capacity = self.twd.get_capacity()
        self.resources = self.twd.get_resources()
        self.production = self.twd.get_production()

    def read_buildings(self):
        self.village_buildings = self.twd.get_buildings()

    def read_fields(self):
        fields_type = ['wood', 'crop', 'wood', 'iron', 'clay', 'clay', 'iron', 'crop', 'crop', 'iron', 'iron', 'crop',
                       'crop', 'wood', 'crop', 'clay', 'wood', 'clay']
        for index, f in enumerate(self.twd.get_fields()):
            self.fields.append((fields_type[index], f))

    def read_army(self):
        self.stationary_troops = self.twd.get_troops()

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
                building_name = line
                building_queue.append(building_name)
        self.building_queue = building_queue


def sleep_random(min_t=1, max_t=3):
    time_to_sleep = random.uniform(min_t, max_t)
    time.sleep(time_to_sleep)
    return time_to_sleep
