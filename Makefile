# Variables
COMPOSE_DEV=app/docker-compose.dev.yaml
COMPOSE_PROD=deploy/docker-compose.prod.yaml
COMPOSE_PROD_ENV=deploy/compose.env

# Targets
.PHONY: dev up down prod-up prod-down migrate

DC_PROD=docker-compose -f $(COMPOSE_PROD) --env-file $(COMPOSE_PROD_ENV)
DC_DEV=docker-compose -f $(COMPOSE_DEV)

# Development
dev-build:
	$(DC_DEV) build --no-cache
	
dev-up:
	$(DC_DEV) up -d

dev-stop:
	$(DC_DEV) stop

dev-down:
	$(DC_DEV) down

dev-logs:
	$(DC_DEV) logs -f

dev-ps:
	$(DC_DEV) ps

dev-enter:
	$(DC_DEV) exec app sh

# Production
prod-up:
	$(DC_PROD) up -d

prod-stop:
	$(DC_PROD) stop

prod-down:
	$(DC_PROD) down

prod-logs:
	$(DC_PROD) logs -f

prod-ps:
	$(DC_PROD) ps