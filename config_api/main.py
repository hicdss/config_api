"""Environment configuration API"""

import os
from flask import Flask

app = Flask(__name__)  # pylint: disable=invalid-name
app.config['SECRET_KEY'] = 'secret!'
VERSION = '0.2'

ROOT_RESOURCE_NAME = os.environ.get('ROOT_RESOURCE_NAME')
app.config['ROOT_RESOURCE_NAME'] = ROOT_RESOURCE_NAME

from config_api.controller import api  # noqa pylint: disable=wrong-import-position,unused-import
