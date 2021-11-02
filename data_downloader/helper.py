import yaml
import argparse
from munch import DefaultMunch


def args_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--symbol", help="Symbol name")
    parser.add_argument("-t", "--time_period", help="Time period")

    return parser.parse_args()


def load_config():
    config_dict = yaml.safe_load(open("../config.yaml"))
    return DefaultMunch.fromDict(config_dict)

