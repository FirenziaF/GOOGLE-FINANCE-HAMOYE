import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

companies = ['TSLA:NASDAQ','FNGD:NYSEARCA','NVDA:NASDAQ','RIVN:NASDAQ', 'U:NYSE','PLUG:NASDAQ','FUTU:NASDAQ','AAPL:NASDAQ','PYPL:NASDAQ','GRAB:NASDAQ','CCL:NYSE','SQ:NYSE','JD:NASDAQ','FRO:NYSE','AAL:NASDAQ','GOLD:NYSE','BABA:NYSE', 'BEKE:NYSE','AMD:NASDAQ','NOK:NYSE' ,'PDD:NASDAQ', 'F:NYSE', 'AMZN:NASDAQ','UPST:NASDAQ','EQNR:NYSE']
def company_scraper(company):
    try:
        # Define the user-agent for identifying the web scraping tool
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
        }

        # Construct the URL
        url = f"https://www.google.com/finance/quote/{company}"

        # Send an HTTP GET request to the URL
        r = requests.get(url, headers=header)

        # Check if the request was successful
        if r.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(r.text, "html.parser")

            # Scraping for company name
            company_name = soup.find("div", {"class": "zzDege"}).text

            # Scraping for company initials
            company_initials = soup.find("div", {"class": "PdOqHc"}).text.split('Home')[1]

            # Scraping for the price
            price = soup.find("div", {"class": "kf1m0"}).text

            # Scraping for the previous close
            Previous_close = soup.find("div", {"class": "P6K39c"}).text

            # Scraping for the market cap
            market_cap = soup.find_all("div", {"class": "P6K39c"})[3].text

            # Extracting the current date and time
            date = datetime.now().strftime("%Y-%m-%d_%H-%M")

            # Defining the data as a dictionary
            data = {
                'Company Name': [company_name],
                'Company Initials': [company_initials],
                'Price': [price],
                'Previous Close': [Previous_close],
                'Market Cap': [market_cap],
                'Date': [date]
            }

            return data
        else:
            print(f"Failed to retrieve data for {company}. Status Code: {r.status_code}")
            return None

    except Exception as e:
        print(f"An error occurred while scraping data for {company}: {str(e)}")
        return None
    
company_names = [company_scraper(company) for company in companies]
data = pd.DataFrame(company_names)
## First lets create a list of all columns in our dataframe
columns_df=["Company Name",	"Company Initials","Price",	"Previous Close", "Market Cap","Date"]
## Removing special characters from specified columns
data[columns_df] = data[columns_df].applymap(lambda x: str(x).replace('+', '').replace(',', '').replace('[', '').replace(']', '').replace('%', '').replace('USD','').replace('$',''))
data[columns_df] = data[columns_df].applymap(lambda x: x.replace("'", ''))
data[columns_df] = data[columns_df].applymap(lambda x: x.replace("'", ''))
data['Price'] = data['Price'].astype(float)
data['Previous Close'] = data['Previous Close'].astype(float)
data['price change'] = data['Price'] - data['Previous Close']
# Here, I created a CSV file name with the current date and time
csv_file = f'{datetime.now().strftime("%Y-%m-%d_%H-%M")} Google_Finance_Data.csv'

# Lastly, I saved the DataFrame to a CSV file, excluding the index column
data.to_csv(csv_file, index=False)