import yfinance as yf
import numpy as np
import pandas as pd
from scipy.stats import norm

def black_scholes(stock_price, strike_price, time_to_expiration, risk_free_rate, volatility, option_type='call'):
    d1 = (np.log(stock_price / strike_price) + (risk_free_rate + 0.5 * volatility ** 2) * time_to_expiration) / (volatility * np.sqrt(time_to_expiration))
    d2 = d1 - volatility * np.sqrt(time_to_expiration)
    if option_type == 'call':
        price = stock_price * norm.cdf(d1) - strike_price * np.exp(-risk_free_rate * time_to_expiration) * norm.cdf(d2)
    else:
        price = strike_price * np.exp(-risk_free_rate * time_to_expiration) * norm.cdf(-d2) - stock_price * norm.cdf(-d1)
    return price

def fetch_option_data(ticker_symbol, expiration_date):
    stock = yf.Ticker(ticker_symbol)
    options_chain = stock.option_chain(expiration_date)
    return options_chain.calls

def calculate_premiums(calls, stock_price, risk_free_rate, expiration_date):
    time_to_expiration = (pd.to_datetime(expiration_date) - pd.Timestamp.today()).days / 365
    strike_prices = calls['strike'].values
    volatilities = calls['impliedVolatility'].values
    calls['BS_Price'] = black_scholes(stock_price, strike_prices, time_to_expiration, risk_free_rate, volatilities)
    calls['Premium'] = calls['lastPrice'] - calls['BS_Price']
    return calls[calls['Premium'] > 0]

def main(ticker_symbol, expiration_date, risk_free_rate=0.01):
    stock = yf.Ticker(ticker_symbol)
    stock_price = stock.history(period='1d')['Close'].iloc[-1]
    calls = fetch_option_data(ticker_symbol, expiration_date)
    good_premium_options = calculate_premiums(calls, stock_price, risk_free_rate, expiration_date)
    print(good_premium_options[['contractSymbol', 'strike', 'lastPrice', 'BS_Price', 'Premium']])

if __name__ == '__main__':
    ticker_symbol = 'NVDA'
    expiration_date = '2025-01-31'  # Example expiration date
    main(ticker_symbol, expiration_date)