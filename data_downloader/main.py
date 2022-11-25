from timescale import TmDB
import yahoo
import helper
import datetime
from dateutil.relativedelta import relativedelta
import logging
import os


def _get_starting_date():
    '''Get the first date from where we want the data series we downloading will begin from.
    If there is no data at all, it will download the data by the data_period provided in the config.yaml file.
    If there is data, but there is a new data that should be downloaded, or the data_period is going further back from our oldest data_point, the missing data will be downloaded and added to the existing data.
    '''

    start = None
    first_data_point_date = db.get_first(table=config.db.stock_prices_table, ticker=ticker[0])
    last_data_point_date = db.get_last(table=config.db.stock_prices_table, ticker=ticker[0])
    period_date = current_date - relativedelta(years=config.data_period) + relativedelta(weeks=1)
    
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


if __name__ == "__main__":
    # Set logger configuration
    logging.basicConfig(
        format="%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
        datefmt="%Y-%m-%d:%H:%M:%S",
        level=logging.INFO,
    )

    # Load config.yaml and get today's date for future use
    config = helper.load_config(os.environ.get("CONFIG_PATH"))
    current_date = datetime.date.today()
    
    # Prepare stock tickers to iterate over and get their data
    db = TmDB(config)
    tickers = db.get_tickers_list(config.db.stock_tickers_table)
    
    # Download stocks data and save into DB
    for index, ticker in enumerate(tickers):
        # a limit for a number of stocks we want to get data on from the list, this should be use only in dev.
        if config.number_of_tickers and index >= config.number_of_tickers:
            break
        
        start = _get_starting_date()

        if start != current_date: # prevent an API call when there is no need
            tickers_data = yahoo.download_prices(
                ticker=ticker[0],
                start=start,
                end=current_date,
                interval=config.data_interval,
            )
            logging.info(f"Uploading {ticker[0]} data to DB.")
            db.upsert_data(df=tickers_data, table=config.db.stock_prices_table)
        else:
            logging.info(f"{ticker[0]} Is up to date, no action needed.")

    logging.info("Data updated successfully.")
