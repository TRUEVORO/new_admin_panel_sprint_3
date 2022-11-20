THIS_FILE := $(lastword $(MAKEFILE_LIST))
.PHONY: help run stop down destroy restart logs
help:
	make -pRrq  -f $(THIS_FILE) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'
run:
	docker-compose -f docker-compose.yml up --build -d $(c)
stop:
	docker-compose -f docker-compose.yml stop $(c)
down:
	docker-compose -f docker-compose.yml down $(c)
destroy:
	docker-compose -f docker-compose.yml down -v $(c)
restart:
	docker-compose -f docker-compose.yml stop $(c)
	docker-compose -f docker-compose.yml up -d $(c)
etl-logs:
	docker-compose logs -f etl
