import yfinance as yf


def download_prices(ticker, period, interval, progress=False):
    """Download stock prices from yahoo as pandas DataFrame"""

    df = yf.download(
        tickers=ticker,
        period=period,
        interval=interval,
        progress=progress
    )

    df = df.reset_index()  # remove the index
    df['ticker'] = ticker  # add a column for the ticker

    # Rename columns to match our database table
    df = df.rename(columns={
        "Date": "time",
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Adj Close": "close_adj",
        "Volume": "volume",
    })
    print(f"Downloaded {period} {ticker} stock data from yahoo")
    return df

