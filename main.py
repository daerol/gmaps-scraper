from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.chrome.options import Options
import os
import logging


SEARCH_TERM = "Bakery"
LOCATION = "Ang Mo Kio"
BASE_URL = "https://www.google.com/maps/search/{search}/@1.3158171,103.7213709,11.71z/data=!3m1!4b1"
FINAL_URL = BASE_URL.format(search=SEARCH_TERM+"+in+"+LOCATION)
browser = webdriver.Chrome()
SCROLL_PAUSE_TIME = 5
record = []
temp_array = []
number_counter = 0

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

def parse_data():

    action = ActionChains(browser)
    a = browser.find_elements(By.CLASS_NAME, "hfpxzc")
  
    while len(a) < 1000:
        
        var = len(a)
        scroll_origin = ScrollOrigin.from_element(a[len(a)-1])
        action.scroll_from_origin(scroll_origin, 0, 5000).perform()
        time.sleep(SCROLL_PAUSE_TIME)
        a = browser.find_elements(By.CLASS_NAME, "hfpxzc")
        

        if len(a) == var:
            print(f"{bcolors.OKCYAN}2/4: ----RUNNING: Preparing {(number_counter/len(a))*100:.2f}/100%... please wait... {bcolors.ENDC}")
            number_counter+=6
            if number_counter > len(a):
                break
        else:
            number_counter = 0
            print(f"{bcolors.OKBLUE}2/4: ----RUNNING: Loading {len(a)} queries... {bcolors.ENDC}")
    
        
    

    for i in range(len(a)):
        scroll_origin = ScrollOrigin.from_element(a[i])
        action.scroll_from_origin(scroll_origin, 0, 5000).perform()
        action.move_to_element(a[i]).perform()
        a[i].click()
        time.sleep(2)
        source = browser.page_source
        soup = BeautifulSoup(source, 'html.parser')
        try:
            # Reset the names, phone, address, website
            name, phone, address, website = "","","",""

            # Get company name
            company_name = soup.findAll('h1', {"class": "DUwDvf fontHeadlineLarge"})

            name = company_name[0].text
            if name not in temp_array:
                print(f"{bcolors.OKBLUE}3/4: ----RUNNING: Scraping {i}/{len(a)-1} company name:{name} {bcolors.ENDC}")

                # Store name in temp array to prevent duplicates
                temp_array.append(name)

                # Get phone number and website
                card_body = soup.findAll('div', {"class": "Io6YTe fontBodyMedium"})
                length_card_body = len(card_body)
                try:
                    for j in range(length_card_body):
                        if str(card_body[j].text)[0] == "6" or len(str(card_body[j].text)[0]) == 9:
                            phone = card_body[j].text
                except:
                    phone="Not available"

                address = card_body[0].text
                
                try:
                    for z in range(length_card_body):
                        if str(card_body[z].text)[-4] == "." or str(card_body[z].text)[-3] == "."  or str(card_body[z].text)[-2] == ".":
                            website = card_body[z].text
                except:
                    website="Not available"

                # Append to record
                record.append((name,phone,address,website))
                df = pd.DataFrame(record,columns=['Name','Phone number','Address','Website'])  
                df.to_csv(SEARCH_TERM + '.csv', index=False, encoding='utf-8')
        except:
            print(f"{bcolors.FAIL}3/4: ----FAILED: Phone or website error, IGNORE {bcolors.ENDC}")
            continue

    

if __name__ == "__main__":
    print(f"{bcolors.WARNING}1/4: ----INFO: Search Term: {SEARCH_TERM}, Location: {LOCATION} {bcolors.ENDC}")
    print(f"{bcolors.WARNING}1/4: ----STARTED: Running Gmaps Crawler {bcolors.ENDC}")
    browser.get(FINAL_URL)
    time.sleep(10)
    parse_data()
    print(f"{bcolors.OKGREEN}4/4: ----COMPLETED: Closing Gmaps Crawler pipeline {bcolors.ENDC}")