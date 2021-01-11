from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from tqdm import tqdm
import requests
import time, os
import csv
import json

chromedriver = "/Applications/chromedriver" # path to the chromedriver executable
os.environ["webdriver.chrome.driver"] = chromedriver
options = Options()
options.headless = True

def get_name(name_card):
    return name_card.text.strip()

#get price per service in form of list of tuples
def get_service_prices(service_card):
    service_prices = []

    service_list = service_card.find_all('h3', class_='h5 margin-v-x0')
    price_list = service_card.find_all('div', class_='h2 margin-v-x0')

    for service, price in zip(service_list, price_list):
        service_str = service.text.strip()
        price_int = int(price.text.strip().replace('$', ''))
        service_prices.append((service_str, price_int))

    return service_prices

#convert list of tuples into dictionary
def Convert(tup, di):
    di = dict(tup)
    return di

#read into sitters.csv and retrieve sitter profile_links
profile_links = []
with open('sitters.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    for row in csv_reader:
        profile_links.append(row['Link'])

#scrape and retrieve service prices
sitter_service_prices = []

for link in tqdm(profile_links):
    driver = webdriver.Chrome(chromedriver, options=options)
    driver.get(link)
    soup = BeautifulSoup(driver.page_source, 'lxml')

    #name
    name_card = soup.find('h1', class_='provider-name media-heading nomargin')
    name = get_name(name_card)

    #service_prices dict
    service_card = soup.find('div', class_='services-card')
    service_prices_list = get_service_prices(service_card)
    dictionary = {}
    service_prices = Convert(service_prices_list, dictionary)

    profile = {'Name': name, 'Services': service_prices}
    sitter_service_prices.append(profile)

    driver.close()

with open('service_prices.json', 'w') as fout:
    json.dump(sitter_service_prices, fout)
