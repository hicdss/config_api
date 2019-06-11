DOCKER_IMAGE=config_api
VERSION?=latest

run: pull down
	docker run -p 8888:8888 --name config_api -d $(DOCKER_IMAGE):$(VERSION)

build:
	docker build -t $(DOCKER_IMAGE):$(VERSION) .

down:
	-docker rm -f config_api

logs:
	docker logs config_api

test_in_docker:
	docker run -w /config_api -v $(shell pwd):/config_api -t hicrondss/python-linter:latest bash -c "pylint config_api && pycodestyle config_api"

test:
	pylint config_api
	pycodestyle config_api

pull:
	-docker pull $(DOCKER_IMAGE):$(VERSION)

push:
	docker push $(DOCKER_IMAGE):$(VERSION)
