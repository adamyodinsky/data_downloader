# 1. Data Downloader

- [1. Data Downloader](#1-data-downloader)
  - [1.1. Glossary](#11-glossary)
  - [1.2. Dependencies](#12-dependencies)
  - [1.3. Local Development](#13-local-development)
  - [1.4. Project Structure](#14-project-structure)
    - [1.4.1. base folder](#141-base-folder)
    - [1.4.2. data\_downloader](#142-data_downloader)
    - [1.4.3. docker\_compose](#143-docker_compose)
    - [1.4.4. scripts](#144-scripts)
  - [1.5. Configuration](#15-configuration)
  - [1.6. Makefile](#16-makefile)
  - [1.7. What's next?](#17-whats-next)

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


## 1.4. Project Structure

### 1.4.1. base folder

- `config.yaml` A configuration file for the data_downloader, [see more about this file](#configuration).
- `Dockerfile` A docker file to build a data_downloader image.
- `Makefile` A make-file that contains shortcuts for useful commands within the context of the project. [read more about this file].


### 1.4.2. data_downloader

[data_downloader](./data_downloader/) The python source code folder that populates an SQL database with data about stocks.

- [`db_vars.py`](./data_downloader/db_vars.py) Contains commands for creating tables, creating indices, and populating the "tickers" table. used by `db_cli.py`.
- [`db_cli.py`](./data_downloader/db_cli.py) Is a command line tool for DB administration.
- [`helpers.py`](./data_downloader/helper.py) contains helpers functions, which can be also called "utils", right now containing only a "load_config" function.
- [`timescale.py`](./data_downloader/timescale.py) A file that contains a class that encapsulates all the functionality for interacting with our timescaleDB.
- [`yahoo.py`](./data_downloader/yahoo.py) A file with all the functions needed for interacting with yahoo API for getting data about stocks.
- [`main.py`](./data_downloader/main.py) The entry-point of the data_downloader, which downloads stocks' data.

Under [`data_downloader/files`](./data_downloader//files/) you can find CSV files that contain the data needed for the initial population of the ["stocks list table"](#11-glossary)

### 1.4.3. docker_compose

The [docker_compose](./docker_compose/) folder contains all the configuration files needed for spinning up the database set-up.

### 1.4.4. scripts

The [scripts](./scripts/) folder contains random scripts needed for the project XD

## 1.5. Configuration

Trying to imitate the JS style of loading configuration to your app.

```
number_of_tickers: <int>
data_interval: "<int>d/<int>h" (in days/hours)
data_period: <int> (in years)

db:
  stock_tickers_table: "tickers"
  stock_prices_table: "stock_price"


POSTGRES_HOST: localhost
POSTGRES_USER: postgres
POSTGRES_DB: postgres
POSTGRES_PASSWORD: 1234
POSTGRES_PORT: 5432
```

## 1.6. Makefile

## 1.7. What's next?

- Handle data about the finances and fundamentals of the companies.
