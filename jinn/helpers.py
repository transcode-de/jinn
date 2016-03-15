import configparser
import importlib
import logging
import os
from distutils.util import strtobool

from jinn import exceptions

logger = logging.getLogger(__name__)
CONFIG_FILE = 'setup.cfg'

INVOKE_CONFIG = {
    'run': {
        'echo': True,
        'pty': True,
    }
}


def envdir(ctx, command, env=None):
    """Helper to wrap command in envdir command with given env."""
    return 'envdir {envdir} {command}'.format(
        envdir=os.path.join('envs', env or 'dev'),
        command=command
    )


def confirmation_prompt(question):
    """Helper to ask user for confirmation."""
    logger.info("{} (y/n)\n".format(question))
    while True:
        try:
            return strtobool(input().lower())
        except ValueError:
            logger.info("Please respond with \"y\" or \"n\".\n")


def load_config_section(section, keys):
    """Helper to load config sections from setup.cfg."""
    try:
        config = configparser.ConfigParser()
        config.read_file(open(CONFIG_FILE))
        config.read(CONFIG_FILE)
        if section:
            prefixed_section = 'jinn:{section}'.format(section=section)
        else:
            prefixed_section = 'jinn'
        config_section = dict(config.items(prefixed_section))
        if set(keys) <= set(config_section.keys()):
            if section:
                return {section: config_section}
            else:
                return config_section
        else:
            msg = "".join([
                "You need the keys \'{keys}\' in section \'{prefixed_section}\'",
                "\nBut you only have the keys \'{config_keys}\'."
            ]).format(
                keys=', '.join(keys),
                prefixed_section=prefixed_section,
                config_keys=', '.join(config_section.keys())
            )
            raise exceptions.ConfigurationFileSectionKeysMissingError(msg)
    except FileNotFoundError as f:
        msg = "".join([
            "Can not find a configuration file '{CONFIG_FILE}' in the current working"
            " directory."
        ]).format(
            CONFIG_FILE=CONFIG_FILE
        )
        raise exceptions.ConfigurationFileNotFoundError(f, msg)
    except configparser.NoSectionError:
        msg = "".join([
            "There is no section \'{prefixed_section}\', but there should be one",
            " in the configuration file \'{CONFIG_FILE}\'."
        ]).format(
            prefixed_section=prefixed_section,
            CONFIG_FILE=CONFIG_FILE
        )
        raise exceptions.ConfigurationFileSectionNotFoundError(msg)


def add_tasks(ns, tasks):
    if tasks is not None:
        for module_name in tasks.splitlines():
            if module_name:
                ns.add_collection(importlib.import_module(module_name))
