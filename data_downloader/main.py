from timescale import TmDB
import yahoo
import helper
import datetime
import logging


def populate_stocks_prices():

    config = helper.load_config("../config.yaml")
    db = TmDB(config)

    tickers = db.get_tickers_list(config.db.stocks_tickers_table)

    for index, ticker in enumerate(tickers):
        if index >= config.tickers_scale:
            break

        start = db.get_last(table=config.db.stocks_prices_table, ticker=ticker[0])
        if start is not None:
            start = start[1]

        today = datetime.date.today()

        tickers_data = yahoo.download_prices(ticker=ticker[0], start=start, end=today)

        logging.info(f"Uploading {ticker[0]} data to timescale")

        db.upsert_data(df=tickers_data, table=config.db.stocks_prices_table)


def populate_macro_values():
    config = helper.load_config("../config.yaml")
    db = TmDB(config)
    tickers_data = None

    tickers = db.get_tickers_list(config.db.macro_tickers_table)

    for index, ticker in enumerate(tickers):
        if index >= config.tickers_scale:
            break

        start = db.get_last(table=config.db.macro_values_table, ticker=ticker[0])
        if start is not None:
            start = start[1]

        today = datetime.date.today()

        api_source = (db.get_api_source(table=config.db.macro_tickers_table, ticker=ticker[0]))[0]

        if api_source == "yahoo":
            tickers_data = yahoo.download_prices(ticker=ticker[0], start=start, end=today)
        else:
            logging.info("API source is not yahoo.")

        db.upsert_data(df=tickers_data, table=config.db.stocks_prices_table)
        logging.info(f"Uploading {ticker[0]} data to timescale")


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                        datefmt='%Y-%m-%d:%H:%M:%S',
                        level=logging.INFO)

    populate_macro_values()

    print("All done!")
