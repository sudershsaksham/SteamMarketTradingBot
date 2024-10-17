import os
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
from datetime import datetime, timezone

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

        try:
            items = driver.find_elements(By.CSS_SELECTOR, '.market_listing_item_name_block')
        except:
            not_last_page = False

        # Add item names to the set
        for item in items:
            print(item.text.split('\n')[0])
            item_names.add(item.text.split('\n')[0])
            
        if len(items) < 10:
            break

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

def generate_hero_id(item_name: str) -> str:
    '''
    :params:    Item Name
    :returns:   Hero ID from Dota 2  
    '''    
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Runs Chrome in headless mode
    driver = webdriver.Chrome(options=chrome_options)

    hero_dict = {
        'Anti-Mage': 1,
        'Axe': 2,
        'Bane': 3,
        'Bloodseeker': 4,
        'Crystal Maiden': 5,
        'Drow Ranger': 6,
        'Earthshaker': 7,
        'Juggernaut': 8,
        'Mirana': 9,
        'Shadow Fiend': 11,
        'Morphling': 10,
        'Phantom Lancer': 12,
        'Puck': 13,
        'Pudge': 14,
        'Razor': 15,
        'Sand King': 16,
        'Storm Spirit': 17,
        'Sven': 18,
        'Tiny': 19,
        'Vengeful Spirit': 20,
        'Windranger': 21,
        'Zeus': 22,
        'Kunkka': 23,
        'Lina': 25,
        'Lich': 31,
        'Lion': 26,
        'Shadow Shaman': 27,
        'Slardar': 28,
        'Tidehunter': 29,
        'Witch Doctor': 30,
        'Riki': 32,
        'Enigma': 33,
        'Tinker': 34,
        'Sniper': 35,
        'Necrophos': 36,
        'Warlock': 37,
        'Beastmaster': 38,
        'Queen of Pain': 39,
        'Venomancer': 40,
        'Faceless Void': 41,
        'Skeleton King': 42,
        'Death Prophet': 43,
        'Phantom Assassin': 44,
        'Pugna': 45,
        'Templar Assassin': 46,
        'Viper': 47,
        'Luna': 48,
        'Dragon Knight': 49,
        'Dazzle': 50,
        'Clockwerk': 51,
        'Leshrac': 52,
        "Nature's Prophet": 53,
        'Lifestealer': 54,
        'Dark Seer': 55,
        'Clinkz': 56,
        'Omniknight': 57,
        'Enchantress': 58,
        'Huskar': 59,
        'Night Stalker': 60,
        'Broodmother': 61,
        'Bounty Hunter': 62,
        'Weaver': 63,
        'Jakiro': 64,
        'Batrider': 65,
        'Chen': 66,
        'Spectre': 67,
        'Doom': 69,
        'Ancient Apparition': 68,
        'Ursa': 70,
        'Spirit Breaker': 71,
        'Gyrocopter': 72,
        'Alchemist': 73,
        'Invoker': 74,
        'Silencer': 75,
        'Outworld Devourer': 76,
        'Lycanthrope': 77,
        'Brewmaster': 78,
        'Shadow Demon': 79,
        'Lone Druid': 80,
        'Chaos Knight': 81,
        'Meepo': 82,
        'Treant Protector': 83,
        'Ogre Magi': 84,
        'Undying': 85,
        'Rubick': 86,
        'Disruptor': 87,
        'Nyx Assassin': 88,
        'Naga Siren': 89,
        'Keeper of the Light': 90,
        'Wisp': 91,
        'Visage': 92,
        'Slark': 93,
        'Medusa': 94,
        'Troll Warlord': 95,
        'Centaur Warrunner': 96,
        'Magnus': 97,
        'Timbersaw': 98,
        'Bristleback': 99,
        'Tusk': 100,
        'Skywrath Mage': 101,
        'Abaddon': 102,
        'Elder Titan': 103,
        'Legion Commander': 104,
        'Ember Spirit': 106,
        'Earth Spirit': 107,
        'Abyssal Underlord': 108,
        'Terrorblade': 109,
        'Phoenix': 110,
        'Techies': 105,
        'Oracle': 111,
        'Winter Wyvern': 112,
        'Arc Warden': 113,
    }

    url = "https://steamcommunity.com/market/listings/570/" + process_name(item_name)
    driver.get(url)
    try:
        element = driver.find_element(By.CSS_SELECTOR, '.descriptor:nth-child(1)').text
        if element.startswith("Used By: "):
            hero_name = element.replace("Used By: ", "")
            if hero_name in hero_dict:
                return hero_dict[hero_name]
            else:
                print(f"{item_name} has no associated hero!")
                return 0
        else:
            print(f"{item_name} has no associated hero!")
            return 0
    except:
        return 0
    
