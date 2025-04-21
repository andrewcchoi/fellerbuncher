import atexit
import json
import logging.config
import logging.handlers
import pathlib

from fellerbuncher import Fellerbuncher

lumberjack = logging.getLogger(__name__)

def main():
    # setup_logging()
    Fellerbuncher()
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
