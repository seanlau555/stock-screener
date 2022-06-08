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
# data = pd.read_csv("./selected_hk_stock_2022-03-01.csv", header=0)
data = pd.read_csv("./hongkong_2022-06-01.csv", header=0)
tickers = [
    str(item).zfill(4) + ".HK" for item in data.Ticker
]  # Yahoo Finance uses dashes instead of dots
# tickers = [ele.replace(".HK", "") for ele in data.Ticker]
# tickers = ["HKEX:" + str(ele) for ele in data.Ticker]
# tickers = [
#     item for item in data.Ticker
# ]  # Yahoo Finance uses dashes instead of dots
dict = {"Symbol": tickers}
df = pd.DataFrame(dict)
df.to_csv("./tickers_hk.csv")
# df.to_csv("./output.csv")
