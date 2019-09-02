import logging
import configparser
import os
import re
import xml.etree.ElementTree as ET
from enum import Enum

def parse_config(config_path):
    config_file_path = os.path.abspath(config_path)
    logging.debug("Reading config from {}".format(config_file_path))
    if not os.path.exists(config_file_path):
        raise ConfigException("Config file path is not valid")
    config = configparser.ConfigParser()
    config.read(config_file_path)
    config_dict = dict()
    for section in config.sections():
        config_dict[section] = dict()
        options = config.options(section)
        for option in options:
            value = config.get(section, option)
            value = check_for_bool(value)
            config_dict[section][option] = value
    return config_dict

def check_for_bool(value):
    if value.lower() == 'true':
        return True
    elif value.lower() == 'false':
        return False
    else:
        return value

# Use this exception for problems in the server configuration
class ConfigException(Exception):
    pass
