""" This file contain database administration commands to be used be dv_cmd.py functions """

import os
import config

path = os.path.dirname(__file__)
print(path)


# Create tickers list table
create_stocks_list_table_message = (
    f"Created {config.db_stock_tickers_table} table successfully"
)
create_stocks_list_table = f"""
    CREATE TABLE IF NOT EXISTS {config.db_stock_tickers_table} (
        ticker TEXT PRIMARY KEY,
        name TEXT,
        industry TEXT,
        market_cap MONEY
    );
    """

# Create stock prices table
create_stock_price_table_message = (
    f"Created {config.db_stock_price_table} table successfully"
)
create_stock_price_table = f"""
    CREATE TABLE IF NOT EXISTS {config.db_stock_price_table} (
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

# index tables
index_stocks_list_table_message = f"Indexed the table {config.db_stock_tickers_table}."
index_stocks_list_table = (
    f"CREATE INDEX ON {config.db_stock_tickers_table} (ticker, market_cap DESC);"
)

index_stocks_list_table_message = f"Indexed the table {config.db_stock_price_table}."
index_stock_price_table = (
    f"CREATE INDEX ON {config.db_stock_price_table} (ticker, date DESC);"
)

# convert table to a time series table (postgres timescaledb feature)
create_stock_price_hypertable_message = (
    f"Converted {config.db_stock_price_table} to a Hyper Table."
)
create_stock_price_hypertable = f"SELECT create_hypertable('{config.db_stock_price_table}', 'date', if_not_exists => TRUE);"

# Delete table content

delete_stock_price_content_message = (
    f"Deleted the content from {config.db_stock_tickers_table} table."
)
delete_stock_price_content = f"DELETE FROM {config.db_stock_price_table}"

delete_stock_price_content_message = (
    f"Deleted the content from {config.db_stock_tickers_table} table."
)
delete_stocks_list_content = f"DELETE FROM {config.db_stock_tickers_table}"

# TODO this is not working
# create_server_command = """
# CREATE SERVER IF NOT EXISTS postgres2 FOREIGN
# DATA WRAPPER postgres_fdw
# OPTIONS (host 'timescale', dbname 'postgres', port '5432');
# """
# create_server_message = "Created server successfully."