def build_item_list(dir_path: str) -> None:
    '''
    Saves main.csv file with all item_name, hash_name and url
    '''
    item_names = scrape_item_names()
    hash_names = list()
    urls = list()
    hero_ids = list()

    for item in item_names:
        hash_names.append(process_name(item))
        urls.append(generate_price_history_url(item))
        hero_ids.append(generate_hero_id(item))

    data = {
        'Item Name': item_names,
        'Hash Name': hash_names,
        'URL': urls,
        'Hero ID': hero_ids
        }
    
    df = pd.DataFrame(data)
    df.to_csv(os.path.join(dir_path, 'main.csv'), index=False)
    print('Saved main.csv for all Dota 2 Immortal Standard Quality Items!')

def scrape_item_price_history(url: str) -> requests.Response:
    '''
    :params:    URL to use to ask for data
    :returns:   Response Object
    '''
    # Open the file in read mode
    with open('config.txt', 'r') as file:
        login_cookie = file.read().split('\n')[0]

    header = {
    'Cookie': f'steamLoginSecure={login_cookie}'
    }
    data = requests.get(url, headers=header)
    return data

def parse_price_history_json(item_name: str, data: dict, dir_path: str) -> pd.DataFrame:
    '''
    :params:    Response Object for Item Price History Request
                Item Name in Hash Format
                Directory Path to Save Price History
    :returns:   Pandas DF of Daily Prices for Item Name
    '''
    if data.status_code != 200:
        return False
    else:
        df = pd.DataFrame(data.json()['prices'])
        df.rename(columns={0: 'Timestamp', 1: 'Price', 2: 'Volume'}, inplace=True)
        df['Timestamp'] = df['Timestamp'].str.replace(r': \+\d{1}', '', regex=True)
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%b %d %Y %H')
        df['Price'] = df['Price'].astype('float')
        df['Volume'] = df['Volume'].astype('int')
        df.to_csv(os.path.join(dir_path, f'{item_name}.csv'), index = False)
        return True

def process_price_history_row(row: pd.Series, dir_path: str) -> bool:
    '''
    :params:    A Single Row of the pandas DF which contains item_name, hash_name and url columns
    :saves:     A CSV file containing Price History
    :returns:   True if request successful, False otherwise
    '''
    item_name = row['Hash Name']
    if row['Hero ID'] == 0:
        print(f'No price history for {row['Item Name']} as it is not a hero item')
        return False
    
    data = scrape_item_price_history(row['URL'])
    time.sleep(5)
    if parse_price_history_json(item_name, data, dir_path):
        return True
    else:
        print(f'Error: could not save price history for {row['Item Name']}')
        return False

def convert_unix_to_date(unix_timestamp):
    return datetime.fromtimestamp(unix_timestamp, tz=timezone.utc).strftime('%Y-%m-%d')

def send_graphql_query(url, query, variables=None, headers=None):
    """Sends a GraphQL query and returns the response."""
    json_data = {
        'query': query,
        'variables': variables or {}
    }
    
    response = requests.post(url, json=json_data, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Query failed with status code {response.status_code}: {response.text}")

def get_hero_stats(hero_id, till_date, token):
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "STRATZ_API",
    }
    endpoint = "https://api.stratz.com/graphql"
    
    query = '''
    query ($heroId: [Short]!, $skip: Int!) {
        heroStats {
            winMonth(heroIds: $heroId, skip: $skip) {
                month
                matchCount
                winCount
            }
        }
    }
    '''
    
    # Initialize variables
    skip = 0
    batch_size = 8
    all_results = []  # List to store all fetched data
    
    while True:
        time.sleep(2)
        variables = {
            "heroId": hero_id,
            "skip": skip
        }
        
        # Send the GraphQL query
        response = send_graphql_query(endpoint, query, variables, headers)
        data = response.get('data', {}).get('heroStats', {}).get('winMonth', [])
        for each_row in data:
            each_row['month'] = convert_unix_to_date(each_row['month'])

        # Break the loop if no more data is returned
        if not data:
            break
        
        # Accumulate results
        all_results.extend(data)
        
        # Increment skip for pagination
        skip += batch_size
        
        # Check if we've reached the desired date and stop if necessary
        last_day = data[-1]['month']
        if last_day < till_date:
            break  # Stop fetching if we have reached or passed the till_date
    
    # Process or save the accumulated results as needed
    return all_results