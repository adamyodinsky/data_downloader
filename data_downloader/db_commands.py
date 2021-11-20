import timescale, helper
import pandas as pd
import argparse

config = helper.load_config("../config.yaml")
db = timescale.TmDB(config)

stock_tickers_table = "stock_tickers"
macro_tickers_table = "macro_tickers"
stock_tickers_prices_table = "stock_prices"
macro_tickers_values_table = "macro_values"

stocks_raw_csv_file_name = "../files/sp500_stocks_05112021.csv"
macro_raw_csv_file_name = "../files/macro.csv"

commands_list = """
create_stock_tickers_table
create_macro_tickers_table
create_macro_tickers_values_table
create_stock_tickers_values_table
populate_ticker_table
populate_macro_tickers_table
run_all
"""


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--func', type=str)
    return parser.parse_args()


def create_stock_tickers_table():
    command = f"""
    CREATE TABLE IF NOT EXISTS {stock_tickers_table} (
        ticker TEXT PRIMARY KEY,
        name TEXT,
        industry TEXT,
        market_cap MONEY
    );
    """

    db.cursor.execute(command)
    db.conn.commit()
    print("Created Tickers table successfully")

    command = f"CREATE INDEX ON {stock_tickers_table} (ticker, market_cap DESC);"
    db.cursor.execute(command)
    db.conn.commit()
    print("Indexed successfully")


def create_macro_tickers_table():
    command = f"""
    CREATE TABLE IF NOT EXISTS {macro_tickers_table} (
        ticker TEXT PRIMARY KEY,
        name TEXT,
        api_source TEXT
    );
    """

    db.cursor.execute(command)
    db.conn.commit()
    print("Created Macro Tickers table successfully")


def create_tickers_values_table(table_name):
    command = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
          date DATE NOT NULL,
          ticker TEXT,
          open NUMERIC,
          high NUMERIC,
          low NUMERIC,
          close NUMERIC,
          close_adj NUMERIC,
          volume NUMERIC,
          PRIMARY KEY (ticker, date)
    );
    """
    db.cursor.execute(command)
    db.conn.commit()
    print("Created Macro Tickers Values table successfully")

    command = f"CREATE INDEX ON {table_name} (ticker, date DESC);"
    db.cursor.execute(command)
    db.conn.commit()
    print("Indexed successfully")


def populate_stock_tickers_table():
    df = pd.read_csv(stocks_raw_csv_file_name)
    df = df.rename(columns={
        "Symbol": "ticker",
        "Description": "name",
        "GICS Sector": "industry",
        "Market cap": "market_cap",
    })

    db.upsert_data(df=df, table=stock_tickers_table)
    print("Uploaded the data successfully")


def populate_macro_tickers_table():
    df = pd.read_csv(macro_raw_csv_file_name)
    df = df.rename(columns={
        "Symbol": "ticker",
        "Description": "name",
        "API": "api_source"
    })

    db.upsert_data(df=df, table=macro_tickers_table)
    print("Uploaded the data successfully")


def run():
    args = get_args()

    if args.func == 'create_stock_tickers_table':
        create_stock_tickers_table()
    elif args.func == 'create_macro_tickers_table':
        create_macro_tickers_table()
    elif args.func == 'create_macro_tickers_values_table':
        create_tickers_values_table(macro_tickers_values_table)
    elif args.func == 'create_stock_tickers_values_table':
        create_tickers_values_table(stock_tickers_prices_table)
    elif args.func == 'populate_ticker_table':
        populate_stock_tickers_table()
    elif args.func == 'populate_macro_tickers_table':
        populate_macro_tickers_table()
    elif args.func == 'run_all':
        create_stock_tickers_table()
        create_macro_tickers_table()
        create_tickers_values_table(macro_tickers_values_table)
        create_tickers_values_table(stock_tickers_prices_table)
        populate_stock_tickers_table()
        populate_macro_tickers_table()
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
