FROM tiangolo/meinheld-gunicorn-flask:python3.7-alpine3.8

ENV MODULE_NAME=config_api.main
ENV PORT=8888

COPY config_api /app/config_api