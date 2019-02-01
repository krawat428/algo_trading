#!/usr/bin/env python3
from upstox_api.api import *
import datetime
import time

api_key = ''
path='/home/ec2-user/upstox/'
#path=''
#xls_file=str(time.ctime()).replace(' ', '_')
#i=0
def get_token():
    with open(path+'token.txt', 'r') as f:
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


def order_execution_cover(exchange,instrument_name,data):
    instrument_variable=instrument(exchange,instrument_name)
    global order
            
    if data['open'] > data['close']:
        order=u.place_order(TransactionType.Buy,  # transaction_type
                      u.get_instrument_by_symbol(exchange, instrument_name),
                      1,  # quantity
                      OrderType.Market,  # order_type
                      ProductType.CoverOrder,  # product_type
                      0.0,  # price
                      float(data['open']-1),  # trigger_price Here the trigger_price is taken as stop loss (provide stop loss in actual amount)
                      0,  # disclosed_quantity
                      DurationType.DAY,  # duration
                      None,  # stop_loss
                      None,  # square_off
                      None)  # trailing_ticks
                    
    elif data['open'] < data['close']:
        order=u.place_order(TransactionType.Sell,  # transaction_type
                      u.get_instrument_by_symbol(exchange, instrument_name),
                      1,  # quantity
                      OrderType.Market,  # order_type
                      ProductType.CoverOrder,  # product_type
                      0.0,  # price
                      float(data['open']+1),  # trigger_price Here the trigger_price is taken as stop loss (provide stop loss in actual amount)
                      0,  # disclosed_quantity
                      DurationType.DAY,  # duration
                      None,  # stop_loss
                      None,  # square_off
                      None)  # trailing_ticks
    
        
    elif data['open'] == data['close']:
        order="No gap Up/No gap Down"
        print("No gap Up/No gap Down")
    else:
        order="Error"
        print("Error")
    
    
    return(order)

def order_output(order):
    with open(path+'order.txt', 'w') as o:
        o.write(str(order))
    print("END")

def xls_write(value,column_number,i):
    sheet1.write(i,column_number,value)
    wb.save(xls_file+'.xls')

    
def execute(data,execute_time):
    if datetime.datetime.fromtimestamp(int(data['timestamp'])/1000)>execute_time:
        print('hello')
        order=order_execution_cover('MCX_FO','copper19febfut',data)
        order_output(order)
        print(order)
        u.unsubscribe(instrument('MCX_FO','copper19febfut'), LiveFeedType.Full)
        
    
def event_handler_quote_update(message):
    global data
    data={}
    data['ltp']=message['ltp']
    data['timestamp']=message['timestamp']
    data['close']=message['close']
    data['open']=message['open']

    execute(data,execute_time)
    print(data)
    

if __name__ == "__main__":
    access_token=get_token()
    u = Upstox(api_key,access_token)
    fetch_index()
    #start_time=custom_time(9,0,2)
    global execute_time
    execute_time=custom_time(9,0,0)
    end_time=custom_time(9,2,0)

    u.set_on_quote_update(event_handler_quote_update)
    u.subscribe(instrument('MCX_FO','copper19febfut'), LiveFeedType.Full)
    u.start_websocket(False)

    
    
    
    
    
