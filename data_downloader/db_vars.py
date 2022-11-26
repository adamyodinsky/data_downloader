# This file contain database administration commands to be used be dv_cmd.py functions
import os
import helper

path = os.path.dirname(__file__)
print(path)


config = helper.load_config(os.environ.get("CONFIG_PATH"))

STOCK_PRICE_TABLE_NAME = os.environ.get("DB_STOCK_PRICE_TABLE")
STOCK_LIST_TABLE_NAME = os.environ.get("DB_STOCK_TICKERS_TABLE")

# Create tickers list table
create_stocks_list_table_message = f"Created {STOCK_LIST_TABLE_NAME} table successfully"
create_stocks_list_table = f"""
    CREATE TABLE IF NOT EXISTS {STOCK_LIST_TABLE_NAME} (
        ticker TEXT PRIMARY KEY,
        name TEXT,
        industry TEXT,
        market_cap MONEY
    );
    """

# Create stock prices table
create_stock_price_table_message = (
    f"Created {STOCK_PRICE_TABLE_NAME} table successfully"
)
create_stock_price_table = f"""
    CREATE TABLE IF NOT EXISTS {STOCK_PRICE_TABLE_NAME} (
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
index_stocks_list_table_message = f"Indexed the table {STOCK_LIST_TABLE_NAME}."
index_stocks_list_table = (
    f"CREATE INDEX ON {STOCK_LIST_TABLE_NAME} (ticker, market_cap DESC);"
)

index_stocks_list_table_message = f"Indexed the table {STOCK_PRICE_TABLE_NAME}."
index_stock_price_table = (
    f"CREATE INDEX ON {STOCK_PRICE_TABLE_NAME} (ticker, date DESC);"
)

# convert table to a time series table (postgres timescaledb feature)
create_stock_price_hypertable_message = (
    f"Converted {STOCK_PRICE_TABLE_NAME} to a Hyper Table."
)
create_stock_price_hypertable = f"SELECT create_hypertable('{STOCK_PRICE_TABLE_NAME}', 'date', if_not_exists => TRUE);"

# Delete table content

delete_stock_price_content_message = (
    f"Deleted the content from {STOCK_LIST_TABLE_NAME} table."
)
delete_stock_price_content = f"DELETE FROM {STOCK_PRICE_TABLE_NAME}"

delete_stock_price_content_message = (
    f"Deleted the content from {STOCK_LIST_TABLE_NAME} table."
)
delete_stocks_list_content = f"DELETE FROM {STOCK_LIST_TABLE_NAME}"

# TODO this is not working
# create_server_command = """
# CREATE SERVER IF NOT EXISTS postgres2 FOREIGN
# DATA WRAPPER postgres_fdw
# OPTIONS (host 'timescale', dbname 'postgres', port '5432');
# """
# create_server_message = "Created server successfully."
