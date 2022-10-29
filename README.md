# Data Downloader

The purpose of This project is to populate an SQL database with stock data.

## Local Development

### Load python env

```sh
source ./.venv/bin/activate
```

### Initiate the Database

1. `make db-up`.
2. Open the browser at http://localhost:9000 for the PGAdmin UI.
   1. Connect with `my@email.com` and `password`
   2. Click `Add new server`.
      1. On the first page name=`postgres`.
      2. On `connection` page host=`timescale` username=`postgres` pass=`1234`.
   3. Click `Save`.
3. `make db-init` - Create tables and indices.
4. `make db-populate`- Populate the "tickers" table.

### Start Downloading Data

```sh
make start
```


## db_cli.py & db_vars.py
`db_vars.py` Contains commands for creating tables, creating indices, and populating the "tickers" table. used by `db_cli.py`.
`db_cli.py` Is a command line tool for DB administration.

