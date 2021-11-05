import timescale, helper
import pandas as pd
import argparse

config = helper.load_config("../config.yaml")
db = timescale.TmDB(config)

ticker_table_name = "stock_tickers"
raw_csv_file_name = "../sp500_stocks_05112021.csv"
commands_list = """
- create_tickers_table
- index_ticker_table
- populate_ticker_table
"""


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--func', type=str)
    return parser.parse_args()


def create_tickers_table():
    command = """
    CREATE TABLE IF NOT EXISTS stock_tickers (
        ticker TEXT PRIMARY KEY,
        name TEXT,
        industry TEXT,
        market_cap MONEY
    );
    """

    db.cursor.execute(command)
    db.conn.commit()
    print("Created Tickers table successfully")


def index_ticker_table():
    command = f"CREATE INDEX ON {ticker_table_name} (ticker, market_cap DESC);"
    db.cursor.execute(command)
    db.conn.commit()
    print("Indexed successfully")


def populate_ticker_table():
    df = pd.read_csv(raw_csv_file_name)
    df = df.rename(columns={
        "Symbol": "ticker",
        "Description": "name",
        "GICS Sector": "industry",
        "Market cap": "market_cap",
    })

    db.upsert_data(df=df, table="stock_tickers")
    print("Uploaded the data successfully")


def run():
    args = get_args()

    if args.func == 'create_tickers_table':
        create_tickers_table()
    elif args.func == 'index_ticker_table':
        index_ticker_table()
    elif args.func == 'populate_ticker_table':
        populate_ticker_table()
    else:
        print(f"{args.func} is not a valid command. valid commands are:\n{commands_list}")

    # match args.func:
    #     case 'create_tickers_table':
    #         create_tickers_table()
    #     case 'index_ticker_table':
    #         index_ticker_table()
    #     case 'populate_ticker_table':
    #         populate_ticker_table()
    #     case _:
    #         print(f"{args.func} is not a valid command. valid commands are: {commands_list}")


run()
