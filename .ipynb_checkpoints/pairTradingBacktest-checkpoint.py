import numpy as np
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

data = yf.download(tickers='BAC', period='YTD', interval='1d')

fig = go.Figure(data=[go.Candlestick(x=data.index,
                open=data.Open,
                high=data.High,
                low=data.Low,
                close=data.Close)])
fig.show()