import data_downloader

if __name__ == "__main__":
    ctx = data_downloader.cli()
    data_downloader.get_stocks_data(ctx)
