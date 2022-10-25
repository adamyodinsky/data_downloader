from timescale import TmDB
import yahoo
import helper
import datetime
import logging

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                        datefmt='%Y-%m-%d:%H:%M:%S',
                        level=logging.INFO)
    config = helper.load_config("../config.yaml")
    db = TmDB(config)

    tickers = db.get_tickers_list(config.db.tickers_table)

    for index, ticker in enumerate(tickers):
        if index >= config.tickers_scale:
            break

        start = db.get_last(table=config.db.prices_table, ticker=ticker[0])
        if start is not None:
            start = start[1]

        today = datetime.date.today()
        tickers_data = yahoo.download_prices(ticker=ticker[0], start=start, end=today)

        logging.info(f"Uploading {ticker[0]} data to timescale")

        db.upsert_data(df=tickers_data, table=config.db.prices_table)

    print("All done!")
