from dotenv import load_dotenv
from pathlib import Path
from timescale import TmDB
from dateutil.relativedelta import relativedelta
import os


def load_env(path: str):
    dotenv_path = Path(path)
    load_dotenv(dotenv_path=dotenv_path)


def get_starting_date(db: TmDB, ticker: str, data_period: str, current_date):
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

