import random
import re
import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

import undetected_chromedriver as uc
from enums import AttackType, Buildings


class TravianWebDriver:
    """
    Class used to manage game UI.
    """

    def __init__(self, url):
        # Create driver
        self.driver = uc.Chrome()
        self.driver.maximize_window()
        self.driver.get(url)
        self.driver.implicitly_wait(2)

    def login(self, email, password, server):
        """

        Parameters
        ----------
        email: str
        password: str
        server: str
        """
        self.driver.find_element(by=By.XPATH, value='//*[@id="sectionAfter"]/ul/li[3]/a').click()
        self.driver.find_element(by=By.XPATH, value=f"//*[contains(text(), '{server}')]").click()
        self.driver.find_element(by=By.ID, value='usernameOrEmail').send_keys(email)
        self.driver.find_element(by=By.ID, value='password').send_keys(password)
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

    def change_language_british(self):
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

    def click_upgrade(self):
        """
        Click building upgrade button.
        """
        self.driver.find_element(by=By.XPATH, value="//button[contains(text(), 'Upgrade to level')]").click()

    def is_upgrade_button(self):
        """
        Checks if upgrade button is available.
        Returns
        -------

        """
        try:
            self.driver.find_element(by=By.XPATH, value="//button[contains(text(), 'Upgrade to level')]")
            return True
        except NoSuchElementException:
            return False

    def click_building(self, name: str):
        """
        Click buiilding from Buildings menu.
        Parameters
        ----------
        name

        Returns
        -------

        """
        self.driver.find_element(by=By.XPATH, value=f'//div[@id="villageContent"]/div[@data-name="{name}"]').click()

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

    def click_stationary_troops_filter(self):
        """
        Turns on filter in Rally Point Overview.
        """
        self.driver.find_element(by=By.XPATH, value='//*[@id="build"]/div[1]/div/button[3]').click()

    def click_outgoing_troops_filter(self):
        """
        Turns on filter in Rally Point Overview.
        """
        self.driver.find_element(by=By.XPATH, value='//*[@id="build"]/div[1]/div/button[2]/').click()

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
        Checks if Hero is in the village.
        Returns
        -------
        bool: True if Hero is available in the village, else False
        """
        try:
            self.driver.find_element(by=By.XPATH, value='//*[@class="heroHome"]')
            return True
        except NoSuchElementException:
            return False

    def check_adventure(self) -> bool:
        """
        Checks if any adventure is available .
        Returns
        -------
        bool: True if adventure is available, else False
        """
        try:
            self.driver.find_element(by=By.XPATH, value='//*[@href="/hero/adventures"]/div')
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
        # Check if troops are incoming
        try:
            incoming_text = self.driver.find_element(by=By.XPATH, value='//*[@id="movements"]/tbody/tr[1]/th').text
            if 'Incoming' not in incoming_text:
                return 0
            # Check if is attack
            attacks = self.driver.find_element(by=By.XPATH, value='//*[@id="movements"]/tbody/tr[2]/td[2]/div[1]').text
            if 'Attack' not in attacks:
                return 0
        except (AttributeError, NoSuchElementException):
            return 0
        # Check time
        time = self.driver.find_element(by=By.XPATH,
                                        value='//*[@id="movements"]/tbody/tr[2]/td[2]/div[2]/span').text
        time = time.split(':')
        time_seconds = int(time[0]) * 3600 + int(time[1]) * 60 + int(time[2])
        return time_seconds

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
        # Input troops
        for index, t in enumerate(troops):
            if t > 0:
                troops_available = 0
                try:
                    troops_available = int(self.driver.find_element(by=By.XPATH,
                                                                    value=f'//*[@id="troops"]/tbody/{quantity_inputs[index]}/a').text.encode(
                        'ascii', 'ignore'))
                except NoSuchElementException:
                    # troops unavailable
                    pass
                if troops_available - t < 0:
                    # Not enough troops to send
                    return False
                try:
                    input_box = self.driver.find_element(by=By.XPATH,
                                                         value=f'//*[@id="troops"]/tbody/{quantity_inputs[index]}/input')
                    input_box.clear()
                    input_box.send_keys(t)

                except NoSuchElementException:
                    # in case hero is not in the village
                    pass
        # Select attack type
        if attack_type == AttackType.Reinforcement:
            self.driver.find_element(by=By.XPATH, value='//*[@class="option"]/label/input[@value="2"]').click()
        if attack_type == AttackType.Normal:
            self.driver.find_element(by=By.XPATH, value='//*[@class="option"]/label/input[@value="3"]').click()
        if attack_type == AttackType.Raid:
            self.driver.find_element(by=By.XPATH, value='//*[@class="option"]/label/input[@value="4"]').click()
        # Input coordinates
        self.driver.find_element(by=By.XPATH, value='//div[@class="xCoord"]/input').clear()
        self.driver.find_element(by=By.XPATH, value='//div[@class="xCoord"]/input').send_keys(coordinates[0])
        self.driver.find_element(by=By.XPATH, value='//div[@class="yCoord"]/input').clear()
        self.driver.find_element(by=By.XPATH, value='//div[@class="yCoord"]/input').send_keys(coordinates[1])
        # Click submit
        time.sleep(random.uniform(1, 4))
        self.driver.find_element(by=By.XPATH, value='//*[@id="btn_ok"]').click()
        time.sleep(random.uniform(0, 0.8))
        # Click confirm
        self.driver.find_element(by=By.XPATH, value='//*[@id="btn_ok"]').click()
        return True

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
            try:
                production_list.append(int("".join(filter(str.isdigit, r.text.encode('ascii', 'ignore')))))
            except TypeError:
                production_list.append(int(r.text.encode('ascii', 'ignore')))

        return production_list

    def get_capacity(self) -> list:
        """decode
        Get capacity of warehouse and granary.
        Returns
        -------
        list: returns list of capacity in the following order: [warehouse, granary]
        """
        capacity_list = []
        time.sleep(2)
        capacity = self.driver.find_elements(by=By.CLASS_NAME, value='capacity')
        for c in capacity:
            # capacity_list.append(int("".join(filter(str.isdigit, c.text.encode('ascii', 'ignore')))))
            capacity_list.append(int(c.text.encode('ascii', 'ignore').decode().replace(',', '')))
            # except TypeError:
            #     capacity_list.append(int(c.text.encode('ascii', 'ignore').decode().replace(',', '')))
        return capacity_list

    def get_fields(self) -> list:
        fields = []
        fields_content = self.driver.find_elements(by=By.XPATH, value='//*[@id="resourceFieldContainer"]/*')
        for f in fields_content:
            f = f.get_attribute('class').split(' ')
            fields.append(f[len(f) - 1])
        fields.pop(0)
        fields.pop()
        fields.pop()
        return fields

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

    def is_built(self):
        """
        From Resources/Buildings view checks if any building is currently being built.
        """
        try:
            self.driver.find_element(by=By.XPATH, value='//div[@class="buildingList"]')
            return True
        except NoSuchElementException:
            return False

    def upgrade_building(self, building_name: Buildings):
        """

        Parameters
        ----------
        building_name - name of a building to build
        """
        self.click_building(building_name.value)
        self.click_upgrade()
