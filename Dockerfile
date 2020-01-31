FROM tiangolo/meinheld-gunicorn-flask:python3.7-alpine3.8

MAINTAINER wojciech.puchta@hicron.com

ENV MODULE_NAME=config_api.main
ENV PORT=8888
ENV ROOT_RESOURCE_NAME=config-api

COPY config_api /app/config_api
