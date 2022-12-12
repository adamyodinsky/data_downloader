import utils
import os

utils.load_env(os.environ.get("ENV_FILE_PATH"))

# Logs
log_level = os.environ.get("LOG_LEVEL") or "INFO"

# Downloader settings
fred_token = os.environ.get("FRED_TOKEN")
data_period = (
    int(os.environ.get("DATA_PERIOD")) if os.environ.get("DATA_PERIOD") else None
)
data_interval = os.environ.get("DATA_INTERVAL")

# Tickers
tickers = os.environ.get("TICKERS")
number_of_tickers = (
    int(os.environ.get("NUMBER_OF_TICKERS"))
    if os.environ.get("NUMBER_OF_TICKERS")
    else 5
)

# DB Table names
db_stock_price_table = os.environ.get("DB_STOCK_PRICE_TABLE") or "stock_price"
db_sp500_tickers_table = os.environ.get("DB_STOCK_TICKERS_TABLE") or "sp500_tickers"
macro_table = os.environ.get("MACRO_TABLE_NAME") or "macros"

# Postgres configuration
postgres_dbname = os.environ.get("POSTGRES_DB") or "stocks_data"
postgres_host = os.environ.get("POSTGRES_HOST") or "localhost"
postgres_port = os.environ.get("POSTGRES_PORT") or "5432"
postgres_username = os.environ.get("POSTGRES_USER") or "admin"
postgres_password = os.environ.get("POSTGRES_PASSWORD") or "1234"
