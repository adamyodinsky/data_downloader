""" This file contain database administration commands to be used be dv_cmd.py functions """

import os
import config

path = os.path.dirname(__file__)
print(path)

# TODO: need to refactor this whole file pronto, it's horrible

# Create tickers list table

create_sp500_tickers_table_message = (
    f"Created {config.db_sp500_tickers_table} table successfully"
)
create_sp500_tickers_table_query = f"""
    CREATE TABLE IF NOT EXISTS {config.db_sp500_tickers_table} (
        ticker TEXT,
        name TEXT,
        weight FLOAT,
        PRIMARY KEY (ticker)
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
create_macro_table_message = f"Created {config.macro_table} table successfully"
create_macro_table_query = f"""
    CREATE TABLE IF NOT EXISTS {config.macro_table} (
        date DATE,
        value FLOAT,
        m_type TEXT,
        PRIMARY KEY (date, m_type)
    );
    """


# Index sp500 table
index_sp500_tickers_table_message = (
    f"Indexed the table {config.db_sp500_tickers_table}."
)
index_sp500_tickers_table_query = (
    f"CREATE INDEX ON {config.db_sp500_tickers_table} (ticker, weight DESC);"
)

# Index stock price table
index_stock_price_table_message = f"Indexed the table {config.db_stock_price_table}."
index_stock_price_table_query = (
    f"CREATE INDEX ON {config.db_stock_price_table} (ticker, date DESC);"
)

# Index macro table
index_macro_table_message = f"Indexed the table {config.macro_table}."
index_macro_table_query = f"CREATE INDEX ON {config.macro_table} (m_type, date DESC);"


# Convert stock tables to a time series table (postgres timescaledb feature)
# stock price table
# create_stock_price_hypertable_message = (
#     f"Converted {config.db_stock_price_table} to a Hyper Table."
# )
# create_stock_price_hypertable_query = f"SELECT create_hypertable('{config.db_stock_price_table}', 'date', if_not_exists => TRUE);"

# macro table
# create_macro_hypertable_message = f"Converted {config.macro_table} to a Hyper Table."
# create_macro_hypertable_query = f"SELECT create_hypertable('{config.macro_table}', 'type, date', if_not_exists => TRUE);"

# Delete tables content
delete_stock_price_content_message = (
    f"Deleted the content from {config.db_stock_price_table} table."
)
delete_stock_price_content_query = f"DELETE FROM {config.db_stock_price_table}"

delete_sp500_tickers_content_query = f"DELETE FROM {config.db_sp500_tickers_table}"
delete_sp500_tickers_content_message = (
    f"Deleted the content from {config.db_sp500_tickers_table} table."
)
delete_macro_content_query = f"DELETE FROM {config.macro_table}"
delete_macro_content_message = f"Deleted the content from {config.macro_table} table."


# TODO create_server_query is not working yet
postgres_fdw_extension_query = "CREATE EXTENSION IF NOT EXISTS postgres_fdw"
postgres_fdw_extension_message = "Created postgres_fdw extension successfully."

create_server_query = f"""
CREATE SERVER IF NOT EXISTS {config.postgres_dbname}
    FOREIGN DATA WRAPPER postgres_fdw
    OPTIONS (host '{config.postgres_username}:{config.postgres_password}@{config.postgres_host}', dbname '{config.postgres_dbname}', port '{config.postgres_port}');
"""
create_server_message = "Created server successfully."


# a dictionary of all the queries and messages ordered by the order they should be executed
queries = {
    "create": {
        "create_sp500_tickers_table": {
            "query": create_sp500_tickers_table_query,
            "message": create_sp500_tickers_table_message,
        },
        "create_stock_price_table": {
            "query": create_stock_price_table_query,
            "message": create_stock_price_table_message,
        },
        "create_macro_table": {
            "query": create_macro_table_query,
            "message": create_macro_table_message,
        },
    },
    "index": {
        "index_sp500_tickers_table": {
            "query": index_sp500_tickers_table_query,
            "message": index_sp500_tickers_table_message,
        },
        "index_stock_price_table": {
            "query": index_stock_price_table_query,
            "message": index_stock_price_table_message,
        },
        "index_macro_table": {
            "query": index_macro_table_query,
            "message": index_macro_table_message,
        },
        # "create_stock_price_hypertable": {
        #     "query": create_stock_price_hypertable_query,
        #     "message": create_stock_price_hypertable_message,
        # },
        # "create_macro_hypertable": {
        #     "query": create_macro_hypertable_query,
        #     "message": create_macro_hypertable_message,
        # },
    },
    "delete": {
        "delete_stock_price_content": {
            "query": delete_stock_price_content_query,
            "message": delete_stock_price_content_message,
        },
        "delete_sp500_tickers_content": {
            "query": delete_sp500_tickers_content_query,
            "message": delete_sp500_tickers_content_message,
        },
        "delete_gdp_content": {
            "query": delete_macro_content_query,
            "message": delete_macro_content_message,
        },
    },
    "others": {
        "postgres_fdw_extension": {
            "query": postgres_fdw_extension_query,
            "message": "postgres_fdw extension created successfully.",
        },
        "create_server": {
            "query": create_server_query,
            "message": create_server_message,
        },
    },
}
