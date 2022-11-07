import timescale, helper
import pandas as pd
import click
import os

from db_vars import *

config = helper.load_config(os.environ.get("CONFIG_PATH"))
db = timescale.TmDB(config)


module_path = os.path.dirname(__file__)
raw_csv_file_name = f"{module_path}/files/sp500_stocks_05112021.csv"


def execute_db_command(message, command):
    db.cursor.execute(command)
    db.conn.commit()
    print(message)


@click.group()
def cli():
    pass


@click.command(
    help=f"Create and index {STOCK_PRICE_TABLE_NAME} and {STOCK_LIST_TABLE_NAME} tables"
)
def init():
    execute_db_command(create_stocks_list_table_message, create_stocks_list_table)
    execute_db_command(create_stock_price_table_message, create_stock_price_table)
    execute_db_command(index_stocks_list_table_message, index_stocks_list_table)
    execute_db_command(index_stocks_list_table_message, index_stock_price_table)
    execute_db_command(
        create_stock_price_hypertable_message, create_stock_price_hypertable
    )


@click.command(help=f"Populate {STOCK_LIST_TABLE_NAME} table from a local csv file")
def populate_tickers_table():
    df = pd.read_csv(raw_csv_file_name)
    df = df.rename(
        columns={
            "Symbol": "ticker",
            "Description": "name",
            "GICS Sector": "industry",
            "Market cap": "market_cap",
        }
    )

    db.upsert_data(df=df, table=STOCK_LIST_TABLE_NAME)
    print(f"Uploaded the data successfully to {STOCK_LIST_TABLE_NAME} table")


@click.command(help="Delete tables content")
def delete_tables_content():
    execute_db_command(delete_stock_price_content_message, delete_stock_price_content)
    execute_db_command(delete_stock_price_content_message, delete_stocks_list_content)


cli.add_command(init)
cli.add_command(populate_tickers_table)
cli.add_command(delete_tables_content)

cli()
