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
   6. `make db-init-tables` Create tables and indices.
   7. `make db-populate-tickers-table` Populate the [stocks list table](#11-glossary).
3. `poetry install` to install python libraries in the poetry virtual environment.
4. `make start` Run the data downloader python code  (via poetry) and start downloading stocks data!


## 1.4. Project Structure

### 1.4.1. base folder

- `config.yaml` A configuration file for the data_downloader, [see more about this file](#15-configuration).
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

The [scripts](./scripts/) folder contains random scripts needed for the project XD.

Currently, there is only a script used for installing poetry in the data_downloader docker image. this is done with a local file instead of fetching it from the web with curl. Docker does not recognize it's the same layer when being fetched from the web, this results in undesired rebuilding of all the layers again and again, not using the docker layers caching mechanism.

## 1.5. Configuration

<!-- TODO consider replacing the config file with env vars -->
A configuration file for the data_downloader to globally consume.


```
number_of_tickers: <int> // number of tickers to iterate over
data_period: <int> // how back to get data from in years
data_interval: "<int>d/<int>h" // interval of prices data in days/hours

db:
  stock_tickers_table: <str> // ticker tables name in postgres
  stock_prices_table: <str> // stock price table name in postgres


POSTGRES_DB: <str> // database name
POSTGRES_HOST: <str> // postgres domain name
POSTGRES_PORT: <int>
POSTGRES_USER: <str>
POSTGRES_PASSWORD: <str>
```

## 1.6. Makefile

- `db-up` Spin up the database containers ("pgadmin" and "timescale") using docker-compose.
- `db-down` Remove the database containers and networks using docker-compose.
- `db-stop` Stop the database containers using docker-compose.
- `db-rm-volumes` Remove the database containers, networks, and volumes using docker-compose.
- `db-init-tables` Create tables and indices.
- `db-populate-tickers-table` Populate the [stocks list table](#11-glossary).
- `db-delete-tables-content` Delete all table's content.
- `run-data-downloader` Run data_downloader python code as a process via poetry.
- `docker-build-data-downloader` build a docker image for data_downloader
- `run-data-downloader-container` Run data_downloader container.
- `run-data-downloader-container-interactive` Run data_downloader container in interactive mode (bash).
-  `run-data-downloader-container-deatched` Run data_downloader container in detached head mode.
-  `format` Format the python code of the project

## 1.7. What's next?

- Handle data about the finances and fundamentals of the companies.
