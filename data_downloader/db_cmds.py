import timescale, helper
import pandas as pd
import argparse

from db_vars import *

config = helper.load_config("../config.yaml")
db = timescale.TmDB(config)

raw_csv_file_name = "../files/sp500_stocks_05112021.csv"
# COMMANDS_LIST = """
# - create_table
# - index_ticker_table
# - populate_ticker_table
# """


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--func', type=str)
    return parser.parse_args()


def execute_db_command(message, command):
    db.cursor.execute(command)
    db.conn.commit()
    print(message)


def populate_tickers_table():
    df = pd.read_csv(raw_csv_file_name)
    df = df.rename(columns={
        "Symbol": "ticker",
        "Description": "name",
        "GICS Sector": "industry",
        "Market cap": "market_cap",
    })

    db.upsert_data(df=df, table=STOCK_LIST_TABLE_NAME)
    print(f"Uploaded the data successfully to {STOCK_LIST_TABLE_NAME} table")


def init():
    execute_db_command(create_stocks_list_table_message, create_stocks_list_table)
    execute_db_command(create_stock_price_table_message, create_stock_price_table)
    execute_db_command(index_stocks_list_table_message, index_stocks_list_table)
    execute_db_command(index_stocks_list_table_message, index_stock_price_table)
    execute_db_command(create_stock_price_hypertable_message, create_stock_price_hypertable)

    populate_tickers_table()


def run():
    init()
#     args = get_args()

#     if args.func == 'create_tickers_table':
#         create_table()
#     elif args.func == 'index_ticker_table':
#         index_ticker_table()
#     elif args.func == 'populate_ticker_table':
#         populate_ticker_table()
#     else:
#         print(f"{args.func} is not a valid command. valid commands are:\n{commands_list}")

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
