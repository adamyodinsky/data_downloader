from timescale import TmDB
import pandas as pd
import click
import config
import requests
from bs4 import BeautifulSoup as bs

import db_vars


def execute_db_command(message: str, command: str, db: TmDB):
    db.cursor.execute(command)
    db.conn.commit()
    print(message)


@click.group()
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)
    ctx.obj["db"] = TmDB()


@click.command(
    help=f"Create and index {config.db_stock_price_table} and {config.db_sp500_tickers_table} tables"
)
@click.pass_context
def init(ctx):
    execute_db_command(
        "Postgres_fdw extension query completed successfully",
        db_vars.postgres_fdw_extension_query,
        ctx.obj["db"],
    )
    execute_db_command(
        db_vars.create_server_message,
        db_vars.create_server_query,
        ctx.obj["db"],
    )
    execute_db_command(
        "User granted permission successfully",
        f"GRANT USAGE ON FOREIGN SERVER {config.postgres_dbname} TO {config.postgres_username};",
        ctx.obj["db"],
    )
    execute_db_command(
        db_vars.create_sp500_tickers_table_message,
        db_vars.create_sp500_tickers_table_query,
        ctx.obj["db"],
    )
    execute_db_command(
        db_vars.create_stock_price_table_message,
        db_vars.create_stock_price_table_query,
        ctx.obj["db"],
    )
    execute_db_command(
        db_vars.index_sp500_tickers_table_message,
        db_vars.index_sp500_tickers_table_query,
        ctx.obj["db"],
    )
    execute_db_command(
        db_vars.index_stock_price_table_message,
        db_vars.index_stock_price_table_query,
        ctx.obj["db"],
    )
    execute_db_command(
        db_vars.create_stock_price_hypertable_message,
        db_vars.create_stock_price_hypertable_query,
        ctx.obj["db"],
    )
    _update_sp500_tickers_table(ctx.obj["db"])



@click.command(help="Delete tables content")
@click.pass_context
def delete_tables_content(ctx):
    execute_db_command(
        db_vars.delete_stock_price_content_message,
        db_vars.delete_stock_price_content_query,
        ctx.obj["db"],
    )
    execute_db_command(
        db_vars.delete_sp500_tickers_content_message,
        db_vars.delete_sp500_tickers_content_query,
        ctx.obj["db"],
    )


def _update_sp500_tickers_table(db: TmDB):
    url = "https://www.slickcharts.com/sp500"
    request = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = bs(request.text, "lxml")
    stats = soup.find("table", class_="table table-hover table-borderless table-sm")
    df = pd.read_html(str(stats))[0]
    df["% Chg"] = df["% Chg"].str.strip("()-%")
    df["% Chg"] = pd.to_numeric(df["% Chg"])
    df["Chg"] = pd.to_numeric(df["Chg"])
    df = df[["Symbol", "Company", "Weight"]]
    df = df.rename(
        columns={
            "Symbol": "ticker",
            "Company": "name",
            "Weight": "weight",
        }
    )
    # Clean table old data
    execute_db_command(
        db_vars.delete_sp500_tickers_content_message,
        db_vars.delete_sp500_tickers_content_query,
        db,
    )
    # Update with new data
    db.upsert_data(df=df, table=config.db_sp500_tickers_table)
    print(f"Uploaded the data successfully to {config.db_sp500_tickers_table} table")


@click.command(
    help=f"Update {config.db_sp500_tickers_table} table from a local csv file"
)
@click.pass_context
def update_sp500_tickers_table(ctx):
    _update_sp500_tickers_table(ctx.obj["db"])
    


# TODO cli.add_command(create_server) # not working
cli.add_command(init)
cli.add_command(delete_tables_content)
cli.add_command(update_sp500_tickers_table)

cli()
