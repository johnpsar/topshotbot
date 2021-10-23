import fake_useragent
from selenium import webdriver
from selenium.webdriver.chrome import options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import time


def initiate_driver():
    chromeoptions = webdriver.ChromeOptions()

    chromeoptions.add_argument('--disable-blink-features=AutomationControlled')
    chromeoptions.add_argument("--profile-directory=Default")
    chromeoptions.add_argument(
        "--user-data-dir=/home/johnpsar/.config/google-chrome")
    # chromeoptions.add_argument(f'--proxy-server={None}')
    chromeoptions.add_experimental_option(
        "excludeSwitches", ['enable-automation'])
    chromeoptions.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
    driver = webdriver.Chrome(options=chromeoptions)
    # driver.implicitly_wait(1)
    return driver


def create_momentranks_query(players, minPrice, maxPrice, teams, percentageDiscount, series):
    if(percentageDiscount == -1):
        url = "https://momentranks.com/topshot/marketplace?costBasis&limit=25"
    else:
        url = "https://momentranks.com/topshot/marketplace?costBasis=" + \
            str(percentageDiscount)+"&limit=25"
    for player in players:
        name = player.split()
        url += "&playerNames="
        for i in range(len(name)):
            if(i == 0):
                url += name[i]
            else:
                url += "%20"+name[i]
    if(minPrice != -1):
        url += "&priceRange="+str(minPrice)
    if(maxPrice != -1):
        url += "&priceRange="+str(maxPrice)
    for team in teams:
        teamname = team.split()
        url += "&teamNames="
        for i in range(len(teamname)):
            if(i == 0):
                url += teamname[i]
            else:
                url += "%20"+teamname[i]

    if(series != -1):
        url += "&series=Series%20"+str(series)
    print(url)
    return url


driver = initiate_driver()
time.sleep(1)
momentRanksURL = create_momentranks_query([], 4, 4, [], -1, -1)
driver.get(momentRanksURL)
# select moment from moment ranks 
try:
    i=0
    listing = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, "ListingCard_buy__1QVX8")))
    # listing.click()
    for listing in driver.find_elements_by_class_name("ListingCard_buy__1QVX8"):
        listing.click()
        try:
            i=i+1
            # switch to right tab 
            driver.switch_to.window(driver.window_handles[i])
            buybutton = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.CLASS_NAME, "jGdipa")))
            buybutton.click()
            break
        except:
            time.sleep(2)
            driver.switch_to.window(driver.window_handles[0])
            print("next")
except:
    print('Something went wrong when trying to redirect to Topshot')
    driver.quit()


# trying to buy
try:
    buybutton = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "jGdipa")))
    buybutton.click()
except:
    buybutton = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "ieOQLc")))
    buybutton.click()

try:
    buybutton = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, "css-wae9sn")))
    buybutton.click()
except:
    print('No buy button')
