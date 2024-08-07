start-local-docker:
	docker compose --env-file ./docker.env  -f docker-compose.local.yml up --build 
