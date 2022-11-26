from timescale import TmDB
import yahoo
import utils
import datetime
from dateutil.relativedelta import relativedelta
import logging
import os
import click


@click.group()
@click.option('-p', '--data-period', type=int, default=None, help='How many years back to get data from. (<number>y).')
@click.option('-i', '--data-interval', type=str, default=None, help='Intervals of data points, <number>h for hours, <number>d for days.')
@click.pass_context
def cli(ctx: click.Context, data_period: int = None, data_interval: str = None):
    # Load env variables from .env file
    utils.load_env("files/.env")

    data_period = data_period or os.environ.get("DATA_PERIOD")
    data_interval = data_interval or os.environ.get("DATA_INTERVAL")

    db = TmDB()
    # Set logger configuration
    logging.basicConfig(
        format="%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
        datefmt="%Y-%m-%d:%H:%M:%S",
        level=logging.INFO,
    )



def _get_starting_date(db: TmDB, ticker: str, data_period: str, current_date):
    """Get the first date from where we want the data series we downloading will begin from.
    If there is no data at all, it will download the data by the DATA_PERIOD env variable.
    If there is data, but there is a new data that should be downloaded, or the data_period is going further back from our oldest data_point, the missing data will be downloaded and added to the existing data.
    """

    start = None
    first_data_point_date = db.get_first(
        table=os.environ.get("DB_STOCK_PRICE_TABLE"), ticker=ticker
    )
    last_data_point_date = db.get_last(
        table=os.environ.get("DB_STOCK_PRICE_TABLE"), ticker=ticker
    )
    period_date = (
        current_date
        - relativedelta(years=data_period)
        + relativedelta(weeks=1)
    )

    # if period go further in the past compared to the oldest record, use period
    # else, use the last data-point date as a starting point which is the most fresh data point.
    if last_data_point_date is not None:
        if period_date < first_data_point_date[1]:
            start = period_date
        else:
            start = last_data_point_date[1]
    else:
        start = period_date

    return start


@click.command(
    help=f"Download stock historical price data"
)
@click.option('-n', '--number-of-tickers', type=int, default=None, help='Number of tickers to iterate over.')
def download_data(number_of_tickers: int = None, data_period: int = None, data_interval: str = None):
    # Give priority for the cli input over env variables
    number_of_tickers = number_of_tickers or os.environ.get("NUMBER_OF_TICKERS")
    


    current_date = datetime.date.today()

    # Prepare stock tickers to iterate over and get their data
    db = TmDB()
    tickers = db.get_tickers_list()

    # Download stocks data and save into DB
    for index, ticker in enumerate(tickers):
        # a limit for a number of stocks we want to get data on from the list, this probably be used only in dev.
        if number_of_tickers and index >= number_of_tickers:
            break

        start = _get_starting_date(db, ticker[0], data_period, current_date)

        if start != current_date:  # prevent an API call when there is no need
            tickers_data = yahoo.download_prices(
                ticker=ticker[0],
                start=start,
                end=current_date,
                interval=data_interval,
            )
            logging.info(f"Uploading {ticker[0]} data to DB.")
            db.upsert_data(
                df=tickers_data, table=os.environ.get("DB_STOCK_PRICE_TABLE")
            )
        else:
            logging.info(f"{ticker[0]} Is up to date, no action needed.")

    logging.info("Data updated successfully.")


def download_ticker_data(ticker: str, data_period: int = None, data_interval: str = None):
    # Give priority for the cli input over env variables
    data_period = data_period or os.environ.get("DATA_PERIOD")
    data_interval = data_interval or os.environ.get("DATA_INTERVAL")
    current_date = datetime.date.today()

    
    # Download stocks data and save into DB
    
    start = _get_starting_date(db, ticker[0], data_period, current_date)

    if start != current_date:  # prevent an API call when there is no need
        ticker_data = yahoo.download_prices(
            ticker=ticker,
            start=start,
            end=current_date,
            interval=data_interval,
        )
        logging.info(f"Uploading {ticker} data to DB.")
        db.upsert_data(
            df=ticker_data, table=os.environ.get("DB_STOCK_PRICE_TABLE")
        )
    else:
        logging.info(f"{ticker} Is up to date, no action needed.")

    logging.info("Data updated successfully.")


cli.add_command(download_data)

cli()
