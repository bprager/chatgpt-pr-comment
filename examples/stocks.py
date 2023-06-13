#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yfinance as yf
import datetime


def get_stock_price(ticker):
    """Return the price of the given stock ticker."""
    ticker_data = yf.Ticker(ticker).info
    return ticker_data["regularMarketOpen"]


# get historical market data for the last 10 days
def get_stock_history(ticker, start_date, end_date):
    """Return the price of the given stock ticker."""
    ticker_data = yf.Ticker(ticker).history(start=start_date, end=end_date)
    return ticker_data


def main():
    """Main entry point for the script."""
    print("Stock price of GOOG: {}".format(get_stock_price("GOOG")))
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=10)
    print(
        "Stock price of GOOG: {}".format(
            get_stock_history("GOOG", start_date, end_date)
        )
    )


if __name__ == "__main__":
    main()
