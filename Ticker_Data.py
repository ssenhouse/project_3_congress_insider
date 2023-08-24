import os
import pandas as pd
import numpy.random as rnd
import warnings
import json
import requests
import sqlalchemy as sql
import datetime
import yfinance as yf
import numpy as np


# Date range
today = datetime.date.today()
start_date = today - datetime.timedelta(days=365*3) #trading days(252) * amount of years to go back 

start = start_date.strftime("%Y-%m-%d")
end = today.strftime("%Y-%m-%d")


url = "https://api.quiverquant.com/beta/bulk/congresstrading"

headers = {
    "Accept": "application/json",
    "Authorization": "Bearer 77edeff3a3bd2fa2e10472e0536c0d166c147afa"
}

response = requests.get(url, headers=headers).json()

list_series = []

for row in response:
    list_series.append(pd.Series(row))
    column_names = response

congress_df = pd.DataFrame(data=list_series)

#Filter for TransationDate within the last year
congress_df = congress_df[congress_df['TransactionDate'] > start]

#Create a list of all items in the column "Ticker" in the dataframe
ticker_list = congress_df["Ticker"].tolist()
#Remove duplicates from the list
ticker_list = list(dict.fromkeys(ticker_list))

ticker_list = [w.replace('BRK.A', 'BRK-A') for w in ticker_list]
ticker_list = [w.replace('BRK.B', 'BRK-B') for w in ticker_list]
ticker_list = [w.replace('FB', 'META') for w in ticker_list]
ticker_list = [w.replace('BF.B', 'BF-B') for w in ticker_list]
ticker_list = [w.replace('LGF.B', 'LGF-B') for w in ticker_list]
ticker_list = [w.replace('KMI.W', 'KMI-W') for w in ticker_list]
ticker_list = [w.replace('CWEN.A', 'CWEN-A') for w in ticker_list]
ticker_list = [w.replace('ABB', 'ABBNY') for w in ticker_list]
ticker_list = [w.replace('RTN', 'RTX') for w in ticker_list]
ticker_list = [w.replace('INSW.V', 'INSW-V') for w in ticker_list]
ticker_list = [w.replace('FMBA', 'FMAO') for w in ticker_list]
ticker_list = [w.replace('ESALY', 'ESALF') for w in ticker_list]
ticker_list = [w.replace('RDSMY', 'RDSMF') for w in ticker_list]


# Downloading data
og_data = yf.download(ticker_list, start = start, end = end)




