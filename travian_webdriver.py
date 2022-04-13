import re

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

import undetected_chromedriver as uc
from enums import AttackType

driver = uc.Chrome()
driver.maximize_window()
driver.get('https://www.travian.pl')


def switch_language():
    """
    Switch site language to english.
    """
    driver.find_element(by=By.XPATH, value='//*[@id="sectionAfter"]/ul/li[1]/a/span').click()
    driver.find_element(by=By.XPATH, value='//*[@id="languageSelection"]/div/div[2]/div/div[2]/label[17]').click()


def login(email, password, server):
    """

    Parameters
    ----------
    email: str
    password: str
    server: str
    """
    # Remove pop up windows that sometimes appear
    cookies = driver.find_elements(by=By.XPATH, value="//*[contains(text(), 'Reject all')]")
    if cookies:
        cookies[0].click()
    cookies = driver.find_elements(by=By.XPATH, value="//*[contains(text(), 'Accept all')]")
    if cookies:
        cookies[0].click()
    # Switch to british english
    switch_language()
    # Login part
    driver.find_element(by=By.XPATH, value='//*[@id="sectionAfter"]/ul/li[3]/a').click()
    driver.find_element(by=By.XPATH, value=f"//*[contains(text(), '{server}')]").click()
    driver.find_element(by=By.ID, value='usernameOrEmail').send_keys(email)
    driver.find_element(by=By.ID, value='password').send_keys(password)
    driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Log in and play')]").click()


def click_resources():
    """
    Click Resources icon.
    """
    driver.find_element(by=By.XPATH, value='//*[@id="navigation"]/a[1]').click()


def click_buildings():
    """
    Click Buildings icon.
    """
    driver.find_element(by=By.XPATH, value='//*[@id="navigation"]/a[2]').click()


def click_barracks():
    """
    Click Barracks building from Buildings view.
    """
    driver.find_element(by=By.XPATH, value='//div[@id="villageContent"]/div[@data-name="Barracks"]').click()


def click_rally_point():
    """
    Click Rally Point building from Buildings view.
    """
    driver.find_element(by=By.XPATH, value='//*[@id="villageContent"]/div[@data-name="Rally Point"]').click()


def click_rp_overview():
    """
    Click Overview bar from Rally Point building view.
    """
    driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Overview')]").click()


def click_send_troops():
    """
    Click Send Troops bar from Rally Point building view.
    """
    driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Send troops')]").click()


def click_show_all_raids():
    """
    Click Show All button from Overview view (if exists).
    """
    try:
        driver.find_element(by=By.XPATH, value='//*[@id="build"]/div[2]/p/a').click()
    except NoSuchElementException:
        return False


def click_hero():
    """
    Click Hero icon.
    """
    driver.find_element(by=By.XPATH, value='//*[@id="heroImageButton"]').click()


def click_adventures():
    """
    Click Adventure(s) bar from Hero view.
    """
    driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Adventure(s)')]").click()


# HERO #################################################################################################################

def get_hp() -> int:
    """
    Checks hero hp from Hero view.
    Returns
    -------
    int: Hero hp percentage.
    """
    hp = driver.find_element(by=By.XPATH, value='//*[@id="attributes"]/div[1]/div[3]/table/tbody/tr[1]/td[2]/span').text
    hp = hp.replace('%', '')
    return int(hp.encode('ascii', 'ignore'))


def check_hero() -> bool:
    """
    Checks if Hero is in the village from Resources view.
    Returns
    -------
    bool: True if Hero is available in the village, else False
    """
    return False


def check_adventure() -> bool:
    """
    Check if any adventure is available from Hero->Adventures view.
    Returns
    -------
    bool: True if adventure is available, else False
    """
    try:
        driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Start adventure')]")
        return True
    except NoSuchElementException:
        return False


def send_on_adventure():
    """
    Sends Hero on first available adventure
    """
    try:
        driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Start adventure')]").click()
    except NoSuchElementException:
        pass


# ARMY #################################################################################################################

