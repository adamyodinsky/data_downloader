from dotenv import load_dotenv
from pathlib import Path
import os


def load_env(path: str):
    dotenv_path = Path(path)
    load_dotenv(dotenv_path=dotenv_path)


def check_env_vars():
    env_vars_list = [
        "DB_STOCK_TICKERS_TABLE",
        "DB_STOCK_PRICE_TABLE",
        "POSTGRES_DB",
        "POSTGRES_HOST",
        "POSTGRES_PORT",
        "POSTGRES_USER",
        "POSTGRES_PASSWORD"]

    for var in env_vars_list:
        if os.getenv(var) is None:
            raise RuntimeError(f"Environment variable {var} missing!")
