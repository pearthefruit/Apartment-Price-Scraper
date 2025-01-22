from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
from datetime import date
import pandas as pd
import os
import time

def get_html(seed_url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")  # Optional, but recommended for Windows
    options.add_argument("--no-sandbox")  # Required for Linux

    driver = webdriver.Chrome(options=options)
    driver.get(seed_url)

    WebDriverWait(driver, 10).until(
        lambda d: d.execute_script('return document.readyState') == 'complete'
    )
    time.sleep(5)
    html = driver.page_source
    driver.quit()
    return html

def parse_results(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    units = soup.find_all('li', class_='css-1q2dra3')

    titles = []
    prices = []
    availabilities = []
    spaces = []
    links = []

    for unit in units:
        try:
            title = unit.find('div', class_='txt-box').h3.text.strip()
            price = unit.find('div', class_='txt-box').find_all('ul')[1].find_all('li')[0].text.strip()
            space = unit.find('div', class_='txt-box').find_all('ul')[1].find_all('li')[1].text.strip()
            available = unit.find('div', class_='txt-box').find_all('ul')[2].li.text.strip()
            link = unit.find('a')['href']

            titles.append(title)
            prices.append(price)
            availabilities.append(available)
            spaces.append(space)
            links.append(link)
        except AttributeError as e:
            print(f"Error parsing unit: {e}")
            continue

    return titles, prices, availabilities, spaces, links

def create_dataframe(titles, prices, availabilities, spaces, links):
    data = {
        'title': titles,
        'price': prices,
        'space': spaces,
        'availability': availabilities,
        'link': links
    }

    df = pd.DataFrame(data)
    return df

def main():
    today = date.today()
    filepath = r'C:\Users\peary\OneDrive - The City University of New York\Web Scraping\Rental'
    filename = f'{today.strftime("%Y-%m-%d")}_File.xlsx'

    urls = [
       'https://ironstate.com/property/90-columbus/',
       'https://ironstate.com/property/70-columbus/',
       'https://ironstate.com/property/50-columbus/'
    ]
    
    apt_list = []

    for i in range(len(urls)):
        seed_url = urls[i]
        titles, prices, availabilities, spaces, links = parse_results(get_html(seed_url))

        apt_list.append(create_dataframe(titles, prices, availabilities, spaces, links))

    final_df = pd.concat(apt_list, ignore_index=True)
    final_df.to_excel(os.path.join(filepath, filename), index=False)

    print(final_df)
    print('Data saved to:', filepath + '\\' + filename)
 
if __name__ == "__main__":
    main()
