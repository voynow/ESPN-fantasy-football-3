from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from webdriver_manager.chrome import ChromeDriverManager

from utils import configs

import json
import time


def create_driver(link=None):
    """
    Create chrome driver, get link if available
    """
    driver = webdriver.Chrome(ChromeDriverManager().install())
    if link:
        driver.get(link)

    return driver


def get_player_links_html(driver):
    
    elements_html = []
    next_page = True
    while next_page:
        elements = driver.find_elements(By.CLASS_NAME, 'sort1')
        elements_filtered = [element for element in elements if element.get_attribute('align') == 'LEFT']
        [elements_html.append(element.get_attribute('innerHTML')) for element in elements_filtered]

        try:
            driver.find_element(By.LINK_TEXT, "Next Page").click()
        except NoSuchElementException:
            next_page = False

    return elements_html


def collect_player_links(position_link):

    driver = create_driver(position_link)
    elements_html = get_player_links_html(driver)
    driver.close()

    # iterate over players
    player_links = {}
    for element in elements_html:

        # access player name and link to player data within HTML
        player_name = element.replace("</a>", "").split(">")[-1]
        player_link = configs.fftoday + element.split("\"")[1]

        # collect data in dictionary
        player_links[player_name] = player_link

    return player_links


def get_links():
    """
    Get web link for all players
    """
    position_ids = [10, 20, 30, 40, 80]
    link = configs.link
    suffix = configs.link_suffix

    position_links = [link + str(position_id) + suffix for position_id in position_ids]

    player_links = {}
    for position_link in position_links:
        
        player_links_subset = collect_player_links(position_link)
        for name, player_link in player_links_subset.items():
            player_links[name] = player_link 

    with open(configs.links_loc, "w") as f:
        json.dump(player_links, f, indent=4)


def collect_data(driver, links):
    """
    access raw data from each plauer link and collect metadata
    """
    data_collection = {}
    for i, (name, link) in enumerate(links.items()):
        
        driver.get(link)
        page_element = driver.find_element(By.CLASS_NAME, "bodycontent")

        strfrmt = "%m/%d/%Y, %H:%M:%S"
        data_collection[name] = {
            "id": i,
            "timestamp": time.strftime(strfrmt),
            "link": link,
            "data": page_element.text,
        }
    
    return data_collection


def get_raw():
    """
    facilitation of data collection from player_links
    """
    links = json.load(open(configs.links_loc, 'rb'))
    driver = create_driver()
    data_collection = collect_data(driver, links)

    with open(configs.raw_loc, "w") as f:
        json.dump(data_collection, f, indent=4)


def extract():
    
    get_links()
    get_raw()