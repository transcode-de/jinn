from configparser import NoSectionError


class ConfigurationFileNotFoundError(FileNotFoundError):
    pass


class ConfigurationFileSectionNotFoundError(NoSectionError):
    pass


class ConfigurationFileSectionKeysMissingError(Exception):
    pass


class EnvironmentVariableRequired(Exception):
    def __init__(self, env):
        self.env = env

    def __str__(self):
        return repr('{} environment variable is required!'.format(self.env))
