import datetime
import logging

import config
import pandas as pd
import requests
import yfinance as yf
from fred_extension import FredExtension as Fred


class DataProvider(object):
    REAL_TIME_MAX_DATE = '9999-12-31'
    MACRO_INDICATORS = ['GDP', 'UNRATE', 'CPIAUCSL', 'PPIACO', 'UMCSENT', 'M1', 'M2']
    DAILY_MACRO_INDICATORS = ['DGS10', 'VIXCLS', 'DFF']

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
        df = self.fred.get_series_first_release(m_type)
        df = df.reset_index(name="value").rename(columns={"index": "date"})
        df = df.where(pd.notnull(df), None)
        df['m_type'] = m_type
        return df


    def get_daily_macro_data(self, m_type):
        start = datetime.date.today().strftime('%Y-%m-%d')
        end = start

        df = self.fred.get_series_first_release_by_dates(m_type, realtime_start=start, realtime_end=end)
        df = df.reset_index(name="value").rename(columns={"index": "date"})
        df['m_type'] = m_type
        return df


    
    
    def get_cik(symbol):
        # Set the URL for the CIK data
        url = "https://data.sec.gov/submissions/{}.json".format(symbol)
        
        # Make the request and retrieve the data
        response = requests.get(url)
        data = response.json()
        
        # Extract the CIK from the JSON data
        cik = data['cik']
        
        return cik

    def get_financial_data(reporting_year, symbol):
        # Get the CIK for the stock
        cik = get_cik(symbol)
        
        # Set the URL for the financial data
        url = "https://data.sec.gov/api/xbrl/companyconcept/{}/us-gaap/AssetsCurrent.json".format(cik)
        
        # Make the request and retrieve the data
        response = requests.get(url)
        data = response.json()
        
        # Extract the financial data from the JSON object
        df = pd.DataFrame(data['facts'])
        
        # Filter the data to include only the specified reporting year
        df = df[df['context'].str.contains(reporting_year)]
        
        # Return the financial data
        return df
