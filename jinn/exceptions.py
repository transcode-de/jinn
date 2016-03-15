from configparser import NoSectionError


class ConfigurationFileNotFoundError(FileNotFoundError):
    pass



class ConfigurationFileSectionNotFoundError(NoSectionError):
    pass


class ConfigurationFileSectionKeysMissingError(Exception):
    pass
