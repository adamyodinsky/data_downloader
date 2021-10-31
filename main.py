import yfinance as yf
import argparse
import yaml


def init_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-tk", "--ticker", help="Ticker symbol name")

    return parser.parse_args()


def fetch_ticker(args):
    return yf.Ticker(args.ticker)


def main():
    args = init_parser()
    ticker = fetch_ticker(args)


def load_to_db():
    pass




