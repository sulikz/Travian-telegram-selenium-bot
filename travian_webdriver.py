import re
from configparser import ConfigParser

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

import undetected_chromedriver as uc
from enums import AttackType


class TravianWebDriver:
    """
    Class used to manage game UI.
    """

    def __init__(self, config_file):

        # Read config file
        self.config = ConfigParser()
        self.config.read(config_file)
        self.email = self.config.get('USER', 'email')
        self.password = self.config.get('USER', 'password')
        self.server = self.config.get('USER', 'server')
        self.url = self.config.get('WEBDRIVER', 'url')

        # Create driver
        self.driver = uc.Chrome()
        self.driver.maximize_window()
        self.driver.get(self.url)
        self.driver.implicitly_wait(2)

    def login(self):
        """

        Parameters
        ----------
        email: str
        password: str
        server: str
        """
        self.driver.find_element(by=By.XPATH, value='//*[@id="sectionAfter"]/ul/li[3]/a').click()
        self.driver.find_element(by=By.XPATH, value=f"//*[contains(text(), '{self.server}')]").click()
        self.driver.find_element(by=By.ID, value='usernameOrEmail').send_keys(self.email)
        self.driver.find_element(by=By.ID, value='password').send_keys(self.password)
        self.driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Log in and play')]").click()

    def close_popups(self):
        """
        Closes cookies pop ups that sometimes appear when entering the site.
        """
        cookies = self.driver.find_elements(by=By.XPATH, value="//*[contains(text(), 'Reject all')]")
        if cookies:
            cookies[0].click()
        cookies = self.driver.find_elements(by=By.XPATH, value="//*[contains(text(), 'Accept all')]")
        if cookies:
            cookies[0].click()

    def change_language(self):
        """
        Switch site language to British English.
        """
        self.driver.find_element(by=By.XPATH, value='//*[@id="sectionAfter"]/ul/li[1]/a/span').click()
        self.driver.find_element(by=By.XPATH,
                                 value='//*[@id="languageSelection"]/div/div[2]/div/div[2]/label[17]').click()

    def click_resources(self):
        """
        Click Resources icon.
        """
        self.driver.find_element(by=By.XPATH, value='//*[@id="navigation"]/a[1]').click()

    def click_buildings(self):
        """
        Click Buildings icon.
        """
        self.driver.find_element(by=By.XPATH, value='//*[@id="navigation"]/a[2]').click()

    def click_barracks(self):
        """
        From Buildings view click Barracks building.
        """
        self.driver.find_element(by=By.XPATH, value='//div[@id="villageContent"]/div[@data-name="Barracks"]').click()

    def click_rally_point(self):
        """
        From Buildings view click Rally Point building.
        """
        self.driver.find_element(by=By.XPATH, value='//*[@id="villageContent"]/div[@data-name="Rally Point"]').click()

    def click_rp_overview(self):
        """
        From Rally Point building view click Overview bar.
        """
        self.driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Overview')]").click()

    def click_rp_send_troops(self):
        """
        From Rally Point building view click Send Troops bar.
        """
        self.driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Send troops')]").click()

    def click_show_all_raids(self):
        """
        From Overview view clicks Show All button (if exists).
        """
        try:
            self.driver.find_element(by=By.XPATH, value='//*[@id="build"]/div[2]/p/a').click()
        except NoSuchElementException:
            pass

    def click_hero(self):
        """
        Clicks Hero icon.
        """
        self.driver.find_element(by=By.XPATH, value='//*[@id="heroImageButton"]').click()

    def click_adventures(self):
        """
        From Hero view clicks Adventure(s) bar.
        """
        self.driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Adventure(s)')]").click()

    # HERO #############################################################################################################

    def get_hp(self) -> int:
        """
        From Hero view checks hero hp.
        Returns
        -------
        int: Hero hp percentage.
        """
        hp = self.driver.find_element(by=By.XPATH,
                                      value='//*[@id="attributes"]/div[1]/div[3]/table/tbody/tr[1]/td[2]/span').text
        hp = hp.replace('%', '')
        return int(hp.encode('ascii', 'ignore'))

    def check_hero(self) -> bool:
        """
        From Resources view checks if Hero is in the village.
        Returns
        -------
        bool: True if Hero is available in the village, else False
        """
        # TODO
        return False

    def check_adventure(self) -> bool:
        """
        From Hero->Adventures view check if any adventure is available .
        Returns
        -------
        bool: True if adventure is available, else False
        """
        try:
            self.driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Start adventure')]")
            return True
        except NoSuchElementException:
            return False

    def send_on_adventure(self):
        """
        From Hero->Adventures view sends Hero on a first available adventure.
        """
        try:
            self.driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Start adventure')]").click()
        except NoSuchElementException:
            pass

    # ARMY #############################################################################################################

    def get_first_incoming_attack_time(self) -> int:
        """
        Gets time of first incoming raid from Resources view.
        Returns
        -------
        int: time until next attack in seconds.
        """
        try:
            attacks = self.driver.find_element(by=By.XPATH, value='//*[@id="movements"]/tbody/tr[2]/td[2]/div[1]').text
            if 'Attack' not in attacks:
                return 0
            time = self.driver.find_element(by=By.XPATH,
                                            value='//*[@id="movements"]/tbody/tr[2]/td[2]/div[2]/span').text
            time = time.split(':')
            time_seconds = int(time[0]) * 3600 + int(time[1]) * 60 + int(time[2])
            return time_seconds
        except NoSuchElementException:
            return 0

    def get_incoming_attacks_time(self) -> list:
        """
        From Rally Point Overview get times of up to 10 incoming attacks in seconds.
        Returns
        -------
        list: list of incoming attacks in seconds.
        """
        try:
            raid_list = []
            self.click_show_all_raids()
            troops_incoming = int(
                re.findall(r'\d+', self.driver.find_element(by=By.XPATH, value='//*[@id="build"]/div[2]/h4[1]').text)[
                    0])
            if troops_incoming > 0:
                for i in (i for i in range(1, (troops_incoming + 1 if troops_incoming <= 10 else 11))):
                    raid_text = self.driver.find_element(by=By.XPATH,
                                                         value=f'//*[@id="build"]/div[2]/table[{i}]/thead/tr/td[2]/a').text
                    is_raid = True if 'raids' in raid_text else False
                    time = self.driver.find_element(by=By.XPATH,
                                                    value=f'//*[@id="build"]/div[2]/table[{i}]/tbody[3]/tr/td/div[1]/span').text
                    time = time.split(':')
                    time_seconds = int(time[0]) * 3600 + int(time[1]) * 60 + int(time[2])
                    if is_raid:
                        raid_list.append(time_seconds)
                return raid_list
            return []
        except NoSuchElementException:
            return []

    def send_troops(self, troops: list, attack_type: AttackType, coordinates: tuple):
        """
        Sends troops to given coordinates.
        Parameters
        ----------
        troops: list of troops
                Index 0 - 1st unit (Phalanx/Clubswinger/Legionnaire)
                Index 2 - 2nd unit (Swordsman/Swordman/Praetorian)
                ...
                Index 10 - Settler
                Index 11 - Hero.
                e.g. [2, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1] for Romans corresponds to 2 Legionnaires, 1 Imperian, 1 hero.
        attack_type
        coordinates: tuple (x, y)
        """
        quantity_inputs = ['tr[1]/td[1]', 'tr[2]/td[1]', 'tr[3]/td[1]', 'tr[1]/td[2]', 'tr[2]/td[2]', 'tr[3]/td[2]',
                           'tr[1]/td[3]', 'tr[2]/td[3]', 'tr[1]/td[4]', 'tr[2]/td[4]', 'tr[3]/td[4]']
        # Select attack type
        if attack_type == AttackType.Reinforcement:
            self.driver.find_element(by=By.XPATH, value='//*[@class="option"]/label/input[@value="2"]').click()
        if attack_type == AttackType.Normal:
            self.driver.find_element(by=By.XPATH, value='//*[@class="option"]/label/input[@value="3"]').click()
        if attack_type == AttackType.Raid:
            self.driver.find_element(by=By.XPATH, value='//*[@class="option"]/label/input[@value="4"]').click()
        # Input coordinates
        self.driver.find_element(by=By.XPATH, value='//div[@class="xCoord"]/input').send_keys(coordinates[0])
        self.driver.find_element(by=By.XPATH, value='//div[@class="yCoord"]/input').send_keys(coordinates[1])
        # Input troops
        try:
            for index, t in enumerate(troops):
                self.driver.find_element(by=By.XPATH,
                                         value=f'//*[@id="troops"]/tbody/{quantity_inputs[index]}/input').send_keys(t)
        except NoSuchElementException:
            # in case hero is not in the village
            pass
        # Click submit
        self.driver.find_element(by=By.XPATH, value='//*[@id="btn_ok"]').click()
        # Click confirm
        self.driver.find_element(by=By.XPATH, value='//*[@id="btn_ok"]').click()

    def check_attack_possible(self):
        """
        Checks if there is an error message after attempting to send troops.
        Returns
        -------
        False if sending troops failed, else True.
        """
        try:
            self.driver.find_element(by=By.XPATH, value='//p[@class="error"]')
            return False
        except NoSuchElementException:
            return True

    def train_troops(self, troop: str, quantity: int):
        """
        Build troops from barracks view.

        Parameters
        ----------
        troop: str - troop name
        quantity: int
        """
        troop_name = self.driver.find_element(by=By.XPATH, value=f'//*[contains(text(), "{troop}")]')
        troop_panel = troop_name.find_element(by=By.XPATH, value='..//..//..//..')
        quantity_input = troop_panel.find_element(by=By.XPATH, value='//input[@class="text"]')
        quantity_input.clear()
        quantity_input.send_keys(quantity)
        self.driver.find_element(by=By.XPATH, value=f"//button[contains(text(), 'Train')]").click()

    def get_troops(self) -> list:
        """
        Get troops from rally point overview.
        :return:
        list - list of troops
        """

        troops_list = []
        self.driver.find_element(by=By.XPATH, value='//*[@id="build"]/div[1]/div/button[3]').click()
        troops_table = self.driver.find_elements(by=By.XPATH, value='//*[@id="build"]/div[2]/table/tbody[2]/tr/*')
        troops_table.pop(0)
        for t in troops_table:
            troops_list.append(int(t.text))
        return troops_list

    # VILLAGE ##########################################################################################################

    def get_resources(self) -> list:
        """
        Get current village resources.
        Returns
        -------
        list: List of current resources in the following order: [wood, clay, iron, crop]
        """
        res = ['l1', 'l2', 'l3', 'l4']
        resources_list = []
        for r in res:
            resources_list.append(int(self.driver.find_element(by=By.ID, value=r).text))
        return resources_list

    def get_production(self) -> list:
        """
        From Resources view get current resource production.
        Returns
        -------
        list: returns list of current resource production in the follwoing order: [wood, clay, iron, crop]
        """
        production_list = []
        production = self.driver.find_elements(by=By.CLASS_NAME, value='num')
        for index, r in enumerate(production):
            if index >= 4:
                break
            production_list.append(int(r.text.encode('ascii', 'ignore')))
        return production_list

    def get_capacity(self) -> list:
        """
        Get capacity of warehouse and granary.
        Returns
        -------
        list: returns list of capacity in the following order: [warehouse, granary]
        """
        capacity_list = []
        capacity = self.driver.find_elements(by=By.CLASS_NAME, value='capacity')
        for c in capacity:
            capacity_list.append(int(c.text.encode('ascii', 'ignore')))
        return capacity_list

    def get_fields(self) -> dict:
        # To get gid4 - crop fields
        # f = bot.twd.driver.find_element(by=By.XPATH, value='//*[contains(@class, "gid4")]')
        fields = []
        fields_content = self.driver.find_elements(by=By.XPATH, value='//*[@id="resourceFieldContainer"]/*')
        for f in fields_content:
            f = f.get_attribute('class').split(' ')
            fields.append(f[len(f) - 1])
        fields.pop(0)
        fields.pop()
        fields.pop()
        # TODO
        # return a proper structure. now returns list e.g. ['level2', 'level3' ... ]
        return fields_content

    def get_buildings(self) -> dict:
        """
        From Buildings view get all built buildings with their corresponding IDs.
        Returns
        -------
        dict: returns dictionary with pairs like: {int->id: str->building name}
        """
        buildings_dict = {}
        buildings_content = self.driver.find_elements(by=By.XPATH, value='//div[@id="villageContent"]/*')
        for building in buildings_content:
            if 'buildingSlot' in building.get_attribute(name='class'):
                building_name = building.get_attribute(name='data-name')
                id = building.get_attribute(name='data-aid')
                if building_name == '':
                    building_name = 'No_building'
                buildings_dict.update({int(id): building_name})
        return buildings_dict

    def construct_building(id: int, building_name: str):
        """

        Parameters
        ----------
        id - id of a slot to build in
        building_name - name of a building to build
        """
        # TODO
        pass
