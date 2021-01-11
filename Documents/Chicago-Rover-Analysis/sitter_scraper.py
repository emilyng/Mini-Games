from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import time, os
import csv

chromedriver = "/Applications/chromedriver" # path to the chromedriver executable
os.environ["webdriver.chrome.driver"] = chromedriver
options = Options()
options.headless = True

url = "https://www.rover.com/search/?alternate_results=true&override_check=true&accepts_only_one_client=false&apse=false&bathing_grooming=false&cat_care=false&centerlat=41.804000&centerlng=-87.707000&dogs_allowed_on_bed=false&dogs_allowed_on_furniture=false&frequency=onetime&fulltime_availability=true&giant_dogs=false&has_fenced_yard=false&has_house=false&has_no_children=false&is_premier=false&knows_first_aid=false&large_dogs=false&location=60632&location_accuracy=5161&maxprice=150&medium_dogs=false&minprice=0&no_caged_pets=false&no_cats=false&no_children_0_5=false&no_children_6_12=false&non_smoking=false&page=1&person_does_not_have_dogs=false&pet=&petsitusa=false&pet_type=dog&puppy=false&service_type=dog-walking&small_dogs=false&volunteer_donor=false&search_score_debug=false&injected_medication=false&special_needs=false&oral_medication=false&more_than_one_client=false&uncrated_dogs=false&unspayed_females=false&non_neutered_males=false&females_in_heat=false&unactivated_provider=false&premier_matching=false&premier_or_rover_match=false&is_member_of_sitter_to_sitter=false&is_member_of_sitter_to_sitter_plus=false&location_type=geoip&midday_availability=true"
driver = webdriver.Chrome(chromedriver, options=options)
driver.get(url)
time.sleep(0.5)

driver.find_element_by_xpath('//*[@id="base-content"]/div[1]/div/div/div[2]/div[3]/button').click()
location_box = driver.find_element_by_xpath('//*[@id="base-content"]/div[1]/div/div/div[2]/div[3]/button').click()
time.sleep(0.5)

profile_links = []
names = []
locations = []

#get first 50 pages of result cars (20cards x 50pages) = 1000profiles
for page in range(50):
    soup = BeautifulSoup(driver.page_source, 'lxml')
    #getting profile links
    result_cards = soup.find_all('a', class_="SearchResultCard__MemberProfileAnchor-sc-69cmvm-0 jmSVjX")
    profile_links.append([card.get('href') for card in result_cards])
    #getting names
    name_cards = soup.find_all('a', class_='NameRow__NameLink-w16h4v-2 ddRlnv')
    names.append([card.text for card in name_cards])
    #getting location info
    info_cols = soup.find_all('span', class_="InfoColumn__Location-sc-9o301b-2 gjcFLl")
    locations.append([card.text for card in info_cols])
    time.sleep(0.5)
    #click next page
    try:
        driver.find_element_by_xpath('//*[@id="base-content"]/div[2]/div/ul/li[6]').click()
    except:
        pass
    try:
        driver.find_element_by_xpath('//*[@id="base-content"]/div[2]/div/ul/li[5]').click()
    except:
        pass
    time.sleep(0.5)

driver.close()

flat_profile_links = [link for sublist in profile_links for link in sublist]
flat_names = [name for sublist in names for name in sublist]
flat_locations = [location for sublist in locations for location in sublist]

rows = zip(flat_names, flat_locations, flat_profile_links)

with open('sitters.csv', mode='w') as file:
    writer = csv.writer(file)
    writer.writerow(['Name', 'Location', 'Link'])
    for row in rows:
        writer.writerow(row)
