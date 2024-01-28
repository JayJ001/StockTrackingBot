import random
import myrequests
import database

def handle_response(message: str) -> str:
    p_message = message.lower();
    
    if p_message == 'roll':
        return str(random.randint(1, 6))
    
    if p_message == 'help':
        return '''`Try the following commands:
!search {stock symbol}` to get info on a stock
!add {stock symbol} to add stock to watchlist
!remove {stock symbol} to remove stock from watchlist`'''
    
    if p_message[:6] == 'search':
        return myrequests.stockInfo(p_message[7:])
    
    if p_message[:3] == 'add':
        return database.addStock(p_message[4:])
    
    if p_message[:6] == 'remove':
        return database.removeStock(p_message[7:])
    
    return 'Invalid command. Try !help for help.'
