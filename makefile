db-up:
	docker-compose -f ./docker/timescale_docker-compose.yaml up -d

db-down:
	docker-compose -f ./docker/timescale_docker-compose.yaml down