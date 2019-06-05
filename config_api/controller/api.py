"""REST API controllers."""

from config_api.main import app  # pylint: disable=cyclic-import
from config_api.model.environment_config import ENVIRONMENTS
from config_api.infrastructure.crud import get_app
from config_api.infrastructure.crud import get_env
from config_api.infrastructure.crud import get_param
from config_api.infrastructure.response import json_response


@app.route('/config-api/all', methods=['GET'], endpoint='get_all')
@json_response
def rest_get_all_configuration():
    """GET: full solar system configuration"""
    return ENVIRONMENTS


@app.route('/config-api/list', methods=['GET'], endpoint='get_list')
@json_response
def rest_get_app_list():
    """GET: list of planets"""
    return [application for application in ENVIRONMENTS]


@app.route('/config-api/<application>', methods=['GET'], endpoint='get_application')
@json_response
def rest_get_app(application):
    """GET: full configuration for a an application"""
    return get_app(application)


@app.route('/config-api/<application>/<env>', methods=['GET'], endpoint='get_env')
@json_response
def rest_get_env(application, env):
    """GET: full configuration for an environment"""
    return get_env(application, env)


@app.route('/config-api/<app>/<env>/<param>', methods=['GET'], endpoint='get_param')
@json_response
def rest_get_param(application, env, param):
    """GET: parameter by application and environment"""
    return get_param(application, env, param)
