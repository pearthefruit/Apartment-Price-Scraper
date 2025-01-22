import pandas as pd
import requests
from bs4 import BeautifulSoup

url = "https://99hudsonliving.com/availability/"
url2 = "https://www.65bay.com"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
}

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.content, "html.parser")

apartments = soup.find_all("div", class_ = "residence-item")

apartment_names = []
apartment_prices = []
bedrooms = []
bathrooms = []
size = []

for apartment in apartments:
    name = apartment.find('div', class_="residence-item__details__name")
    price = apartment.find('div', class_="residence-item__details__price")
    beds = apartment.find('span', class_="residence-item__details__layout__type")
    baths = apartment.find('span', class_ = "residence-item__details__layout__bathrooms")
    sqft = apartment.find('span', class_ ="residence-item__details__layout__footage")
    
    apartment_names.append(name.text)
    apartment_prices.append(price.text.strip())
    bedrooms.append(beds.text.strip())
    bathrooms.append(baths.text.strip())
    size.append(sqft.text.strip())

from datetime import date
data = {
    'Date': [date.today()] * len(apartment_names),
    'Apartment Name': apartment_names,
    'Price': apartment_prices,
    'Bedrooms': bedrooms,
    'Bathrooms': bathrooms,
    'Size': size
}

df = pd.DataFrame(data)
print(df)


today = date.today()
filename = f'99_hudson_living_{today}.xlsx'
path = r'C:\Users\peary\OneDrive - The City University of New York\Web Scraping\Rental'

# save new data to today's date
df.to_excel(f'{path}\{filename}', index=False)

# append data to running file - pulls from 99_hudson_condos.xlsx
df2 = pd.read_excel(r'C:\Users\peary\OneDrive - The City University of New York\Web Scraping\Rental\99_hudson_condos.xlsx')
# df['Date'] = pd.to_datetime(df['Date'])

# concatenate new data and old data from existing file
df_concat = pd.concat([df, df2])
print(df)
print(df2)


df_concat.to_excel(f'{path}\\{today}_99_hudson_condos.xlsx', index=False)
