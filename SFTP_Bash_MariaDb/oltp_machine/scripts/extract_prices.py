import pandas as pd
import yfinance as yf
import datetime as DT
import configparser
import os
import sys

os.chdir(os.path.dirname(sys.argv[0]))

today = DT.date.today().strftime("%Y-%m-%d")

week_ago = (DT.date.today() - DT.timedelta(days=7)).strftime("%Y-%m-%d")

data  = yf.download(tickers="msft aapl goog tsla",
					start=week_ago,
					end=today,
					interval = "1m")

data['Adj Close'].to_csv('../data/data.csv')