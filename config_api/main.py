"""Environment configuration API"""

from flask import Flask

app = Flask(__name__)  # pylint: disable=invalid-name
app.config['SECRET_KEY'] = 'secret!'
VERSION = '0.1'

from config_api.controller import api  # noqa pylint: disable=wrong-import-position,unused-import
