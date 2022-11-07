from timescale import TmDB
import yahoo
import helper
import datetime
from dateutil.relativedelta import relativedelta
import logging
import os

def get_starting_date():
    start = None
    first_data_point_date = db.get_first(table=config.db.stock_prices_table, ticker=ticker[0])
    last_data_point_date = db.get_last(table=config.db.stock_prices_table, ticker=ticker[0])
    period_date = current_date - relativedelta(years=config.data_period) + relativedelta(weeks=1)
    
    # if period go further in the past compared to the oldest record, use period
    # else, use the last data-point date as a starting point which is the most fresh.
    if last_data_point_date is not None:
        if period_date < first_data_point_date[1]:
            start = period_date
        else:
            start = last_data_point_date[1]
    else:
        start = period_date

    return start

if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
        datefmt="%Y-%m-%d:%H:%M:%S",
        level=logging.INFO,
    )
    config = helper.load_config(os.environ.get("CONFIG_PATH"))
    db = TmDB(config)

    current_date = datetime.date.today()
    tickers = db.get_tickers_list(config.db.stock_tickers_table)

    for index, ticker in enumerate(tickers):
        if index >= config.number_of_tickers:
            break

        start = get_starting_date()

        if start != current_date:
            tickers_data = yahoo.download_prices(
                ticker=ticker[0],
                start=start,
                end=current_date,
                interval=config.data_interval,
            )
            logging.info(f"Uploading {ticker[0]} data to DB")
            db.upsert_data(df=tickers_data, table=config.db.stock_prices_table)

    print("All done!")
