from configparser import NoSectionError


class ConfigurationFileNotFoundError(FileNotFoundError):
    """Configuration file setup.cfg not found."""
    pass


class ConfigurationFileSectionNotFoundError(NoSectionError):
    """Configuration section in setup.cfg not found."""
    pass


class ConfigurationFileSectionKeysMissingError(Exception):
    """Configuration section key in setup.cfg not found."""
    pass


class EnvironmentVariableRequired(Exception):
    """Envionment variable is required."""
    def __init__(self, env):
        self.env = env

    def __str__(self):
        return repr('{} environment variable is required!'.format(self.env))
