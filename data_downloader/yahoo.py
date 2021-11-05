import yfinance as yf
import datetime
import logging


def download_prices(ticker: str, start: datetime.date = None, end: datetime.date = None,
                    period: str = '5y', interval: str = '1d', progress=False):
    """Download stock prices from yahoo as pandas DataFrame"""

    if start is None:
        df = yf.download(
            tickers=ticker,
            period=period,
            interval=interval,
            progress=progress)
    else:
        df = yf.download(
            tickers=ticker,
            start=start,
            end=end,
            interval=interval,
            progress=progress)

    df = df.reset_index()  # remove the index
    df['ticker'] = ticker  # add a column for the ticker

    # Rename columns to match our database table
    df = df.rename(columns={
        "Date": "date",
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Adj Close": "close_adj",
        "Volume": "volume",
    })

    if start is None:
        logging.info(f"Downloaded '{ticker}' {period} data from yahoo.")
    else:
        logging.info(f"Downloaded '{ticker}' ({start}-{end}) data from yahoo.")
    return df
