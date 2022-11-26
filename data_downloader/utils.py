import yaml
from munch import DefaultMunch
from dotenv import load_dotenv
from pathlib import Path


def load_env(path: str):
    dotenv_path = Path(path)
    load_dotenv(dotenv_path=dotenv_path)


def load_config(path: str):
    config_dict = yaml.safe_load(open(path))
    return DefaultMunch.fromDict(config_dict)
