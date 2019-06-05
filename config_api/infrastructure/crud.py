"""GETTERS"""

from config_api.infrastructure.exception import InvalidParameterException
from config_api.model.environment_config import ENVIRONMENTS


def get_application(application):
    """Get application info"""
    try:
        return ENVIRONMENTS[application]
    except KeyError:
        raise InvalidParameterException(
            "ERROR: Invalid applicationlication name (%s) supplied." % (
                application.__repr__()
            ),
        )


def get_env(application, env):
    """Get env info"""
    try:
        return ENVIRONMENTS[application][env]
    except KeyError:
        raise InvalidParameterException(
            "ERROR: Invalid applicationlication name (%s) or environment name (%s) supplied." % (  # noqa
                application.__repr__(),
                env.__repr__()
            ),
        )


def get_param(application, env, param):
    """Get param for env"""
    try:
        return ENVIRONMENTS[application][env][param]
    except KeyError:
        raise InvalidParameterException(
            "ERROR: Invalid applicationlication name (%s), environment name (%s) or parameter (%s) supplied." % (  # noqa pylint: disable=line-too-long
                application.__repr__(),
                env.__repr__(),
                param.__repr__()
            ),
        )
