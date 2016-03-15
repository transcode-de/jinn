import configparser
import os
import sys
import logging
from distutils.util import strtobool

logger = logging.getLogger('jinn-helper')
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
        envdir=os.path.join('envs', env),
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
    if os.path.exists(CONFIG_FILE):
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)
        if section:
            prefixed_section = 'jinn:{section}'.format(section=section)
        else:
            prefixed_section = 'jinn'
        if prefixed_section in config.sections():
            section_config = dict(config.items(prefixed_section))
            if set(keys) == set(section_config.keys()):
                if section:
                    return {section:section_config}
                else:
                    section_config.update(INVOKE_CONFIG)
                    return section_config
            else:
                msg = "".join([
                    "You need the keys \'{keys}\' in section \'{prefixed_section}\'",
                    "\nBut you only have the keys \'{config_keys}\'."
                ]).format(
                    keys=', '.join(keys),
                    prefixed_section=prefixed_section,
                    config_keys=', '.join(section_config.keys())
                )
        else:
            msg = "".join([
                "There is no section \'{prefixed_section}\', but there should be one",
                " in the configuration file \'{CONFIG_FILE}\'."
            ]).format(
                prefixed_section=prefixed_section,
                CONFIG_FILE=CONFIG_FILE
            )
    else:
        msg = "".join([
            "Can not find a configuration file \'{CONFIG_FILE}\' in the current working"
            " directory."
            ]).format(
                CONFIG_FILE=CONFIG_FILE
            )
    logger.error(msg)
    sys.exit(os.EX_CONFIG)
