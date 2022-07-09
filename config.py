"""Please make sure computer have environment of APP_SETTINGS
If not, in CMD: set APP_SETTINGS=config.XXXConfig
XXX is either Production/Local/Development/Testing
"""
import datetime
import os
import json
import logging
import logging.config
import platform
import xml.etree.ElementTree
import lxml.etree as etree

logger_charset_normalizer = logging.getLogger('charset_normalizer')
logger_charset_normalizer.setLevel(logging.CRITICAL)


_dir_path     = os.path.dirname(os.path.realpath(__file__))
_config_file  = os.path.join(_dir_path, 'learning_grpc.config')


try:
    root = xml.etree.ElementTree.parse(_config_file).getroot()
    node = etree.parse(_config_file)
except Exception as e:
    #logging not configed yet
    print('error in xml.etree.ElementTree.parse({}).getroot()'.format(_config_file))
    ## TODO assign the root
    raise e

class Config(object):
    _log_path         = node.xpath('//add[@key="logPath"]')[0].attrib['value']
    _log_path         = '' if _log_path is None else _log_path
    replace_arg = ("/", "\\")
    if platform.system() != "Windows":
        replace_arg = ("", "")
    LOG_PATH = _log_path if os.path.isabs(_log_path) \
        else os.path.join(_dir_path, _log_path.replace(*replace_arg))
    for path in (LOG_PATH, ):
        os.makedirs(path, exist_ok=True)
    with open(os.path.join(_dir_path, "logging.json"), 'r') as f:
        LOGGING_CONFIG = json.load(f)
    FNAME = 'learning_grpc'+ datetime.datetime.now().strftime('%Y-%m-%d')+'.log'
    LOGGING_CONFIG['handlers']['file_handler']['filename'] = os.path.join(LOG_PATH, FNAME)

    logging.config.dictConfig(LOGGING_CONFIG)
    LOGGER = logging.getLogger(__name__)



try:
    CONFIG = Config()
except Exception as e:
    # logging not configed yet
    print('error in Config() {0}'.format(e))
    ## TODO make new CONFIG
    raise e
