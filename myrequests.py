import requests
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

KEY = os.getenv('API_KEY')

# retrieve data for the current day
def getData(stockSymbol):
    response = requests.get(f'https://api.twelvedata.com/time_series?symbol={stockSymbol}&interval=1day&apikey={KEY}')
    return response.json()

# retrieve basic info for stock
def getInfo(stockSymbol):
    response = requests.get(f'https://api.twelvedata.com/symbol_search?symbol={stockSymbol}')
    return response.json()

# retrieve avg prices for stock day
def getAvg(stockSymbol):
    response = requests.get(f'https://api.twelvedata.com/avg?symbol={stockSymbol}&interval=1day&apikey={KEY}')
    return response.json()

def stockInfo(stockSymbol):
    data = getData(stockSymbol)

    if(data['status'] == 'error'):
        return 'Stock symbol not found.'
    else:
        return f'''`Stock symbol: {data['meta']['symbol']}
Info for: {data['values'][0]['datetime']}
Open: {data['values'][0]['open']}
High: {data['values'][0]['high']}
Low: {data['values'][0]['low']}
Close: {data['values'][0]['close']}
Volume: {data['values'][0]['volume']}`'''
    
