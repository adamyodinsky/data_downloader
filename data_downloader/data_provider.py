import datetime
import logging

import config
import pandas as pd
import yfinance as yf
from fred_extension import FredExtension as Fred


class DataProvider(object):
    REAL_TIME_MAX_DATE = '9999-12-31'

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
        df = df.reset_index(name="value").rename(columns={"index": "date"})
        df['m_type'] = 'GDP'
        return df

    def get_unemployment_data(self):
        df = self.fred.get_series_first_release('UNRATE')
        df = df.reset_index(name="value").rename(columns={"index": "date"})
        df['m_type'] = 'UNRATE'
        return df

    def get_inflation_data(self):
        df = self.fred.get_series_first_release('CPIAUCSL')
        df = df.reset_index(name="value").rename(columns={"index": "date"})
        df['m_type'] = 'CPIAUCSL'
        return df


    def get_consumer_sentiment_data(self):
        df = self.fred.get_series_first_release('UMCSENT')
        df = df.reset_index(name="value").rename(columns={"index": "date"})
        df['m_type'] = 'UMCSENT'

        # Replace NaT values with nulls
        df = df.where(pd.notnull(df), None)

        return df


    def get_interest_rate_data(self):
        start = '2020-01-01'
        end = self.REAL_TIME_MAX_DATE

        df = self.fred.get_series_first_release_by_dates('DFF', realtime_start=start, realtime_end=end)
        df = df.reset_index(name="value").rename(columns={"index": "date"})
        df['m_type'] = 'DFF'
        return df
    
    # def get_interest_rate_data(self):
    #     url = f"https://api.stlouisfed.org/fred/series/observations?series_id=DFF&api_key={config.fred_token}&file_type=json"
    #     response = requests.get(url)
    #     data = response.json()
    #     df = pd.DataFrame(data["observations"])
    #     df["date"] = pd.to_datetime(df["date"])
    #     df = df.set_index("date")
    #     df = df.drop(columns=["realtime_start", "realtime_end"])
    #     df = df.rename(columns={"value": "interest_rate"})
    #     return df