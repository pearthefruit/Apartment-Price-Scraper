import sys
import re
import pandas as pd
import platform
import os
from datetime import date
import random

if platform.system()=="Windows":
    sys.path.append(r'C:\Users\peary\OneDrive - The City University of New York\Web Scraping')
elif platform.system()=="Darwin":
    sys.path.append(r'/Users/pearsonyam/Library/CloudStorage/OneDrive-TheCityUniversityofNewYork/Web Scraping')

import scrapers



today = date.today()

def getAptDataFromSoup(soup):
    units = soup.find_all('div', class_='listingCardBottom listingCardBottom-rental')
    titles = []
    descriptions = []
    prices = []
    fees = []
    # availabilities = []
    beds = []
    baths = []
    space = []
    # floor_plans = []
    links = []


    for unit in units:
        title = unit.find('address', class_='listingCard-addressLabel listingCard-upperShortLabel').text.strip()
        description = unit.find('p', class_='listingCardLabel listingCardLabel-grey listingCard-upperShortLabel').text.strip()
        price = unit.find('span', class_='price listingCard-priceMargin').text
        try:
            fee = unit.find('span', class_='NoFeeBadge NoFeeBadge--SRPCard').text
        except Exception as e:
            fee = 'n/a'
        try:
            bed = unit.find('div', class_='listingDetailDefinitions').find_all('div')[0].text.strip()
        except Exception as e:
            bed = 'n/a'
        bath = unit.find('span', class_='listingDetailDefinitionsText', string=re.compile("Bath")).text.strip()
        try:
            area = unit.find_all('div', class_='listingDetailDefinitionsItem')[3].find_all('span', class_='listingDetailDefinitionsText')[1].text
        except Exception as e:
            area = "n/a"
        # available = unit.div.button.find_all('div')[4].find_all('span')[2].text
        # floor_plan = unit.find('span', class_='transition space-above').a['href']
        link = unit.find('address', class_='listingCard-addressLabel listingCard-upperShortLabel').a['href']

        titles.append(title)
        descriptions.append(description)
        beds.append(bed)
        baths.append(bath)
        prices.append(price)
        fees.append(fee)
        # availabilities.append(available)
        space.append(area)
        links.append(link)

        print('title:', title)
        print('description:', description)
        print('beds: ' + bed)
        print('baths:', baths)
        print('price: ', price)
        print('fee: ', fee)
        print('area:', area)
        # print(available)
        print('link: ', link)
        print("")

    data = {
        'scraped_date': today,
        'title': title,
        'description': description,
        'beds': beds,
        'baths': baths,
        'price': prices,
        'fee': fees,
        'sqft': space,
        'link': links
    }

    df = pd.DataFrame(data)

    return df

def createEmptyDF(columns):
    data = {}
    df.columns = columns
    df = pd.DataFrame(data)
    return df

def main():
    STREETEASY_BASEURL = 'https://streeteasy.com/for-rent/nyc/'
    FILTERS = 'price:-8000%7Carea:104,158,120,123%7Cbeds:1-2%7Cin_rect:40.714,40.749,-74.004,-73.943%7Camenities:washer_dryer,dishwasher,elevator,doorman'
    START_PAGE = 1

    # handles savepaths and filenames for both mac/windows
    if platform.system() == 'Windows':
        filepath = r'C:\Users\peary\OneDrive - The City University of New York\Web Scraping\Rental'
    elif platform.system() == 'Darwin':
        filepath = r'/Users/pearsonyam/Library/CloudStorage/OneDrive-TheCityUniversityofNewYork/Web Scraping/Rental'
    else:
        raise Exception("unsupported OS")

    filename = 'StreetEasy_data.csv'
    fullpath = os.path.join(filepath, filename)

    # Check if file exists and append or create new file
    if not os.path.isfile(fullpath):
        headers = ['scraped_date', 'title', 'description', 'beds', 'baths', 'price', 'fee', 'sqft', 'link']
        empty_df = pd.DataFrame(columns=headers)
        empty_df.to_csv(fullpath, index=False)
    else:
        # read in existing file
        existing_df = pd.read_csv(fullpath)

    # scrape the initial URL to get the max pages
    soup = scrapers.scrape_Sel(f'{STREETEASY_BASEURL}{FILTERS}?page={START_PAGE}')
    print('scraping initial url to extract max pages..')
    max_page = soup.find('ul', class_='pagination-list-container').find_all('li')[4].text.strip()

    # create an empty dataframe to append data to
    df = createEmptyDF(['scraped_date', 'title', 'description', 'beds', 'baths', 'price', 'fee', 'sqft', 'link'])

    # scrape all pages from url
    for i in range(1, max_page, 1):
        soup = scrapers.scrape_Sel(f'{STREETEASY_BASEURL}{FILTERS}?page={i}')
        print(f'scraping page {i}')
        units = soup.find_all('span', class_='u-displayNone')

        # combine results from each new page
        df = pd.concat([df, getAptDataFromSoup(soup)])

    # append the data to the existing data file
    new_df = pd.concat([existing_df, df])


if __name__ == "__main__":
    main()
