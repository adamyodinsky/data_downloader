from dotenv import load_dotenv
from pathlib import Path


def load_env(path: str):
    dotenv_path = Path(path)
    load_dotenv(dotenv_path=dotenv_path)
