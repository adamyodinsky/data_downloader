import timescale
import yahoo
import helper
# import pandas as pd


if __name__ == "__main__":
    config = helper.load_config()

    tickers = timescale.get_tickers_list(config)

    for ticker in tickers:
        tickers_data = yahoo.download_prices(ticker[0])
        print(f"Uploading {ticker[0]} data to timescale")
        timescale.upload_data(tickers_data, config)

    print("All done!")