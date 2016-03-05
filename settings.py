from configparser import ConfigParser
import os

def make_config():
    _config = ConfigParser()
    _config.read(os.path.join(os.environ['HOME'], '.hackfest'))
    return dict(_config.items(os.getenv('CONFIG_SECTION', 'default')))

config = make_config()
