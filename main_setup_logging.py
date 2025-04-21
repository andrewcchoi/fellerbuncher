import atexit
import json
import logging.config
import logging.handlers
import pathlib

lumberjack = logging.getLogger(__name__)

def setup_logging():
    config_file = pathlib.Path("harvesting_configs/harvesterConfig.json")
    with open(config_file) as f_in:
        harvester = json.load(f_in)

    logging.config.dictConfig(harvester)
    queue_handler = logging.getHandlerByName("queue_handler")
    if queue_handler is not None:
        queue_handler.listener.start()
        atexit.register(queue_handler.listener.stop)


def main():
    setup_logging()
    logging.basicConfig(level="INFO")
    lumberjack.debug("debug message", extra={"acdc": "sample line"})
    lumberjack.info("info message")
    lumberjack.warning("warning message")
    lumberjack.error("error message")
    lumberjack.critical("critical message")

    try:
        1 / 0
    except ZeroDivisionError:
        lumberjack.exception("exception message:\n")


if __name__ == "__main__":
    main()
