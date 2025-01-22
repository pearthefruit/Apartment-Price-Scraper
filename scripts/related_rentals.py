# %%
import time
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import re

# %%
# Configure Edge Options
options = Options()
# options.add_argument("--headless=new")  # Run Edge in headless mode
path = r'C:\Users\peary\Documents\edgedriver_win64\msedgedriver.exe'
seed_url = "https://www.relatedrentals.com/search?city=46&property=4691%7C4696%7C4701%7C4706%7C4681%7C4686%7C47344341%7C4716%7C4721%7C4726%7C4741%7C4746%7C4731%7C4736%7C4756%7C4761%7C4766%7C4771%7C5604866%7C4786&field_line_special_offers_target_id_op=%3D&field_unit_special_offers_target_id_op=%3D&bedrooms=1&form-price-min=Any&form-price-max=Any&sort_by=field_availability_price_value&property_replacement[]=4601&property_replacement[]=4691&property_replacement[]=4696&property_replacement[]=4701&property_replacement[]=4706&property_replacement[]=16965636&property_replacement[]=4681&property_replacement[]=4686&property_replacement[]=47344341&property_replacement[]=4716&property_replacement[]=4611&property_replacement[]=4721&property_replacement[]=4726&property_replacement[]=4616&property_replacement[]=4741&property_replacement[]=4746&property_replacement[]=4731&property_replacement[]=4736&property_replacement[]=4621&property_replacement[]=4756&property_replacement[]=4626&property_replacement[]=4761&property_replacement[]=4766&property_replacement[]=4771&property_replacement[]=5604866&property_replacement[]=4636&property_replacement[]=4786&property_replacement[]=4601&property_replacement[]=4691&property_replacement[]=4696&property_replacement[]=4701&property_replacement[]=4706&property_replacement[]=16965636&property_replacement[]=4681&property_replacement[]=4686&property_replacement[]=47344341&property_replacement[]=4716&property_replacement[]=4611&property_replacement[]=4721&property_replacement[]=4726&property_replacement[]=4616&property_replacement[]=4741&property_replacement[]=4746&property_replacement[]=4731&property_replacement[]=4736&property_replacement[]=4626&property_replacement[]=4761&property_replacement[]=4766&property_replacement[]=4771&property_replacement[]=5604866&property_replacement[]=4636&property_replacement[]=4786&property_replacement[]=4601&property_replacement[]=4691&property_replacement[]=4696&property_replacement[]=4701&property_replacement[]=4706&property_replacement[]=16965636&property_replacement[]=4681&property_replacement[]=4686&property_replacement[]=47344341&property_replacement[]=4716&property_replacement[]=4616&property_replacement[]=4741&property_replacement[]=4746&property_replacement[]=4731&property_replacement[]=4736&property_replacement[]=4626&property_replacement[]=4761&property_replacement[]=4766&property_replacement[]=4771&property_replacement[]=5604866&property_replacement[]=4636&property_replacement[]=4786&property_replacement[]=4601&property_replacement[]=4691&property_replacement[]=4696&property_replacement[]=4701&property_replacement[]=4706&property_replacement[]=16965636&property_replacement[]=4681&property_replacement[]=4686&property_replacement[]=47344341&property_replacement[]=4716&property_replacement[]=4616&property_replacement[]=4741&property_replacement[]=4746&property_replacement[]=4731&property_replacement[]=4736&property_replacement[]=4626&property_replacement[]=4761&property_replacement[]=4766&property_replacement[]=4771&property_replacement[]=5604866&property_replacement[]=4601&property_replacement[]=4691&property_replacement[]=4696&property_replacement[]=4701&property_replacement[]=4706&property_replacement[]=16965636&property_replacement[]=4681&property_replacement[]=4686&property_replacement[]=47344341&property_replacement[]=4716&property_replacement[]=4626&property_replacement[]=4761&property_replacement[]=4766&property_replacement[]=4771&property_replacement[]=5604866&property_replacement[]=4601&property_replacement[]=4691&property_replacement[]=4696&property_replacement[]=4701&property_replacement[]=4706&property_replacement[]=16965636&property_replacement[]=4681&property_replacement[]=4686&property_replacement[]=47344341&property_replacement[]=4716&property_replacement[]=16965636&property_replacement[]=4681&property_replacement[]=4686&property_replacement[]=47344341&property_replacement[]=4716"

# Initialize WebDriver
# driver = webdriver.Edge(path, options=options)
driver = webdriver.Edge(path)

# Get the page HTML using Selenium
driver.get(seed_url)
height = driver.execute_script("return document.documentElement.scrollHeight")

time.sleep(5)  # Add a delay to ensure the page is fully loaded

driver.execute_script("window.scrollTo(0, {0})".format(height))

time.sleep(5)  # Add a delay to ensure the page is fully loaded

# Grab the HTML
html = driver.page_source

# Quit the WebDriver
driver.quit()


# %%
soup = BeautifulSoup(html,"html.parser")
# soup

# %%
''' retailer scrapes to pick up individual products'''

titles = []
uuids = []
property_neighborhoods = []
links = []
prices = []
base_url = "https://www.relatedrentals.com"

products = soup.find_all('div', class_='fg-unit-related__content')
for product in products:
    title = product.find('p', class_='title').text.strip()
    property_neighborhood = product.find('span', class_='property-neighborhood').text.strip()
    price = product.find('dd', class_='field-price').text.strip()
    link = product.parent.get('href').strip()
    uuid = link[-5:]
    
    titles.append(title)
    uuids.append(uuid)
    property_neighborhoods.append(property_neighborhood)
    prices.append(price)
    links.append(base_url + link)

    print("title: " + str(title))
    print("uuid: " + str(uuid))
    print("property-neighborhood: " + str(property_neighborhood))
    print("price: " + str(price))
    print("link: " + base_url + str(link))

# %%
from datetime import date
today = date.today()

data = {
    "date": today,
    "apt_id": uuids,
    "apt_size": titles,
    "property_neighborhood": property_neighborhoods,
    "price": prices,
    "links": links
}

df = pd.DataFrame(data)

# %%
df

# %%

file = str(today) + 'Related_Rental_APTs.xlsx'
path = r'C:\Users\peary\OneDrive - The City University of New York\Web Scraping\Rental'

df.to_excel(f'{path}\{file}', index=False)


