import config
import datetime
import logging
import pandas as pd
import click
from data_provider import DataProvider
from dateutil.relativedelta import relativedelta
from timescale import TmDB


def _get_stock_data(
    current_date,
    data_interval: str,
    data_period: int,
    ticker: str,
    db: TmDB,
    dp: DataProvider,
):
    start = _get_starting_date(db, ticker, data_period, current_date)

    # Download stock data and save into DB
    if start != current_date:  # prevent an unneeded API calls
        ticker_data = dp.download_prices(
            ticker=ticker,
            start=start,
            end=current_date,
            interval=data_interval,
        )
        logging.info(f"Uploading {ticker} data to DB.")
        db.upsert_data(df=ticker_data, table=config.db_stock_price_table)
    else:
        logging.info(f"{ticker} Is up to date, no action needed.")

    logging.info("Data updated successfully.")


def _get_starting_date(db: TmDB, ticker: str, data_period: str, current_date):
    """Get the first date from where we want the data series we downloading will begin from.
    If there is no data at all, it will download the data by the DATA_PERIOD env variable.
    If there is data, but there is a new data that should be downloaded, or the data_period is going further back from our oldest data_point, the missing data will be downloaded and added to the existing data.
    """

    start = None
    first_data_point_date = db.get_first(
        table=config.db_stock_price_table, ticker=ticker
    )
    last_data_point_date = db.get_last(table=config.db_stock_price_table, ticker=ticker)
    period_date = (
        current_date - relativedelta(years=data_period) + relativedelta(weeks=1)
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


@click.group()
@click.option(
    "-p",
    "--data-period",
    type=int,
    default=None,
    help="How many years back to get data from. (<number>y).",
)
@click.option(
    "-i",
    "--data-interval",
    type=str,
    default=None,
    help="Intervals of data points, <number>h for hours, <number>d for days.",
)
@click.pass_context
def cli(ctx, data_period: int = None, data_interval: str = None):
    ctx.ensure_object(dict)
    # Load env variables from .env file
    # utils.check_env_vars()

    # Set logger configuration
    logging.basicConfig(
        format="%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
        datefmt="%Y-%m-%d:%H:%M:%S",
        level=logging._nameToLevel[config.log_level],
    )

    # Give priority to cli inputs over env variables
    ctx.obj["data_period"] = data_period or config.data_period
    ctx.obj["data_interval"] = data_interval or config.data_interval
    ctx.obj["current_date"] = datetime.date.today()
    ctx.obj["db"] = TmDB()
    ctx.obj["dp"] = DataProvider()

    return ctx


@click.command(help=f"Download historical price data for a list of stocks.")
@click.option(
    "-n",
    "--number-of-tickers",
    type=int,
    default=None,
    help="Number of tickers to iterate over.",
)
@click.option(
    "-t",
    "--tickers",
    type=str,
    default=None,
    help="List of tickers to iterate over, separated with whitespace.",
)
@click.pass_context
def get_stocks_data(ctx, tickers: str = None, number_of_tickers: int = None):
    # Priority to cli inputs over env variables, last priority is from a DB table
    number_of_tickers = number_of_tickers or int(config.number_of_tickers)
    tickers = tickers or config.tickers

    # If there is a tickers string from the cli input or from env variable, split it to a list
    # Else, get and map a list from the DB tickers table.
    tickers = (
        tickers.split()
        if tickers
        else list(map(lambda t: t[0], ctx.obj["db"].get_tickers_list()))
    )

    # Download stocks data and save into DB
    for index, ticker in enumerate(tickers):
        # A limit for a number of stocks we get data on from the tickers list
        # This probably will be used only in dev.
        if number_of_tickers and index >= number_of_tickers:
            break

        _get_stock_data(
            ticker=ticker,
            data_period=ctx.obj["data_period"],
            data_interval=ctx.obj["data_interval"],
            current_date=ctx.obj["current_date"],
            db=ctx.obj["db"],
            dp=ctx.obj["dp"],
        )

    logging.info("Stocks data updated successfully.")


@click.command(help=f"Download a specific stock historical price data")
@click.option("-t", "--ticker", type=str, help="A single stock ticker", required=True)
@click.pass_context
def get_stock_data(ctx: click.Context, ticker: str):
    _get_stock_data(
        ticker=ticker,
        data_period=ctx.obj["data_period"],
        data_interval=ctx.obj["data_interval"],
        current_date=ctx.obj["current_date"],
        db=ctx.obj["db"],
        dp=ctx.obj["dp"],
    )


@click.command(help=f"Download Macro Economics historical data")
@click.pass_context
def get_macros_data(ctx):
    """Download macro-economics data and save into the DB"""

    dp: DataProvider = ctx.obj["dp"]
    db: TmDB = ctx.obj["db"]

    for indicator in DataProvider.DAILY_MACRO_INDICATORS:
        df = dp.get_daily_macro_data_2(indicator)
        db.upsert_data(df, config.macro_table)
        logging.info(f"{indicator} data updated successfully.")

    for indicator in DataProvider.MACRO_INDICATORS:
        df = dp.get_macro_data(indicator)
        db.upsert_data(df, config.macro_table)
        logging.info(f"{indicator} data updated successfully.")

    logging.info("Macro data updated successfully.")


cli.add_command(get_stocks_data)
cli.add_command(get_stock_data)
cli.add_command(get_macros_data)

cli()
