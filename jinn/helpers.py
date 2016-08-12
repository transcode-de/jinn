import configparser
import importlib
import inspect
import logging
import os
from distutils.util import strtobool

from . import exceptions

logging.basicConfig(level=logging.INFO)
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
    if env is not None:
        command = 'envdir {envdir} {command}'.format(
            envdir=os.path.join('envs', env),
            command=command
        )
    return command


def confirmation_prompt(question):
    """Helper to ask user for confirmation."""
    attempts = 3
    logger.info("{} (y/n)\n".format(question))
    while attempts > 0:
        attempts -= 1
        try:
            return strtobool(input().lower())
        except ValueError:
            logger.info("Please respond with \"y\" or \"n\".\n")


def load_config_section(keys, section=None):
    """Helper to load config sections from setup.cfg."""
    try:
        config = configparser.ConfigParser()
        config.read_file(open(determine_config_path()))
        if section is not None:
            prefixed_section = 'jinn:{section}'.format(section=section)
        else:
            prefixed_section = 'jinn'
        config_section = dict(config.items(prefixed_section))
        if set(keys) <= set(config_section.keys()):
            if section is not None:
                return {section: config_section}
            else:
                return config_section
        else:
            msg = "".join([
                "You need the keys '{keys}' in section '{prefixed_section}'",
                "\nBut you only have the keys '{config_keys}'."
            ]).format(
                keys=', '.join(keys),
                prefixed_section=prefixed_section,
                config_keys=', '.join(config_section.keys())
            )
            raise exceptions.ConfigurationFileSectionKeysMissingError(msg)
    except FileNotFoundError as f:
        msg = "".join([
            "Can not find a configuration file '{CONFIG_FILE}' in the current working"
            " directory {cwd}."
        ]).format(
            CONFIG_FILE=CONFIG_FILE,
            cwd=os.getcwd(),
        )
        raise exceptions.ConfigurationFileNotFoundError(f, msg)
    except configparser.NoSectionError:
        msg = "".join([
            "There is no section '{prefixed_section}', but there should be one",
            " in the configuration file '{CONFIG_FILE}'."
        ]).format(
            prefixed_section=prefixed_section,
            CONFIG_FILE=CONFIG_FILE
        )
        raise exceptions.ConfigurationFileSectionNotFoundError(msg)


def add_tasks(ns, tasks):
    """Import task modules listed in config and made them available."""
    for module_name in tasks.splitlines():
        if module_name:
            ns.add_collection(importlib.import_module(module_name))


def module_name(filename):
    """Get module name from file name."""
    return inspect.getmodulename(filename)


def determine_config_path():
    """Helper to determine setup.cfg path."""
    path = CONFIG_FILE
    env = os.environ.get('JINN_CONFIG_PATH')
    if env:
        path = os.path.join(env, CONFIG_FILE)
    return path
