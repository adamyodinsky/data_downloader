from timescale import TmDB
import yahoo
import utils
import datetime
import logging
import os
import click


@click.group()
@click.option('-p', '--data-period', type=int, default=None, help='How many years back to get data from. (<number>y).')
@click.option('-i', '--data-interval', type=str, default=None, help='Intervals of data points, <number>h for hours, <number>d for days.')
@click.pass_context
def cli(ctx, data_period: int = None, data_interval: str = None):
    ctx.ensure_object(dict)
    # Load env variables from .env file
    utils.load_env(os.environ.get("ENV_FILE_PATH"))

    # Set logger configuration
    logging.basicConfig(
        format="%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
        datefmt="%Y-%m-%d:%H:%M:%S",
        level=logging.INFO,
    )

    # Give priority to cli inputs over env variables
    ctx.obj["data_period"] = data_period or int(os.environ.get("DATA_PERIOD"))
    ctx.obj["data_interval"] = data_interval or os.environ.get("DATA_INTERVAL")
    ctx.obj["current_date"] = datetime.date.today()
    ctx.obj["db"] = TmDB()

    return ctx
    

@click.command(
    help=f"Download historical price data for a list of stocks"
)
@click.option('-n', '--number-of-tickers', type=int, default=None, help='Number of tickers to iterate over.')
@click.option('-t', '--tickers', type=str, default=None, help='List of tickers to iterate over, separated with whitespace.')
@click.pass_context
def get_stocks_data(ctx, tickers: str = None, number_of_tickers: int = None):
    # Give priority to cli inputs over env variables
    number_of_tickers = number_of_tickers or int(os.environ.get("NUMBER_OF_TICKERS"))
    tickers = tickers or (os.environ.get("TICKERS"))

    # If there is a tickers string from the cli input or from env variable, split it to a list
    # Else, get and map a list from the DB tickers table.
    tickers = tickers.split() if tickers else list(map(lambda t: t[0], ctx.obj["db"].get_tickers_list()))

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
        )

    logging.info("Stocks data updated successfully.")


@click.command(
    help=f"Download a specific stock historical price data"
)
@click.option('-t', '--ticker', type=str, help="Stock ticker")
@click.pass_context
def get_stock_data(ctx: click.Context, ticker: str):
    _get_stock_data(
        ticker=ticker,
        data_period=ctx.obj["data_period"],
        data_interval=ctx.obj["data_interval"],
        current_date=ctx.obj["current_date"],
        db=ctx.obj["db"],
    )


def _get_stock_data(current_date, data_interval: str, data_period: int, ticker: str, db: TmDB):
    start = utils.get_starting_date(db, ticker, data_period, current_date)

    # Download stock data and save into DB
    if start != current_date:  # prevent an unneeded API calls
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


cli.add_command(get_stocks_data)
cli.add_command(get_stock_data)

cli()
