DOCKER_COMPOSE = docker-compose
DOCKER_COMPOSE_FILE = docker-compose.yml

.PHONY: build serve up down logs

build:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) build

serve: build
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) up

up:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) up --build

down:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) down

logs:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) logs -f
