# from configparser import ConfigParser
import os
import json

def make_config():
    return json.load(open(os.path.join(os.environ['HOME'], '.hackfest'), 'r'))
    # _config = ConfigParser()
    # _config.read(os.path.join(os.environ['HOME'], '.hackfest'))
    # return dict(_config.items(os.getenv('CONFIG_SECTION', 'default')))

config = make_config()
print(config)
