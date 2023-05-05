import pandas as pd
import sqlite3
import requests

# Read the list of companies from the config file
with open('config.txt') as f:
    companies = [line.strip() for line in f]

# Define the database connection
conn = sqlite3.connect('finance_data.db')

# Loop through each company and download the data
for company in companies:
    url = f'https://finance.yahoo.com/quote/{company}/history?p={company}'
    url_link =  requests.get(url,headers ={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
    df = pd.read_html(url_link.text)[0]

    
    # Clean up the column names
    df.columns = [col.lower().replace(' ', '_') for col in df.columns]
    
    # Insert the data into the database
    df.to_sql(name='finance_data', con=conn, if_exists='append', index=False)
    
conn.close()
