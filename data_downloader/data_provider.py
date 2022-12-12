import yfinance as yf
from fredapi import Fred
import datetime
import logging
import config


class DataProvider(object):
    def __init__(self):
        self.fred = Fred(api_key=config.fred_token)


    def get_stock_data(
        self,
        ticker: str,
        interval: str,
        start: datetime.date,
        end: datetime.date,
        progress=False,
    ):
        """Download stock prices from yahoo as pandas DataFrame"""

        try:
            df = yf.download(
                tickers=ticker, start=start, end=end, interval=interval, progress=progress
            )

            df = df.reset_index()  # remove the index
            df["ticker"] = ticker  # add a column for the ticker

            # Rename columns to match our database table
            df = df.rename(
                columns={
                    "Date": "date",
                    "Open": "open",
                    "High": "high",
                    "Low": "low",
                    "Close": "close",
                    "Adj Close": "close_adj",
                    "Volume": "volume",
                }
            )
            logging.info(
                f"Downloaded data from yahoo for '{ticker}' from {start} to {end}."
            )
        except Exception as e:
            logging.error(
                f"{e.__class__} occurred while trying to download data from yahoo for '{ticker}' from ({start} to {end} ."
            )
            logging.error(e)
        return df


    def get_gdp_data(self):
        df = self.fred.get_series_first_release('GDP')
        return df
