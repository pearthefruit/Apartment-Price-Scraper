import requests
import pandas as pd
from pandas import json_normalize
import datetime
import os
import numpy as np
import platform

today = datetime.date.today()

if platform.system() == 'Windows':
    path = r'C:\Users\peary\OneDrive - The City University of New York\Web Scraping\Rental'
elif platform.system() == 'Darwin':
    path = r'/Users/pearsonyam/Library/CloudStorage/OneDrive-TheCityUniversityofNewYork/Web Scraping/Rental'
else:
    raise Exception("unsupported OS")

fn = f'Hendrix_data.csv'
filepath = os.path.join(path, fn)

# API endpoint
url = "https://lgyp3mx3h9.execute-api.us-east-1.amazonaws.com/api/19f97cb9-ab75-4c22-8bc6-5670a297e2cc/load-inventory"
headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'authorization': 'kpYR3DWlBW8GycCOmLpmG59PcsIaie237VBAJ2x4',
    'dnt': '1',
    'origin': 'https://www.thehendrixjc.com',
    'priority': 'u=1, i',
    'referer': 'https://www.thehendrixjc.com/',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
}

response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
  try:
    # Parse the JSON data
    data = response.json()
    
    # Normalize the JSON data
    units_df = pd.json_normalize(data['units'])
    
    # Explode the 'images' column to handle nested lists
    units_df = units_df.explode('images')
    
    # Normalize the 'images' column and merge back to the main DataFrame
    images_df = pd.json_normalize(units_df['images'])
    units_df = units_df.drop(columns=['images'])
    result_df = pd.concat([units_df.reset_index(drop=True), images_df.reset_index(drop=True)], axis=1)
    df2 = result_df

    print(result_df.head())
    print(f"\nOld DataFrame shape: {df2.shape}")
    
    # Add a column for the date
    df2['Date'] = today
    df2.reset_index(drop=True)
          
    # Check if file exists and append or create new file
    if not os.path.isfile(filepath):
      result_df.to_csv(filepath, index=False)
    else:
      # read in existing file
      df = pd.read_csv(filepath)
      
      # Reset the index of both DataFrames to avoid reindexing issues
      df = df.reset_index(drop=True)
      df = df.dropna(how='all', axis=0).reset_index(drop=True)
      
      # extract headers before concatenating in numpy (numpy removes headers because it's an array, not a dataframe)
      headings = df.columns
      
      print(f"\nNew DataFrame shape: {df.shape}")

      # combined_df = pd.concat([df, df2], axis=0, ignore_index=True)
      dfs = [df, df2]
      combined_array = np.concatenate(dfs, axis=0)

      new_df = pd.DataFrame(combined_array, columns=headings)
      
      print(f"\nCombined DataFrame shape: {new_df.shape}")
      
      new_df.to_csv(filepath, index=None)

  except ValueError as e:
    print(f"Error parsing JSON data: {e}")

else:
    print(f"Failed to retrieve data: {response.status_code}")
