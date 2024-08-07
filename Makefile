CURRENT_DIR := $(shell pwd)

# Цветовые коды
GREEN  = \033[0;32m
RESET  = \033[0m

start-local-docker:
	docker compose --env-file ./docker.env  -f docker-compose.local.yml up --build -d
	@bash -c 'source $(CURRENT_DIR)/docker.env && \
		echo -e "Service is running on $(GREEN) http://$$traefik_local_host$$traefik_local_path $(RESET)"'
