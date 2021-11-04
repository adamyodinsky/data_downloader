from timescale import TmDB
import yahoo
import helper

if __name__ == "__main__":
    config = helper.load_config()
    db = TmDB(config=config)

    tickers = db.get_tickers_list(config.db.tickers_table)

    for ticker in tickers:
        tickers_data = yahoo.download_prices(ticker=ticker[0], interval=config.yahoo.interval,
                                             period=config.yahoo.period)

        print(f"Uploading {ticker[0]} data to timescale")
        db.upload_data(df=tickers_data, table_name=config.db.prices_table)
    print("All done!")