def get_first_incoming_attack_time() -> int:
    """
    Gets time of first incoming raid from Resources view.
    Returns
    -------
    int: time until next attack in seconds.
    """
    click_resources()
    try:
        attacks = driver.find_element(by=By.XPATH, value='//*[@id="movements"]/tbody/tr[2]/td[2]/div[1]').text
        if 'Attack' not in attacks:
            return 0
        time = driver.find_element(by=By.XPATH, value='//*[@id="movements"]/tbody/tr[2]/td[2]/div[2]/span').text
        time = time.split(':')
        time_seconds = int(time[0]) * 3600 + int(time[1]) * 60 + int(time[2])
        return time_seconds
    except NoSuchElementException:
        return 0


def get_incoming_attacks_time() -> list:
    """
    Get times of up to 10 incoming attacks in seconds.
    Returns
    -------
    list: list of incoming attacks in seconds.
    """
    try:
        raid_list = []
        click_buildings()
        click_rally_point()
        click_rp_overview()
        click_show_all_raids()
        troops_incoming = int(
            re.findall(r'\d+', driver.find_element(by=By.XPATH, value='//*[@id="build"]/div[2]/h4[1]').text)[0])
        if troops_incoming > 0:
            for i in (i for i in range(1, (troops_incoming + 1 if troops_incoming <= 10 else 11))):
                raid_text = driver.find_element(by=By.XPATH,
                                                value=f'//*[@id="build"]/div[2]/table[{i}]/thead/tr/td[2]/a').text
                is_raid = True if 'raids' in raid_text else False
                time = driver.find_element(by=By.XPATH,
                                           value=f'//*[@id="build"]/div[2]/table[{i}]/tbody[3]/tr/td/div[1]/span').text
                time = time.split(':')
                time_seconds = int(time[0]) * 3600 + int(time[1]) * 60 + int(time[2])
                if is_raid:
                    raid_list.append(time_seconds)
            return raid_list
        return []
    except NoSuchElementException:
        return []


def send_attack(troop: list, attack_type: AttackType, coordinates: tuple):
    # TODO
    pass


def build_troops(troop: str, quantity: int):
    """
    Build troops from barracks view.

    Parameters
    ----------
    troop: str - troop name
    quantity: int
    """
    troop_name = driver.find_element(by=By.XPATH, value=f'//*[contains(text(), "{troop}")]')
    troop_panel = troop_name.find_element(by=By.XPATH, value='..//..//..//..')
    quantity_input = troop_panel.find_element(by=By.XPATH, value='//input[@class="text"]')
    quantity_input.clear()
    quantity_input.send_keys(quantity)


def get_troops() -> list:
    """
    Get troops from rally point overview.
    :return:
    list - list of troops
    """

    troops_list = []
    driver.find_element(by=By.XPATH, value='//*[@id="build"]/div[1]/div/button[3]').click()
    troops_table = driver.find_elements(by=By.XPATH, value='//*[@id="build"]/div[2]/table/tbody[2]/tr/*')
    troops_table.pop(0)
    for t in troops_table:
        troops_list.append(int(t.text))
    return troops_list


# VILLAGE ############################################################################################################

def get_resources() -> list:
    """
    Get current village resources.
    Returns
    -------
    list: List of current resources in the following order: [wood, clay, iron, crop]
    """
    res = ['l1', 'l2', 'l3', 'l4']
    resources_list = []
    for r in res:
        resources_list.append(int(driver.find_element(by=By.ID, value=r).text))
    return resources_list


def get_production() -> list:
    """
    Get current resource production from Resources view.
    Returns
    -------
    list: returns list of current resource production in the follwoing order: [wood, clay, iron, crop]
    """
    production_list = []
    production = driver.find_elements(by=By.CLASS_NAME, value='num')
    for r in production:
        production_list.append(int(r.text.encode('ascii', 'ignore')))
    production_list.pop()
    return production_list


def get_capacity() -> list:
    """
    Get capacity of warehouse and granary
    Returns
    -------
    list: returns list of capacity in the following order: [warehouse, granary]
    """
    capacity_list = []
    capacity = driver.find_elements(by=By.CLASS_NAME, value='capacity')
    for c in capacity:
        capacity_list.append(int(c.text.encode('ascii', 'ignore')))
    return capacity_list


def get_buildings() -> dict:
    """
    Get all buildings in the village with their corresponding IDs.
    Returns
    -------
    dict: returns dictionary with pairs like: {int->id: str->building name}
    """
    buildings_dict = {}
    village_content = driver.find_elements(by=By.XPATH, value='//div[@id="villageContent"]/*')
    for building in village_content:
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
