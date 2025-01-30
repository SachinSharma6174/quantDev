import unittest
import yfinance as yf
import numpy as np
import pandas as pd
from scipy.stats import norm
from quant_model.black_scholes import black_scholes, fetch_option_data, calculate_premiums

class TestBlackScholesModel(unittest.TestCase):

    def test_black_scholes_call(self):
        stock_price = 100
        strike_price = 100
        time_to_expiration = 1
        risk_free_rate = 0.05
        volatility = 0.2
        option_type = 'call'
        expected_price = 10.4506
        price = black_scholes(stock_price, strike_price, time_to_expiration, risk_free_rate, volatility, option_type)
        self.assertAlmostEqual(price, expected_price, places=4)

    def test_black_scholes_put(self):
        stock_price = 100
        strike_price = 100
        time_to_expiration = 1
        risk_free_rate = 0.05
        volatility = 0.2
        option_type = 'put'
        expected_price = 5.5735
        price = black_scholes(stock_price, strike_price, time_to_expiration, risk_free_rate, volatility, option_type)
        self.assertAlmostEqual(price, expected_price, places=4)

    def test_fetch_option_data(self):
        ticker_symbol = 'AAPL'
        expiration_date = '2023-12-15'
        calls = fetch_option_data(ticker_symbol, expiration_date)
        self.assertIsInstance(calls, pd.DataFrame)
        self.assertIn('strike', calls.columns)
        self.assertIn('lastPrice', calls.columns)

    def test_calculate_premiums(self):
        ticker_symbol = 'AAPL'
        expiration_date = '2023-12-15'
        risk_free_rate = 0.01
        stock = yf.Ticker(ticker_symbol)
        stock_price = stock.history(period='1d')['Close'].iloc[-1]
        calls = fetch_option_data(ticker_symbol, expiration_date)
        premiums = calculate_premiums(calls, stock_price, risk_free_rate, expiration_date)
        self.assertIsInstance(premiums, pd.DataFrame)
        self.assertIn('Premium', premiums.columns)
        self.assertTrue((premiums['Premium'] > 0).all())

if __name__ == '__main__':
    unittest.main()