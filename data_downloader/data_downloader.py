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
def cli(ctx, data_period: int = None, data_interval: str = None):
    # Load env variables from .env file
    utils.load_env("files/.env")

    # Set logger configuration
    logging.basicConfig(
        format="%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
        datefmt="%Y-%m-%d:%H:%M:%S",
        level=logging.INFO,
    )

    ctx.obj["data_period"] = data_period or os.environ.get("DATA_PERIOD")
    ctx.obj["data_interval"] = data_interval or os.environ.get("DATA_INTERVAL")
    ctx.obj["current_date"] = datetime.date.today()
    ctx.obj["db"] = TmDB()
    

@click.command(
    help=f"Download historical price data for a list of stocks"
)
@click.option('-n', '--number-of-tickers', type=int, default=None, help='Number of tickers to iterate over.')
def get_stocks_data(ctx, number_of_tickers: int = None):
    number_of_tickers = number_of_tickers or os.environ.get("NUMBER_OF_TICKERS")
    tickers = ctx.obj["db"].get_tickers_list()

    # Download stocks data and save into DB
    for index, ticker in enumerate(tickers):
        # a limit for a number of stocks we want to get data on from the list, this probably be used only in dev.
        if number_of_tickers and index >= number_of_tickers:
            break

        get_stock_data(ctx, ticker[0])

    logging.info("Stocks data updated successfully.")


@click.command(
    help=f"Download a specific stock historical price data"
)
@click.option('-t', '--ticker', type=str, help="Stock ticker")
def get_stock_data(ctx, ticker: str):
    start = utils.get_starting_date(ctx.obj["db"], ticker, ctx.obj["data_period"], ctx.obj["current_date"])

    # Download stock data and save into DB
    if start != ctx.obj["current_date"]:  # prevent an API call when there is no need
        ticker_data = yahoo.download_prices(
            ticker=ticker,
            start=start,
            end=ctx.obj["current_date"],
            interval=ctx.obj["data_interval"],
        )
        logging.info(f"Uploading {ticker} data to DB.")
        ctx.obj["db"].upsert_data(
            df=ticker_data, table=os.environ.get("DB_STOCK_PRICE_TABLE")
        )
    else:
        logging.info(f"{ticker} Is up to date, no action needed.")

    logging.info("Data updated successfully.")


cli.add_command(get_stocks_data)
cli.add_command(get_stock_data)

cli()
