import os
import logging
from configparser import ConfigParser

# Path to this app
basedir: str = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode
DEBUG: bool = True

# Set config for logging
logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(asctime)s - %(message)s')

# Try to load config
def LoadConfig() -> ConfigParser:
    cfg = ConfigParser()

    # Absolute path to config file
    config_path = f"{basedir}\\config.ini"

    # Log error if config is not found
    if not os.path.exists(config_path):
        logging.error("Config could NOT be found ['%s'].\nYou can try to recreate config with config/create.py", config_path)
        exit(0)


    cfg.read(config_path)
    logging.info("Config found and loaded from '%s'", config_path)

    return cfg

CONFIG: ConfigParser = LoadConfig()