import timescale
import yahoo
import helper


if __name__ == "__main__":
    config = helper.load_config()

    tickers = timescale.get_tickers_list(config=config, table_name=config.db.tickers_table)

    for ticker in tickers:
        tickers_data = yahoo.download_prices(ticker=ticker[0], interval=config.yahoo.interval,
                                             period=config.yahoo.period)
        print(f"Uploading {ticker[0]} data to timescale")
        timescale.upload_data(df=tickers_data, config=config, table_name=config.db.prices_table)
    print("All done!")
