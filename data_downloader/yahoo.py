import yfinance as yf
import datetime
import logging


def download_prices(
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
