import pandas as pd 
import numpy as np
import matplotlib
import cryptocompare as cp
import datetime 
import requests
import json
from datetime import datetime

trades= pd.read_csv('C:\\Users\\kille\\Documents\\Python project\\Portoflio screener\Trade_history.csv',header=0, index_col=0, parse_dates=False, na_values=-99.99)
trades #Reading in your trade history

def crypto_amount(from_sym='',account=''):
    deps = trades.loc[trades['To']==from_sym] #Separating buys from sells
    wdrwls = trades.loc[trades['From']==from_sym]
    if account:
        deps = deps.loc[deps['Account']==account]
        wdrwls = wdrwls.loc[wdrwls['Account']==account]
        
    amount= (deps['Amount'].sum())-(wdrwls['Paid'].sum())
    return amount

def get_current_price(from_sym='BTC', to_sym='USD', exchange=''):
    url = 'https://min-api.cryptocompare.com/data/price'    
    
    parameters = {'fsym': from_sym,
                  'tsyms': to_sym }
    
    if exchange:
        print('exchange: ', exchange)
        parameters['e'] = exchange
        
    # response comes as json
    response = requests.get(url, params=parameters)   
    data = response.json()[to_sym]
    
    return data
    
def crypto_value(from_sym='BTC', to_sym='USD', exchange='', account=''):
    url = 'https://min-api.cryptocompare.com/data/price'    
    
    deps = trades.loc[trades['To']==from_sym]
    wdrwls = trades.loc[trades['From']==from_sym]
    
    parameters = {'fsym': from_sym,
                  'tsyms': to_sym }
    if account:
        deps = deps.loc[deps['Account']==account]
        wdrwls = wdrwls.loc[wdrwls['Account']==account]
        
    if exchange:
        parameters['e'] = exchange
        
    # response comes as json
    response = requests.get(url, params=parameters)   
    data = response.json()[to_sym]
    amount= (deps['Amount'].sum())-(wdrwls['Paid'].sum())
    return data*amount  
     
s=sorted(set(trades['To'].to_list()))
df=pd.DataFrame(list(s))
del df[0]
df['Asset']=pd.DataFrame(list(s))
df['Amount'] = list(map(lambda x: crypto_amount(x),df['Asset']))
df['Market Price']=list(map(lambda x: get_current_price(x,'GBP'),df['Asset'])) #I use GBP as it is my home currency however this works with USD and other currencies too!
df['GBP Value'] =list(map(lambda x: crypto_value(x,'GBP'),df['Asset']))
print("Profit/Loss is £", df['GBP Value'].sum(), "as of", datetime.now())
print(df)