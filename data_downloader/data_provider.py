import datetime
import logging

import config
import pandas as pd
import yfinance as yf
from fred_extension import FredExtension as Fred


class DataProvider(object):
    REAL_TIME_MAX_DATE = '9999-12-31'
    MACRO_INDICATORS = ['GDP', 'UNRATE', 'CPIAUCSL', 'PPIACO', 'UMCSENT', 'M1', 'M2', 'DGS10']

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

    
    # and returns the data for that indicator
    def get_macro_data(self, m_type):
        df = self.fred.get_series_first_release('GDP')
        df = df.reset_index(name="value").rename(columns={"index": "date"})
        df = df.where(pd.notnull(df), None)
        df['m_type'] = 'GDP'
        return df

    # TODO: check the date range
    def get_10yr_treasury_data(self):
        start = '2020-01-01'
        end = self.REAL_TIME_MAX_DATE

        df = self.fred.get_series_first_release_by_dates('DGS10', realtime_start=start, realtime_end=end)
        df = df.reset_index(name="value").rename(columns={"index": "date"})
        df['m_type'] = 'DGS10'
        df = df.where(pd.notnull(df), None)
        return df

    # TODO: check the date range
    def get_interest_rate_data(self):   
        start = '2020-01-01'
        end = self.REAL_TIME_MAX_DATE

        df = self.fred.get_series_first_release_by_dates('DFF', realtime_start=start, realtime_end=end)
        df = df.reset_index(name="value").rename(columns={"index": "date"})
        df['m_type'] = 'DFF'
        return df
    