#!/usr/bin/env python3
from upstox_api.api import *
import datetime
import time

api_key = ''

def get_token():
    with open('token.txt', 'r') as f:
      access_token=f.read()
      return(access_token)

def fetch_index():    
    u.get_master_contract('MCX_FO')
    u.get_master_contract('MCX_INDEX') 
    
def instrument(exchange,symbol):
    a=u.get_instrument_by_symbol(exchange, symbol)
    return(a)
    
def live_feed(variable):
    a=u.get_live_feed(variable, LiveFeedType.Full)
    return(a)
    
def custom_time(hour,minutes,second):
    now = datetime.datetime.now()
    custom_time = now.replace( hour=hour, minute=minutes, second=second, microsecond=0)
    return(custom_time)
    
def live_time(variable):
    a=instrument(variable, LiveFeedType.Full)
    return(int(a['ltt'])/1000)

def order_execution(exchange,instrument_name,execute_time):
    instrument_variable=instrument(exchange,instrument_name)
    while True:
        data=live_feed(instrument_variable)
        ltt=datetime.datetime.fromtimestamp(int(data['ltt'])/1000)
        if ltt > execute_time:
            
            if data['open'] > data['close']:
                order=u.place_order(TransactionType.Buy,
                                    u.get_instrument_by_symbol(exchange, instrument_name),
                                    1,
                                    OrderType.Market,
                                    ProductType.Intraday)
            
            elif data['open'] < data['close']:
                order=u.place_order(TransactionType.Buy,
                                    u.get_instrument_by_symbol(exchange, instrument_name),
                                    1,
                                    OrderType.Market,
                                    ProductType.Intraday)
                
            elif data['open'] == data['close']:
                order="No gap Up/No gap Down"
                print("No gap Up/No gap Down")
            else:
                order="Error"
                print("Error")
            break
        print(ltt)
        time.sleep(0.5)
    return(order)

if __name__ == "__main__":
    access_token=get_token()
    u = Upstox(api_key,access_token)
    fetch_index()
    
    execute_time=custom_time(18,36,0)
    order=order_execution('MCX_FO','copper19febfut',execute_time)
    
    with open('order.txt', 'w') as o:
        o.write(str(order))
    
    print("END")
    
    
