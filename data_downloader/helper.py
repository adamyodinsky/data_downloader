import yaml
from munch import DefaultMunch


def load_config(path: str):
    config_dict = yaml.safe_load(open(path))
    return DefaultMunch.fromDict(config_dict)
