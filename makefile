.PHONY: db-up db-down db-stop db-rm-volumes db-init-tables db-populate-tickers-table db-delete-tables-content run-data-downloader docker-build-data-downloader run-data-downloader-container-interactive run-data-downloader-container run-data-downloader-container-deatched format


db-up:
	docker-compose -f ./docker_compose/timescale_docker-compose.yaml up -d

db-down:
	docker-compose -f ./docker_compose/timescale_docker-compose.yaml down

db-stop:
	docker-compose -f ./docker_compose/timescale_docker-compose.yaml stop

db-rm-volumes:
	docker-compose -f ./docker_compose/timescale_docker-compose.yaml down -v

# db-create-server: # TODO make it work
# 	CONFIG_PATH="./config.yaml" poetry run python ./data_downloader/db_cli.py create-server

db-init-tables:
	CONFIG_PATH="./config.yaml" poetry run python ./data_downloader/db_cli.py init-tables

db-populate-tickers-table:
	CONFIG_PATH="./config.yaml" poetry run python ./data_downloader/db_cli.py populate-tickers-table

db-delete-tables-content:
	CONFIG_PATH="./config.yaml" poetry run python ./data_downloader/db_cli.py delete-tables-content

run-data-downloader:
	CONFIG_PATH="./config.yaml" poetry run python data_downloader/main.py

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
