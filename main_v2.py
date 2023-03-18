import time
import os
import logging
import threading
import random
import settings
import pandas as pd
import concurrent.futures
from bs4 import BeautifulSoup
from selenium import webdriver
from emailfinder.extractor import *
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementClickInterceptedException
# ... other imports ...



SEARCH_TERM = "Bakery"
LOCATION = "Ang Mo Kio"
BASE_URL = "https://www.google.com/maps/search/{search}/@1.3158171,103.7213709,11.71z/data=!3m1!4b1"
FINAL_URL = BASE_URL.format(search=SEARCH_TERM+"+in+"+LOCATION)

# Selenium Settings
options = settings.create_chrome_options()
# PROXIES = settings.load_proxies('proxies.txt')  
# selected_proxy = random.choice(PROXIES)
# options.add_argument(f'--proxy-server={selected_proxy}')

browser = webdriver.Chrome(options=options)
SCROLL_PAUSE_TIME = 2
RESULT_LENGTH = 1000
record = []
temp_array = []



class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def scrape_element(element, temp_array, record):
    try:
        action = ActionChains(browser)
        action.move_to_element(element).perform()
        element.click()
        time.sleep(2)
        source = browser.page_source
        soup = BeautifulSoup(source, 'html.parser')
        try:
            name = soup.find('h1', {"class": "DUwDvf fontHeadlineLarge"}).text
            if name in temp_array:
                return

            print(f"{bcolors.OKBLUE}3/4: ----RUNNING: Scraping company name:{name} {bcolors.ENDC}")

            temp_array.append(name)
            card_body = soup.findAll('div', {"class": "Io6YTe fontBodyMedium"})

            phone = "Not available"
            website = "Not available"
            emails = []
            address = card_body[0].text

            for content in card_body:
                text = content.text
                if "." in text[-4:] or "." in text[-3:] or "." in text[-2:]:
                    website = content.text
                elif len(text) == 9:
                    phone = text

            if website != "Not available":
                emails = get_emails_from_bing(website)
                emails = '|'.join(emails)
            else:
                emails = "Not available"

            record.append((name, phone, address, website, emails))
            df = pd.DataFrame(record, columns=['Name', 'Phone number', 'Address', 'Website','Emails'])
            df.to_csv(SEARCH_TERM + "_" + LOCATION + '.csv', index=False, encoding='utf-8')

        except Exception as e:
            print(f"{bcolors.FAIL}3/4: ----FAILED: {e} has occurred {bcolors.ENDC}")
            return
    except (IndexError, ElementClickInterceptedException):
        return


def parse_data():
    number_counter = 0
    action = ActionChains(browser)
    a = browser.find_elements(By.CLASS_NAME, "hfpxzc")
    

    def scroll_to_element(element):
        scroll_origin = ScrollOrigin.from_element(element)
        action.scroll_from_origin(scroll_origin, 0, 5000).perform()
  
    while len(a) < RESULT_LENGTH:
        
        initial_value = len(a)
        scroll_to_element(a[len(a)-1])
        time.sleep(SCROLL_PAUSE_TIME)
        a = browser.find_elements(By.CLASS_NAME, "hfpxzc")
        

        if len(a) == initial_value:
            print(f"{bcolors.OKCYAN}2/4: ----RUNNING: Preparing {(number_counter/len(a))*100:.2f}/100%... please wait... {bcolors.ENDC}")
            number_counter+=6
            if number_counter > len(a):
                break
        else:
            number_counter = 0
            print(f"{bcolors.OKBLUE}2/4: ----RUNNING: Loading {len(a)} queries... {bcolors.ENDC}")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for element in a:
            scroll_to_element(element)
            executor.submit(scrape_element, element, temp_array, record)

    # ... the rest of the code for the parse_data function ...


def main():
    print(f"{bcolors.WARNING}1/4: ----INFO: Search Term: {SEARCH_TERM} | Location: {LOCATION} {bcolors.ENDC}")
    print(f"{bcolors.WARNING}1/4: ----STARTED: Running Gmaps Crawler {bcolors.ENDC}")
    browser.get(FINAL_URL)
    time.sleep(10)
    parse_data()
    print(f"{bcolors.OKGREEN}4/4: ----COMPLETED: Closing Gmaps Crawler pipeline {bcolors.ENDC}")


if __name__ == "__main__":
    main()
