"""CRUD"""

from flask import request

from config_api.main import app  # pylint: disable=cyclic-import
from config_api.infrastructure.exception import InvalidParameterException
from config_api.model.environment_config import ENVIRONMENTS


def get_param():
    """Get requested parameter"""
    try:
        path = _url_path_as_iterable()
        value = ENVIRONMENTS
        for step in path:
            value = value[step]
        return value
    except (InvalidParameterException, KeyError, TypeError):
        return None


def _url_path_as_iterable():
    """Return URL path as list without empty strings"""
    path = [step for step in request.path.split('/') if step]
    if path == [] or path[0] != app.config['ROOT_RESOURCE_NAME']:
        raise InvalidParameterException('404')
    del path[0]
    return path
