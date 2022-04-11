import re

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

import undetected_chromedriver as uc

driver = uc.Chrome()
driver.maximize_window()
driver.get('https://www.travian.pl')


def switch_language():
    driver.find_element(by=By.XPATH, value='//*[@id="sectionAfter"]/ul/li[1]/a/span').click()
    driver.find_element(by=By.XPATH, value='//*[@id="languageSelection"]/div/div[2]/div/div[2]/label[17]').click()


def login(email, password, server):
    cookies = driver.find_elements(by=By.XPATH, value="//*[contains(text(), 'Reject all')]")
    if len(cookies) > 0:
        cookies[0].click()
    cookies = driver.find_elements(by=By.XPATH, value="//*[contains(text(), 'Accept all')]")
    if len(cookies) > 0:
        cookies[0].click()
    switch_language()
    driver.find_element(by=By.XPATH, value='//*[@id="sectionAfter"]/ul/li[3]/a').click()
    driver.find_element(by=By.XPATH, value=f"//*[contains(text(), '{server}')]").click()
    driver.find_element(by=By.ID, value='usernameOrEmail').send_keys(email)
    driver.find_element(by=By.ID, value='password').send_keys(password)
    driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Log in and play')]").click()


def click_resources():
    driver.find_element(by=By.XPATH, value='//*[@id="navigation"]/a[1]').click()


def click_buildings():
    driver.find_element(by=By.XPATH, value='//*[@id="navigation"]/a[2]').click()


def click_rally_point():
    driver.find_element(by=By.XPATH, value='//*[@id="villageContent"]/div[21]').click()


def click_rp_overview():
    driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Overview')]").click()


def click_show_all_raids():
    driver.find_element(by=By.XPATH, value='//*[@id="build"]/div[2]/p/a').click()


def click_hero():
    driver.find_element(by=By.XPATH, value='//*[@id="heroImageButton"]').click()


def click_adventures():
    driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Adventure(s)')]").click()


# HERO #################################################################################################################

def get_hero_hp():
    hp = driver.find_element(by=By.XPATH, value='//*[@id="attributes"]/div[1]/div[3]/table/tbody/tr[1]/td[2]/span').text
    hp = hp.replace('%', '')
    return int(hp.encode('ascii', 'ignore'))


def check_adventure():
    # TODO
    pass


def send_on_adventure():
    try:
        driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Start adventure')]").click()
    except:
        pass


# ARMY #################################################################################################################

def get_incoming_raid_time():
    click_resources()
    try:
        time = driver.find_element(by=By.XPATH, value='//*[@id="movements"]/tbody/tr[2]/td[2]/div[2]/span').text
        time = time.split(':')
        time_seconds = int(time[0]) * 3600 + int(time[1]) * 60 + int(time[2])
        return time_seconds
    except NoSuchElementException:
        return False


def get_10_raids():
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
            time_left = driver.find_element(by=By.XPATH,
                                            value=f'//*[@id="build"]/div[2]/table[{i}]/tbody[3]/tr/td/div[1]/span').text
            if is_raid:
                raid_list.append(time_left)
        return raid_list
    else:
        return 0


def send_attack():
    # TODO
    pass


def build_troops():
    # TODO
    pass


def get_troops():
    # TODO
    pass


# VILLAGE ############################################################################################################

def get_resources():
    res = ['l1', 'l2', 'l3', 'l4']
    resources_list = []
    for r in res:
        resources_list.append(int(driver.find_element(by=By.ID, value=r).text))
    return resources_list


def get_production():
    production_list = []
    production = driver.find_elements(by=By.CLASS_NAME, value='num')
    for r in production:
        production_list.append(int(r.text.encode('ascii', 'ignore')))
    production_list.pop()
    return production_list


def get_capacity():
    capacity_list = []
    capacity = driver.find_elements(by=By.CLASS_NAME, value='capacity')
    for c in capacity:
        capacity_list.append(int(c.text.encode('ascii', 'ignore')))
    return capacity_list


def get_buildings():
    # TODO
    pass


def construct_building():
    # TODO
    pass
