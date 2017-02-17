import ConfigParser
import os

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
config_file_path = os.path.join(ROOT_PATH, 'config.ini')

config = None
if config is None:
	config = ConfigParser.ConfigParser()
	config.read(config_file_path)

def get_value(section, key):
	return config.get(section, key)