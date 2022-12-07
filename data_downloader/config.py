import os

# Logs
log_level = os.environ.get("LOG_LEVEL") or "INFO"

# Files path
env_file_path = os.environ.get("ENV_FILE_PATH")
tickers_csv_file = os.environ.get("TICKERS_CSV__FILE")

# Downloader settings
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

# Table names
db_stock_price_table = os.environ.get("DB_STOCK_PRICE_TABLE")
db_stock_tickers_table = os.environ.get("DB_STOCK_TICKERS_TABLE")

# Postgres configuration
postgres_host = os.environ.get("POSTGRES_HOST")
postgres_port = os.environ.get("POSTGRES_PORT")
postgres_db = os.environ.get("POSTGRES_DB")
postgres_user = os.environ.get("POSTGRES_USER")
postgres_password = os.environ.get("POSTGRES_PASSWORD")
