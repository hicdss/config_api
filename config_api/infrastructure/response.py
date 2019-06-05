"""Response decorators"""

from json import dumps
from flask import Response
from config_api.main import VERSION

HEADERS = {
    "X-CONFIG-API-VERSION": VERSION,
}


def _set_headers(response, override):
    for header_name, header_value in HEADERS.items():
        response.headers[header_name] = header_value
    for header_name, header_value in override.items():
        response.headers[header_name] = header_value
    return response


def json_response(func):
    """Wrapper for JSON reponses"""
    def wrapper(*args, **kwargs):
        response = Response(dumps(func(*args, **kwargs)))
        return _set_headers(response, {'Content-Type': 'application/json'})
    return wrapper
