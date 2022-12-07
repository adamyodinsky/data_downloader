from timescale import TmDB
import pandas as pd
import click
import utils
import config

from db_vars import *


def execute_db_command(message: str, command: str, db: TmDB):
    db.cursor.execute(command)
    db.conn.commit()
    print(message)


@click.group()
@click.pass_context()
def cli(ctx):
    ctx.ensure_object(dict)
    utils.load_env(config.env_file_path)

    ctx.obj["db"] = TmDB()
    ctx.obj["raw_csv_file_name"] = config.tickers_csv_file


@click.command(
    help=f"Create and index {config.db_stock_price_table} and {config.db_stock_tickers_table} tables"
)
@click.pass_context
def init_tables(ctx):
    execute_db_command(
        create_stocks_list_table_message, create_stocks_list_table, ctx.obj["db"]
    )
    execute_db_command(
        create_stock_price_table_message, create_stock_price_table, ctx.obj["db"]
    )
    execute_db_command(
        index_stocks_list_table_message, index_stocks_list_table, ctx.obj["db"]
    )
    execute_db_command(
        index_stocks_list_table_message, index_stock_price_table, ctx.obj["db"]
    )
    execute_db_command(
        create_stock_price_hypertable_message,
        create_stock_price_hypertable,
        ctx.obj["db"],
    )


@click.command(
    help=f"Populate {config.db_stock_tickers_table} table from a local csv file"
)
@click.pass_context
def populate_tickers_table(ctx):
    df = pd.read_csv(ctx.obj["raw_csv_file_name"])
    df = df.rename(
        columns={
            "Symbol": "ticker",
            "Description": "name",
            "GICS Sector": "industry",
            "Market cap": "market_cap",
        }
    )

    ctx.obj["db"].upsert_data(df=df, table=config.db_stock_tickers_table)
    print(f"Uploaded the data successfully to {config.db_stock_tickers_table} table")


@click.command(help="Delete tables content")
@click.pass_context
def delete_tables_content():
    execute_db_command(delete_stock_price_content_message, delete_stock_price_content)
    execute_db_command(delete_stock_price_content_message, delete_stocks_list_content)


# TODO cli.add_command(create_server) # not working
cli.add_command(init_tables)
cli.add_command(populate_tickers_table)
cli.add_command(delete_tables_content)

cli()
