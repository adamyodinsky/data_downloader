db-up:
	docker-compose -f ./docker-compose/timescale_docker-compose.yaml up -d

db-down:
	docker-compose -f ./docker-compose/timescale_docker-compose.yaml down

db-stop:
	docker-compose -f ./docker-compose/timescale_docker-compose.yaml stop

db-rm:
	docker-compose -f ./docker-compose/timescale_docker-compose.yaml down -v

db-init:
	CONFIG_PATH="./config.yaml" python3 ./data_downloader/db_cli.py init

db-populate:
	CONFIG_PATH="./config.yaml" python3 ./data_downloader/db_cli.py populate-tickers-table

start:
	CONFIG_PATH="./config.yaml" python3 data_downloader/main.py

docker-build:
	docker build . -t data_downloader

run-container_interactive:
	docker run -it data_downloader bash

run-container:
	docker run data_downloader

run-container_deatched:
	docker run -d data_downloader
