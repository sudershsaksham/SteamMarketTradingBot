from enum import Enum
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import quote
import requests
import time
import pandas as pd
from typing import List

class Currency(Enum):
    """
    An enumeration representing various currencies.
    The `Currency` class is an `Enum` that encapsulates the ISO 4217a currency codes and their corresponding names.
    """
    USD = 1  # United States dollar
    GBP = 2  # Pound sterling
    EUR = 3  # Euro
    CHF = 4  # Swiss franc
    RUB = 5  # Russian ruble
    PLN = 6  # Polish złoty
    BRL = 7  # Brazilian real
    JPY = 8  # Japanese yen
    SEK = 9  # Swedish króna
    IDR = 10  # Indonesian rupiah
    MYR = 11  # Malaysian ringgit
    PHP = 12  # Philippine peso
    SGD = 13  # Singapore dollar
    THB = 14  # Thai baht
    VND = 15  # Vietnamese đồng
    KRW = 16  # South Korean won
    TRY = 17  # Turkish lira
    UAH = 18  # Ukrainian hryvnia
    MXN = 19  # Mexican peso
    CAD = 20  # Canadian dollar
    AUD = 21  # Australian dollar
    NZD = 22  # New Zealand dollar
    CNY = 23  # Renminbi
    INR = 24  # Indian rupee
    CLP = 25  # Chilean peso
    CUP = 26  # Cuban peso
    COP = 27  # Colombian peso
    ZAR = 28  # South African rand
    HKD = 29  # Hong Kong dollar
    TWD = 30  # New Taiwan dollar
    SAR = 31  # Saudi riyal
    AED = 32  # United Arab Emirates dirham
    # -
    ARS = 34  # Argentine peso
    ILS = 35  # Israeli new shekel
    # -
    KZT = 37  # Kazakhstani tenge
    KWD = 38  # Kuwaiti dinar
    QAR = 39  # Qatari riyal
    CRC = 40  # Costa Rican colon

def scrape_item_names() -> List[str]:
    '''
    :returns:   List of all Dota 2 items from Steam Marketplace 
                that are Immortal and of Standard Quality 
    '''    
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Runs Chrome in headless mode
    driver = webdriver.Chrome(options=chrome_options)

    # Open the Dota 2 items page on the Steam Marketplace for Immortals of Standard Quality
    url = "https://steamcommunity.com/market/search?q=&category_570_Hero%5B%5D=any&category_570_Slot%5B%5D=any&category_570_Type%5B%5D=any&category_570_Quality%5B%5D=tag_unique&category_570_Rarity%5B%5D=tag_Rarity_Immortal&appid=570"
    driver.get(url)

    item_names = set()

    not_last_page = True
    
    while not_last_page:
        # Wait for page load
        time.sleep(10)

        items = driver.find_elements(By.CSS_SELECTOR, '.market_listing_item_name_block')
        
        # Add item names to the set
        for item in items:
            item_names.add(item.text.split('\n')[0])
            
        # Wait for NxtPage button to be clickable
        try:
            element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#searchResults_btn_next"))
            )
        except:
            # Next page button is not clickable
            not_last_page = False
        else:    
            # Next page button is clickable
            next_page_button = driver.find_element(By.CSS_SELECTOR, '#searchResults_btn_next')
            next_page_button.click()

    # Close the driver
    driver.quit()

    return list(item_names)

def process_name(item_name: str) -> str:
    '''
    :params:    item_name
    :returns:   market_hash_name
    '''
    encoded_string = quote(item_name)
    return encoded_string

def generate_price_history_url(item_name: str) -> str:
    '''
    :params:    item_name
    :returns:   url to get request price history for the item
    '''
    base_url = "https://steamcommunity.com/market/pricehistory/?appid=570&market_hash_name="
    url = base_url + process_name(item_name)
    return url

def build_item_list() -> None:
    '''
    Saves main.csv file with all item_name, hash_name and url
    '''
    item_names = scrape_item_names()
    hash_names = list()
    urls = list()

    for item in item_names:
        hash_names.append(process_name(item))
        urls.append(generate_price_history_url(item))

    data = {'Item Name': item_names,
        'Hash Name': hash_names,
        'URL': urls}
    df = pd.DataFrame(data)
    df.to_csv('data/main.csv', index=False)
    print('Saved main.csv for all Dota 2 Immortal Standard Quality Items!')

def scrape_item_price_history(url: str) -> dict:
    '''
    returns price history json
    '''
    login_cookie_value = (
        "76561198150110459%7C%7CeyAidHlwIjogIkpXVCIsICJhbGciOiAiRWREU0EiIH0.eyAiaXNzIjogInI6MTAx"
        "Ql8yNTMzNDUzMl8wRUVENCIsICJzdWIiOiAiNzY1NjExOTgxNTAxMTA0NTkiLCAiYXVkIjogWyAid2ViOmNvbW11"
        "bml0eSIgXSwgImV4cCI6IDE3Mjg5Njg5MzcsICJuYmYiOiAxNzIwMjQxMDI3LCAiaWF0IjogMTcyODg4MTAyNywg"
        "imp0aSI6ICIxMDFCXzI1MzM0NTMyXzExMDRCIiwgIm9hdCI6IDE3Mjg4ODEwMjcsICJydF9leHAiOiAxNzQ3MDYy"
        "NTk3LCAicGVyIjogMCwgImlwX3N1YmplY3QiOiAiNC43MS4yNy4xNjEiLCAiaXBfY29uZmlybWVyIjogIjQuNzEu"
        "MjcuMTYxIiB9.XzoBgqqapATy8nRMBCHbiO8HMI63FIFbII8oB7WSwDz63h470lbN5pdiJspMqEdyHvNjUUXISzMU"
        "ygmeMW3VDw"
    )
    cookie = {'steamLoginSecure': login_cookie_value}    
    data = requests.get(url, cookies=cookie)
    return data.json()

def format_price_history_json():
    '''
    takes json, cleans it up for backtest.py
    '''