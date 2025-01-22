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
import random

# handles savepaths for both mac/windows
if platform.system() == 'Windows':
    filepath = r'C:\Users\peary\OneDrive - The City University of New York\Web Scraping\Rental'
elif platform.system() == 'Darwin':
    filepath = r'/Users/pearsonyam/Library/CloudStorage/OneDrive-TheCityUniversityofNewYork/Web Scraping/Rental'
else:
    raise Exception("unsupported OS")

today = date.today()

# service = Service(r'C:\Users\peary\OneDrive - The City University of New York\Web Scraping\chromedriver-win64\chromedriver.exe')
seed_url = 'https://livehaus25.com/availability/'

# user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"

options = Options()
options.add_argument("--headless=new") 
driver = webdriver.Chrome(options=options)

# time.sleep(random.uniform(2, 4))
driver.get(seed_url)
print(f'scraping {seed_url}')

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


html = driver.page_source
driver.quit()
soup = BeautifulSoup(html, 'html.parser')
print('html saved')

units = soup.find_all('article', class_=re.compile(r"^wpgb-card"))

print(f'units: {units}')

# html parsing
titles = []
prices = []
availabilities = []
layouts = []
beds = []
baths = []
space = []
floor_plans = []
links = []


for unit in units:
    try:
        title = unit.find('div', class_='wpgb-block-2 floorplan-id-row unit_or_floorplan unit').text
        price = unit.find('div', class_='wpgb-block-1 floorplan-id-row rent display-none').text
        layout = unit.find('div', class_='wpgb-block-13 floorplan-bedrooms-row beds').text
        # bed = unit.find('div', class_='wpgb-block-13 floorplan-bedrooms-row').text
        # bath = unit.find('div', class_='wpgb-block-12 floorplan-bedrooms-row').text
        area = unit.find('div', class_='wpgb-block-6 floorplan-bedrooms-row sqft').text
        available = unit.find('div', class_='wpgb-block-17 floorplan-id-row move_in_date').text
        floor_plan = unit.find('div', class_='wpgb-block-11 floorplan-id-row unit_or_floorplan floorplan').text
        link = unit.find('a')['href']

        titles.append(title)
        prices.append(price)
        layouts.append(layout)
        # beds.append(bed)
        # baths.append(bath)
        availabilities.append(available)
        floor_plans.append(floor_plan)
        space.append(area)
        links.append(link)
    except Exception as e:
        print(f"no data available for {unit}")

    print(title)
    print(price)
    print(layout)
    # print(bed)
    # print(bath)
    print(area)
    print(available)
    print(floor_plan)
    print(link)

    print("")

# save data to dataframe
data = {
    'scraped_date': today,
    'title': titles,
    'price': prices,
    'layout': layouts,
    'area': space,
    'floor_plan': floor_plans,
    'availability': availabilities,
    'link': links
}

print('data parsed..')

df = pd.DataFrame(data)
print(df)

filename = 'Haus25_apt_data.csv'
fullpath = os.path.join(filepath, filename)


# Check if file exists and append or create new file
if not os.path.isfile(fullpath):
    headers = ['scraped_date', 'title', 'price', 'layout', 'area', 'floor_plan', 'availability', 'link']
    empty_df = pd.DataFrame(columns=headers)
    empty_df.to_csv(fullpath, index=False)
else:
    # read in existing file
    existing_df = pd.read_csv(fullpath)
    print('reading existing file..')

# concat existing data and save file
existing_df = pd.read_csv(fullpath)
new_df = pd.concat([existing_df, df])
new_df.to_csv(f'{fullpath}', index=None)

print(df)
print('Data saved to:', fullpath)
