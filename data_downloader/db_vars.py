import helper
config = helper.load_config("../config.yaml")

STOCK_PRICE_TABLE_NAME = config.db.stock_prices_table
STOCK_LIST_TABLE_NAME = config.db.stock_tickers_table


config = helper.load_config("../config.yaml")

create_stocks_list_table_message = f"Created {STOCK_LIST_TABLE_NAME} table successfully"
create_stocks_list_table = f"""
    CREATE TABLE IF NOT EXISTS {STOCK_LIST_TABLE_NAME} (
        ticker TEXT PRIMARY KEY,
        name TEXT,
        industry TEXT,
        market_cap MONEY
    );
    """

create_stock_price_table_message = f"Created {STOCK_PRICE_TABLE_NAME} table successfully"
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


index_stocks_list_table_message = f"Indexed the table {STOCK_LIST_TABLE_NAME}."
index_stocks_list_table = f"CREATE INDEX ON {STOCK_LIST_TABLE_NAME} (ticker, market_cap DESC);"

index_stocks_list_table_message = f"Indexed the table {STOCK_PRICE_TABLE_NAME}."
index_stock_price_table = f"CREATE INDEX ON {STOCK_PRICE_TABLE_NAME} (ticker, date DESC);"

create_stock_price_hypertable_message = f"Converted {STOCK_PRICE_TABLE_NAME} to a Hyper Table."
create_stock_price_hypertable = f"SELECT create_hypertable({STOCK_PRICE_TABLE_NAME}, 'date');"
