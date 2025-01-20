from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import re
from datetime import date
import pandas as pd
import os
import time
import platform

# handles savepaths for both mac/windows
if platform.system() == 'Windows':
    filepath = r'C:\Users\peary\OneDrive - The City University of New York\Web Scraping\Rental'
elif platform.system() == 'Darwin':
    filepath = r'/Users/pearsonyam/Library/CloudStorage/OneDrive-TheCityUniversityofNewYork/Web Scraping/Rental'
else:
    raise Exception("unsupported OS")

today = date.today()
# filename = f'{today.strftime("%Y-%m-%d")}_File.xlsx'
filename = 'theBeach_data.csv'
fullpath = os.path.join(filepath, filename)

# read existing file
# Check if file exists and append or create new file
if not os.path.isfile(fullpath):
    headers = ['scraped_date', 'title', 'price', 'availability', 'area', 'link']
    empty_df = pd.DataFrame(columns=headers)
    empty_df.to_csv(fullpath, index=False)
else:
    # read in existing file
    existing_df = pd.read_csv(fullpath)

# Scraping
seed_url = 'https://www.beachjc.com/apartments-jersey-city-for-rent/'

options = Options()
options.add_argument("--headless=new") 
driver = webdriver.Chrome(options=options)

driver.get(seed_url)


# keeps scrolling to the bottom of the page so we can grab the full html
# Get initial height of the page
last_height = driver.execute_script("return document.documentElement.scrollHeight")

while True:
    # Scroll down to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    
    # Wait for new content to load
    time.sleep(3)
    
    # Calculate new scroll height after the page has loaded
    new_height = driver.execute_script("return document.documentElement.scrollHeight")
    
    # Check if the scroll height has increased, if not, we are at the bottom
    if new_height == last_height:
        break
    
    last_height = new_height  # Update to the new height and continue

# save the html object
html = driver.page_source
driver.quit()

# parse in beautifulsoup
soup = BeautifulSoup(html, 'html.parser')

# print(soup)

units = soup.find_all('div', class_='unit-list-item body-subtext transition')

# print(units)

titles = []
prices = []
availabilities = []
space = []
floor_plans = []
links = []

# selectors to pull out data
for unit in units:
    title = unit.find('span', class_='text-bold').text
    price = unit.find('span', class_='transition display-price text-bold').text
    area = unit.find('div', class_='col col--03 col--25 transition').text
    available = unit.div.button.find_all('div')[4].find_all('span')[2].text
    floor_plan = unit.find('span', class_='transition space-above').a['href']
    link = 'beachjc.com' + unit.find('button')['data-link']

    titles.append(title)
    prices.append(price)
    availabilities.append(available)
    space.append(area)
    links.append(link)

    print(title)
    print(price)
    print(area)
    print(available)
    print(link)

    print("")

data = {
    'scraped_date': today,
    'title': titles,
    'price': prices,
    'availability': availabilities,
    'area': space,
    'link': links
}

df = pd.DataFrame(data)
print(df)

new_df = pd.concat([existing_df, df], ignore_index=True)

new_df.to_csv(fullpath, index=None)

print(f'File saved to {fullpath}..')