import atexit
import json
import logging.config
import logging.handlers
import pathlib

def Fellerbuncher():
    config_file = pathlib.Path("harvesting_configs/harvesterConfig.json")
    with open(config_file) as f_in:
        harvester = json.load(f_in)

    logging.config.dictConfig(harvester)
    queue_handler = logging.getHandlerByName("queue_handler")
    if queue_handler is not None:
        queue_handler.listener.start()
        atexit.register(queue_handler.listener.stop)

