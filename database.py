import pymongo
import myrequests
import bot
import time
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

LINK = os.getenv('DATABASE_LINK')

client = MongoClient(LINK)
database = client['Stock-bot']
collection = database['stocks']

def addStock(stockSymbol):
    data = myrequests.getAvg(stockSymbol)

    if(data['code'] == 404):
        return f"Couldn't find {stockSymbol.upper()}"

    for stock in collection.find():
        if(stock['symbol'] == data['meta']['symbol']):
            return f'{stockSymbol} already added'

    info = myrequests.getInfo(stockSymbol)

    avg = 0.0
    for i in range(7):
        avg += float(data['values'][0]['avg'])
    avg = avg / 7

    stock = {
        'name': info['data'][0]['instrument_name'],
        'symbol': data['meta']['symbol'],
        'exchange': info['data'][0]['exchange'],
        'avg': avg,
    }

    collection.insert_one(stock)
    return f'{stockSymbol.upper()} has been added'

def removeStock(stockSymbol):
    stockSymbol = stockSymbol.upper()
    result = collection.delete_one({'symbol': stockSymbol})

    if result.deleted_count > 0:
        return f'Stock with symbol {stockSymbol} has been removed'
    else:
        return f'Stock with symbol {stockSymbol} not found'

def updateStocks():
    updateMessage = "Update\n"
    for stock in collection.find():
        data = myrequests.getAvg(stock['symbol'])
        avg = 0.0
        for i in range(7):
            avg += float(data['values'][0]['avg'])
        avg = avg / 7

        if (float(data['values'][0]['avg']) - float(stock['avg'])) >= 3:
            updateMessage += f'{stock["symbol"]} with an 7 day average of {stock["avg"]} is now {data["values"][0]["avg"]}\n'

        collection.update_one(
            {'symbol': stock['symbol'].upper()},
            {'$set': {'avg': avg}}
        )
        print(stock['symbol'])
        time.sleep(10)

    bot.send_message('', updateMessage, False)
    return

def summary():
    return