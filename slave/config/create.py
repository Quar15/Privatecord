import logging
from configparser import ConfigParser

config = ConfigParser()

# Misc config options
config['DATA'] = {
    'secret': 'my precious',
    'name': 'Club Name',
    'description': 'Description',
}

# IP config options
config['IP'] = {
    'voice': '127.0.0.1',
    'masterwhitelist': ['127.0.0.1'],
    'banlist': []
}

# Database config options
config['DB'] = {
    'path': 'sqlite:///data/db.sqlite3',
    'name': 'db_name', 
    'user': 'db_user',
    'password': 'pass',
    'host': '127.0.0.1'
}

# Overwrite or create new config file
with open('config.ini', 'w') as configfile:
    config.write(configfile)

logging.info('New config.ini file created')