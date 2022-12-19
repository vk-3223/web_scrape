from email import header
from lib2to3.pgen2 import driver
from urllib import response
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time

URL = "https://www.zillow.com/new-york-ny/rentals/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22New%20York%2C%20NY%22%2C%22mapBounds%22%3A%7B%22west%22%3A-74.48642538476562%2C%22east%22%3A-73.47293661523437%2C%22south%22%3A40.35494887771488%2C%22north%22%3A41.038998252252%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A6181%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22mp%22%3A%7B%22min%22%3A800%2C%22max%22%3A2000%7D%2C%22price%22%3A%7B%22min%22%3A214245%2C%22max%22%3A535613%7D%7D%2C%22isListVisible%22%3Atrue%7D"

chrome_driver_path = "D:\my coding\python\python requird files\chromedriver_win32/chromedriver.exe"
header ={
    "Accept-Language":"en-US,en;q=0.9,hi;q=0.8",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
}

response = requests.get(url=URL,headers=header).text
soup = BeautifulSoup(response,"html.parser")

all_address_elements = soup.select(".list-card-info address")
all_addresses = [address.get_text().split(" | ")[-1] for address in all_address_elements]
print(all_addresses)

all_price = soup.select(".list-card-price")
all_price_home = [price.get_text().split("|")[-1] for price in all_price]
print(all_price_home)

all_links_of_home = soup.select(".list-card-top a")
all_link = []

for link in all_links_of_home:
    href = link["href"]
    if "http" not in href:
        all_link.append(f"https://www.zillow.com{href}")  ## convert into link ##
    else:
        all_link.append(href)
print(all_link)            


driver = webdriver.Chrome(executable_path=chrome_driver_path)

for n in range(len(all_link)):
    # Substitute your own Google Form URL here 👇
    driver.get("https://docs.google.com/forms/d/e/1FAIpQLSe1X4ZIiSvP_atGspCH0A9J9py2cFoNCsuPGtSq6yNg7kfoIA/viewform?usp=sf_link")

    time.sleep(2)
    address = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit_button = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div')

    address.send_keys(all_addresses[n])
    price.send_keys(all_price_home[n])
    link.send_keys(all_link[n])
    submit_button.click()
    
