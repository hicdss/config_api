"""REST API controllers."""

from config_api.main import app  # pylint: disable=cyclic-import
from config_api.main import VERSION
from config_api.infrastructure.crud import get_param
from config_api.infrastructure.response import json_response


@app.route('/%s/version' % (app.config['ROOT_RESOURCE_NAME']), methods=['GET'], endpoint='version')  # noqa pylint: disable=line-too-long
@json_response
def get_version_info():
    """GET: app version"""
    return {
        "name": "config_api",
        "version": VERSION,
        "code": "https://github.com/hicdss/config_api/"
    }


@app.errorhandler(404)
@json_response
def get_param_or_404(error):  # pylint: disable=unused-argument
    """Dynamic controller"""
    return get_param()
