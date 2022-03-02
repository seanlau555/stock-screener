# Imports
from pandas_datareader import data as pdr
from yahoo_fin import stock_info as si
from pandas import ExcelWriter
import yfinance as yf
import pandas as pd
import datetime
import time


# # Variables
# # Tickers get

# # Save list to csv
data = pd.read_csv("./selected_hk_stock_2022-03-01.csv", header=0)
tickers = [
    item.lstrip("0") + ".HK" for item in data.Stock
]  # Yahoo Finance uses dashes instead of dots
tickers = [ele.replace(".HK", "") for ele in tickers]
tickers = ["HKEX:" + str(ele) for ele in tickers]
# tickers = [
#     item for item in data.Ticker
# ]  # Yahoo Finance uses dashes instead of dots
dict = {"Symbol": tickers}
df = pd.DataFrame(dict)
df.to_csv("./output.csv")
