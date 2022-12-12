""" This file contain database administration commands to be used be dv_cmd.py functions """

import os
import config

path = os.path.dirname(__file__)
print(path)


# Create tickers list table
create_sp500_tickers_table_message = (
    f"Created {config.db_sp500_tickers_table} table successfully"
)
create_sp500_tickers_table_query = f"""
    CREATE TABLE IF NOT EXISTS {config.db_sp500_tickers_table} (
        ticker TEXT PRIMARY KEY,
        name TEXT,
        weight FLOAT
    );
    """

# Create stock prices table
create_stock_price_table_message = (
    f"Created {config.db_stock_price_table} table successfully"
)
create_stock_price_table_query = f"""
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

# Create tickers list table
create_gdp_table_message = (
    f"Created {config.gdp_table} table successfully"
)
create_gdp_table_query = f"""
    CREATE TABLE IF NOT EXISTS {config.gdp_table} (
        date DATE,
        value FLOAT
    );
    """

# index tables
index_sp500_tickers_table_message = (
    f"Indexed the table {config.db_sp500_tickers_table}."
)
index_sp500_tickers_table_query = (
    f"CREATE INDEX ON {config.db_sp500_tickers_table} (ticker, weight DESC);"
)

index_stock_price_table_message = f"Indexed the table {config.db_stock_price_table}."
index_stock_price_table_query = (
    f"CREATE INDEX ON {config.db_stock_price_table} (ticker, date DESC);"
)

index_gdp_table_message = (
    f"Indexed the table {config.gdp_table}."
)
index_gdp_table_query = (
    f"CREATE INDEX ON {config.gdp_table} (date DESC);"
)

# convert table to a time series table (postgres timescaledb feature)
create_stock_price_hypertable_message = (
    f"Converted {config.db_stock_price_table} to a Hyper Table."
)
create_stock_price_hypertable_query = f"SELECT create_hypertable('{config.db_stock_price_table}', 'date', if_not_exists => TRUE);"

# Delete table content

delete_stock_price_content_message = (
    f"Deleted the content from {config.db_stock_price_table} table."
)
delete_stock_price_content_query = f"DELETE FROM {config.db_stock_price_table}"

delete_sp500_tickers_content_query = f"DELETE FROM {config.db_sp500_tickers_table}"
delete_sp500_tickers_content_message = (
    f"Deleted the content from {config.db_sp500_tickers_table} table."
)
delete_gdp_content_query = f"DELETE FROM {config.gdp_table}"
delete_gdp_content_message = (
    f"Deleted the content from {config.gdp_table} table."
)


# TODO create_server_query is not working yet

postgres_fdw_extension_query = "CREATE EXTENSION IF NOT EXISTS postgres_fdw";

create_server_query = f"""
CREATE SERVER IF NOT EXISTS {config.postgres_dbname}
    FOREIGN DATA WRAPPER postgres_fdw
    OPTIONS (host '{config.postgres_username}:{config.postgres_password}@{config.postgres_host}', dbname '{config.postgres_dbname}', port '{config.postgres_port}');
"""
create_server_message = "Created server successfully."
