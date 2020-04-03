import logging
import logging.config

from ruamel import yaml

log_conf_file = 'logconf.yml'

with open(log_conf_file, 'rb') as f:
    conf_dict = yaml.load(f, Loader=yaml.Loader)
logging.config.dictConfig(conf_dict)
logger = logging.getLogger('root')
