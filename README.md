# Data Downloader

The purpose of This project is to populate an SQL database with stock data.

## Glossary

- `Stocks list table` An SQL table that contains all the stocks` tickers/names that we want to get their historical price data into the "stock price" tables.
- `Stock Price table` This is a table that contains all the historical stock prices, this table is indexed as a hyper-table, which means it is optimized for time series data. Table columns are date, ticker, open, high, low, close, close_adj, and volume. the table's primary key is (ticker, date).

## Dependencies

Get to know and install the next tools:

- [pyenv](https://github.com/pyenv/pyenv#installation)
- [poetry](https://python-poetry.org/docs/#installation) (use the link to install, do not use brew)
- [docker](https://docs.docker.com/get-docker/)
- [docker-compose](https://docs.docker.com/compose/install/)


## Local Development

### Initiate the Database

To start developing locally you will need to:

1. Install [dependencies](#dependencies)
2. Start your timescaleDB engines ON.
   1. `make db-up` Spin up a timescaleDB via docker-compose. you can see the running containers with "docker ps" command.
   2. Open the browser at http://localhost:9000 for the PGAdmin UI.
   3. Connect with `my@email.com` and `password`
   4. Click `Add new server`.
      1. On the first page name=`postgres`.
      2. On `connection` page host=`timescale` username=`postgres` pass=`1234`.
   5. Click `Save`.
   6. `make db-init` Create tables and indices.
   7. `make db-populate` Populate the [stocks list table](#glossary).
3. `poetry install` to install python libraries in the poetry virtual environment.
4. `make start` Run the data downloader python code  (via poetry) and start downloading stocks data!


### Connect to the DB UI

1. Visit http://localhost:9000
2. Fill
   1. Email/Username: `my@email.com`
   2. Password: `password`
3. Press the login button.


### Start Downloading Data


```sh
make start
```

## Project design

### db_cli.py & db_vars.py
`db_vars.py` Contains commands for creating tables, creating indices, and populating the "tickers" table. used by `db_cli.py`.
`db_cli.py` Is a command line tool for DB administration.
`helpers.py` contains helpers functions, which can be also called "utils", right now containing only a "load_config" function.
`timescale.py` A class file that encapsulates all the functionality that we need for interacting with our timescaleDB.
`yahoo.py` A class file that encapsulates all the functionality that we need for interacting with yahoo API for getting data about stocks.


# Create Server command 
<!-- TODO: This is not tested yet, test it, make it work, and add this to db_cli -->
```sql
CREATE SERVER IF NOT EXISTS postgres2 FOREIGN
DATA WRAPPER postgres_fdw
OPTIONS (host 'timescale', dbname 'postgres', port '5432');
```
[Reference](https://www.postgresql.org/docs/current/sql-createserver.html)
