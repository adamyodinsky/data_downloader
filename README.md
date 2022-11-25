# Data Downloader

- [Data Downloader](#data-downloader)
  - [1.1. Glossary](#11-glossary)
  - [1.2. Dependencies](#12-dependencies)
  - [1.3. Local Development](#13-local-development)
  - [1.4. Project design](#14-project-design)
    - [1.4.1. db\_cli.py \& db\_vars.py](#141-db_clipy--db_varspy)
  - [1.5. What's next?](#15-whats-next)

The purpose of This project is to populate an SQL database with data about stocks.
Currently, the project only supports historical price data.
The project uses [the Yahoo API python package](https://pypi.org/project/yfinance/) to fetch the data and [timescaleDB](https://www.timescale.com/) as a time-series database.

## 1.1. Glossary

- `Stocks list table` An SQL table that contains all the stocks` tickers/names that we want to get their historical price data into the "stock price" tables.
- `Stock Price table` This is a table that contains all the historical stock price data, this table is indexed as a hyper-table, which means it is optimized for time series data. Table columns are date, ticker, open, high, low, close, close_adj, and volume. the table's index and primary key are (ticker, date).

## 1.2. Dependencies

Get to know and install the next tools:

- [pyenv](https://github.com/pyenv/pyenv#installation)
- [poetry](https://python-poetry.org/docs/#installation) (use the link to install, do not use brew)
- [docker](https://docs.docker.com/get-docker/)
- [docker-compose](https://docs.docker.com/compose/install/)


## 1.3. Local Development

To start developing locally you will need to:

1. Install the [dependencies](#12-dependencies).
2. Start your timescaleDB engines ON.
   1. `make db-up` Spin up a timescaleDB via docker-compose. you can see the running containers with "docker ps" command.
   2. Open the browser at http://localhost:9000 for the PGAdmin UI.
   3. Connect with `my@email.com` and `password`
   4. Click `Add new server`.
      1. On the first page name=`postgres`.
      2. On `connection` page host=`timescale` username=`postgres` pass=`1234`.
   5. Click `Save`.
   6. `make db-init` Create tables and indices.
   7. `make db-populate` Populate the [stocks list table](#11-glossary).
3. `poetry install` to install python libraries in the poetry virtual environment.
4. `make start` Run the data downloader python code  (via poetry) and start downloading stocks data!


## 1.4. Project design

### 1.4.1. db_cli.py & db_vars.py
`db_vars.py` Contains commands for creating tables, creating indices, and populating the "tickers" table. used by `db_cli.py`.
`db_cli.py` Is a command line tool for DB administration.
`helpers.py` contains helpers functions, which can be also called "utils", right now containing only a "load_config" function.
`timescale.py` A file that contains a class that encapsulates all the functionality for interacting with our timescaleDB.
`yahoo.py` A file with all the functions needed for interacting with yahoo API for getting data about stocks.

## 1.5. What's next?

- Handle data about the finances and fundamentals of the companies.
