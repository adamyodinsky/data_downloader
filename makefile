.PHONY: db-up db-down db-stop db-rm-volumes db-init-tables db-populate-tickers-table db-delete-tables-content run-get-stock-data run-get-stocks-data docker-build-data-downloader run-data-downloader-container-interactive run-data-downloader-container run-data-downloader-container-deatched format


db-up:
	docker-compose -f ./docker_compose/timescale_docker-compose.yaml up -d

db-down:
	docker-compose -f ./docker_compose/timescale_docker-compose.yaml down

db-stop:
	docker-compose -f ./docker_compose/timescale_docker-compose.yaml stop

db-rm-volumes:
	docker-compose -f ./docker_compose/timescale_docker-compose.yaml down -v

# db-create-server: # TODO make it work
# 	poetry run python ./data_downloader/db_cli.py create-server

db-init-tables:
	TICKERS_CSV__FILE="${PWD}/files/dev/sp500_stocks.csv" ENV_FILE_PATH="${PWD}/files/$(ENV)/.env" poetry run python ./data_downloader/db_cli.py init-tables

db-populate-tickers-table:
	TICKERS_CSV__FILE="${PWD}/files/dev/sp500_stocks.csv" ENV_FILE_PATH="${PWD}/files/$(ENV)/.env"  poetry run python ./data_downloader/db_cli.py populate-tickers-table

db-delete-tables-content:
	poetry run python ./data_downloader/db_cli.py delete-tables-content

run-get-stock-data:
	ENV_FILE_PATH="${PWD}/files/$(ENV)/.env" poetry run python data_downloader/data_downloader.py get-stock-data $(ARGS)

run-get-stocks-data:
	ENV_FILE_PATH="${PWD}/files/$(ENV)/.env" poetry run python data_downloader/data_downloader.py get-stocks-data $(ARGS)

docker-build-data-downloader:
	docker build . -t data_downloader

run-data-downloader-container-interactive:
	docker run -it data_downloader bash

run-data-downloader-container:
	docker run data_downloader

run-data-downloader-container-deatched:
	docker run -d data_downloader

format:
	poetry run black . 

setup:
	poetry config virtualenvs.in-project true && poetry install
