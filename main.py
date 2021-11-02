import yfinance as yf
import yaml
import argparse
from munch import DefaultMunch
import psycopg2
from io import StringIO
import os
import pandas as pd


def args_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--symbol", help="Symbol name")
    parser.add_argument("-t", "--time_period", help="Time period")

    return parser.parse_args()


def load_config():
    config_dict = yaml.safe_load(open("config.yaml"))
    return DefaultMunch.fromDict(config_dict)


def fetch_ticker(symbol):
    return yf.Ticker(symbol)


def download_prices(ticker, period='2y', interval='60m', progress=False):
    """Download stock prices to a Pandas DataFrame"""

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
        "Datetime": "time",
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Adj Close": "close_adj",
        "Volume": "volume",
    })
    return df


def upload_to_timescale(df, config, table_name="stock_prices"):
    """
    Upload the stock price data to TimescaleDB as quickly and efficiently as possible
    by truncating (i.e. removing) the existing data and copying all-new data
    """

    with psycopg2.connect(
            host=config.POSTGRES_HOST,
            port=config.POSTGRES_PORT,
            dbname=config.POSTGRES_DB,
            user=config.POSTGRES_USER,
            password=config.POSTGRES_PASSWORD,
            connect_timeout=5
    ) as conn:
        with conn.cursor() as cursor:
            # Truncate the existing table (i.e. remove all existing rows)
            cursor.execute(f"TRUNCATE {table_name}")
            conn.commit()

            # Now insert the brand-new data
            # Initialize a string buffer
            sio = StringIO()
            # Write the Pandas DataFrame as a CSV file to the buffer
            sio.write(df.to_csv(index=None, header=None))
            # Be sure to reset the position to the start of the stream
            sio.seek(0)
            cursor.copy_from(
                file=sio,
                table=table_name,
                sep=",",
                null="",
                size=8192,
                columns=df.columns
            )
            conn.commit()
            print("DataFrame uploaded to TimescaleDB")


def main():
    config = load_config()
    # Download prices for the four stocks in which we're interested
    msft = download_prices("MSFT")
    tsla = download_prices("TSLA")

    # Append the four tables to each-other, one on top of the other
    df_all = pd.concat([msft, tsla])

    # Erase existing data and upload all-new data to TimescaleDB
    upload_to_timescale(df_all, config)

    print("All done!")


main()
