import yfinance as yf
import argparse
import yaml
from munch import DefaultMunch
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


def args_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--symbol", help="Symbol name")
    parser.add_argument("-t", "--time_period", help="Time period")

    return parser.parse_args()


def load_config():
    config_dict = yaml.safe_load(open("config.yaml"))
    return DefaultMunch.fromDict(config_dict)


def fetch_ticker(symbol):
    return yf.Ticker(symbol)


def main():
    args = args_parser()
    config = load_config()
    ticker = fetch_ticker(config.symbol)
    symbol_df = ticker.history(period=config.time_period)

    print(symbol_df)

    client = InfluxDBClient(url=config.db.url, token=config.db.token)
    write_api = client.write_api(write_options=SYNCHRONOUS)

    write_api.write(org=config.db.org, bucket=config.db.bucket, record=symbol_df, data_frame_measurement_name=config.symbol)

main()
