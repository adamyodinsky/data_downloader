# 1. Data Downloader

- [1. Data Downloader](#1-data-downloader)
  - [1.1. Glossary](#11-glossary)
  - [1.2. Local Development](#12-local-development)
    - [1.2.1. Dependencies](#121-dependencies)
    - [1.2.2. Step-by-step instructions](#122-step-by-step-instructions)
  - [1.3. Using The Data Downloader CLI](#13-using-the-data-downloader-cli)
  - [1.4. Project Structure](#14-project-structure)
    - [1.4.1. base folder](#141-base-folder)
    - [1.4.2. data\_downloader](#142-data_downloader)
    - [1.4.3. docker\_compose](#143-docker_compose)
    - [1.4.4. scripts](#144-scripts)
  - [1.5. Makefile](#15-makefile)
  - [1.6. Environment Variables](#16-environment-variables)
  - [1.7. What's next?](#17-whats-next)


A command line tool that can populate a timescaleDB database with historical price data of stocks.
The project uses [the Yahoo API python package](https://pypi.org/project/yfinance/) to fetch the data and [timescaleDB](https://www.timescale.com/) as a time-series database that stores the data.

## 1.1. Glossary

- `Stocks list table` An SQL table that contains all the stocks` tickers/names that we want to get their historical price data into the "stock price" tables.
- `Stock Price table` This is a table that contains all the historical stock price data, this table is indexed as a hyper-table, which means it is optimized for time series data. Table columns are date, ticker, open, high, low, close, close_adj, and volume. the table's index and primary key are (ticker, date).


## 1.2. Local Development

### 1.2.1. Dependencies

Get to know and install the next tools:

- [poetry](https://python-poetry.org/docs/#installation) (use the link to install, do not use brew)
- [docker](https://docs.docker.com/get-docker/)
- [docker-compose](https://docs.docker.com/compose/install/)


### 1.2.2. Step-by-step instructions

To start developing locally you will need to:

1. Install the [dependencies](#121-dependencies).
2. Start your timescaleDB engines ON.
   1. `make db-up` Spin up a timescaleDB via docker-compose. you can see the running containers with "docker ps" command.
   2. Open the browser at http://localhost:9000 for the PGAdmin UI.
   3. Connect with `my@email.com` and `password`
   4. Click `Add new server`.
      1. On the first page name=`postgres`.
      2. On `connection` page host=`timescale` username=`postgres` pass=`1234`.
   5. Click `Save`.
   6. `make db-init-tables` Create tables and indices.
   7. `make db-populate-tickers-table` Populate the [stocks list table](#11-glossary).
3. `make setup` to install python libraries in the poetry virtual environment.
4. [Run the data downloader](#13-using-the-data-downloader-cli)



## 1.3. Using The Data Downloader CLI

`make run-get-stocks-data ENV=<env_folder> ARGS=<args>`

```txt
Download historical price data for a list of stocks.

Arguments:
  -n, --number-of-tickers INTEGER (optional)
                                  Number of tickers to iterate over.
  -t, --tickers TEXT  (optional)  List of tickers to iterate over, separated
                                  with whitespace. 
  --help                          Show this message and exit.
```

`make run-get-stock-data ENV=<env_folder> ARGS=<args>`

```txt
Download a specific stock historical price data

Arguments:
  -t, --ticker TEXT  (required)   A single stock ticker 
      --help                      Show this message and exit.
```

**Note: Command line inputs override env variable values.**


## 1.4. Project Structure

### 1.4.1. base folder

- `Dockerfile` A docker file to build a data_downloader image.
- `Makefile` A make-file that contains shortcuts for useful commands within the context of the project, [see available commands description](#15-makefile).


### 1.4.2. data_downloader

[data_downloader](./data_downloader/) The python source code folder that populates an SQL database with data about stocks.

- [`db_vars.py`](./data_downloader/db_vars.py) Contains commands for creating tables, creating indices, and populating the "tickers" table. used by `db_cli.py`.
- [`db_cli.py`](./data_downloader/db_cli.py) Is a command line tool for DB administration.
- [`helpers.py`](./data_downloader/helper.py) contains helpers functions, which can be also called "utils", right now containing only a "load_config" function.
- [`timescale.py`](./data_downloader/timescale.py) A file that contains a class that encapsulates all the functionality for interacting with our timescaleDB.
- [`yahoo.py`](./data_downloader/yahoo.py) A file with all the functions needed for interacting with yahoo API for getting data about stocks.
- [`data_downloader.py`](./data_downloader/main.py) The entry-point for a command line tool that downloads stocks' data from yahoo.

Under [`data_downloader/files`](./data_downloader//files/) you can find CSV files that contain the data needed for the initial population of the ["stocks list table"](#11-glossary), and a `.env` file for local development.

### 1.4.3. docker_compose

The [docker_compose](./docker_compose/) folder contains all the configuration files needed for spinning up the database set-up.

### 1.4.4. scripts

The [scripts](./scripts/) folder contains random scripts needed for the project XD.

Currently, there is only a script used for installing poetry in the data_downloader docker image. this is done with a local file instead of fetching it from the web with curl. Docker does not recognize it's the same layer when being fetched from the web, this results in undesired rebuilding of all the layers, again and again, not using the docker layers caching mechanism.


## 1.5. Makefile

A make-file that contains shortcuts for useful commands within the context of the project.

- `db-up` Spin up the database containers ("pgadmin" and "timescale") using docker-compose.
- `db-down` Remove the database containers and networks using docker-compose.
- `db-stop` Stop the database containers using docker-compose.
- `db-rm-volumes` Remove the database containers, networks, and volumes using docker-compose.
- `db-init-tables` Create tables and indices.
- `db-populate-tickers-table` Populate the [stocks list table](#11-glossary).
- `db-delete-tables-content` Delete all table's content.
- `make run-get-stock-data ARGS=<args>` Run data_downloader cli to download specific stock data, use "ARGS=--help" to see all available options.
- `make run-get-stock-data ARGS=<args>` Run data_downloader cli to download data for a list of stocks, use "ARGS=--help" to see all available options.
- `docker-build-data-downloader` build a docker image for data_downloader
- `run-data-downloader-container` Run data_downloader container.
- `run-data-downloader-container-interactive` Run data_downloader container in interactive mode (bash).
- `run-data-downloader-container-deatched` Run data_downloader container in detached head mode.
- `format` Format the python code of the project.
- `setup` Set poetry to create a virtual environment in the project folder and installs python dependencies.


## 1.6. Environment Variables

- `ENV_FILE_PATH` *(optional)* Environment variables.
- `TICKERS` *(optional)* A whitespace-separated tickers list, for example: "MSFT ADSK GOOGL".
- `NUMBER_OF_TICKERS` *(optional)* Number of tickers to iterate over.
- `DATA_PERIOD` *(optional)* How back to get data from in years.
- `DATA_INTERVAL` *(optional)* Interval of price data in days/hours (examples: "1d" or "1h").
- `DB_STOCK_TICKERS_TABLE` *(required)* Ticker tables name in timescaleDB.
- `DB_STOCK_PRICE_TABLE` *(required)* Stock price table name in timescaleDB.
- `POSTGRES_DB` *(required)* Database name.
- `POSTGRES_HOST` *(required)* Postgres domain name.
- `POSTGRES_PORT` *(required)* Postgres port.
- `POSTGRES_USER` *(required)* Postgres username.
- `POSTGRES_PASSWORD` *(required)* Postgres password.

**Note: Command line inputs override env variable values.**

## 1.7. What's next?

- Download data about the finances and fundamentals of the companies.
