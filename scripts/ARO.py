import requests
from bs4 import BeautifulSoup

url = 'https://aro.nyc/availability/'

response = requests.get(url, "html.parser")
soup = BeautifulSoup(response.content)

units = soup.find_all('div', class_='grid-x avai-list')



for unit in units:
    print (unit.text)
