import atexit
import json
import logging.config
import logging.handlers
import pathlib

import _config as config

def logHarvestConfiguration(
    host: str, 
    port: str, 
    sender: str, 
    to: str, 
    user: str, 
    pwd: str,
    timeout: int = 5
) -> json:
  """Configure logging for the Fellerbuncher application."""

  harvestConfig = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
      "simple": {
        "format": "%(asctime)s: %(message)s",
        "datefmt": "%Y-%m-%dT%H:%M:%S%z"
      },
      "detailed": {
        "format": "%(asctime)s [%(levelname)s|%(module)s|L%(lineno)d]: %(message)s",
        "datefmt": "%Y-%m-%dT%H:%M:%S%z"
      },
      "json": {
        "()": "log_formatter.HarvestJSONFormatter",
        "fmt_keys": {
          "timestamp": "timestamp",
          "level": "levelname",
          "thread_name": "threadName",
          "task_name": "taskName",
          "logger": "name",
          "module": "module",
          "function": "funcName",
          "line": "lineno",
          "message": "message"
        }
      }
    },
    "filters": {
      "no_errors": {
        "()": "log_formatter.NonErrorFilter"
      }
    },
    "handlers": {
      "stdout": {
        "class": "logging.StreamHandler",
        "level": "INFO",
        "formatter": "simple",
        "stream": "ext://sys.stdout",
        "filters": ["no_errors"]
      },
      "stderr": {
        "class": "logging.StreamHandler",
        "level": "WARNING",
        "formatter": "detailed",
        "stream": "ext://sys.stderr"
      },
      "fellerbuncher_json": {
        "class": "logging.handlers.RotatingFileHandler",
        "level": "DEBUG",
        "formatter": "json",
        "filename": "logs/fellerbuncher.log.jsonl",
        "maxBytes": 400000,
        "backupCount": 3
      },
      "fellerbuncher_json_error": {
        "class": "logging.handlers.RotatingFileHandler",
        "level": "ERROR",
        "formatter": "json",
        "filename": "logs/fellerbuncher_error.log.jsonl",
        "maxBytes": 400000,
        "backupCount": 3
      },
      "fellerbuncher_mail": {
        "class": "logging.handlers.SMTPHandler",
        "level": "ERROR",
        "formatter": "json",
        "mailhost": (host,int(port)),
        "fromaddr": sender,
        "toaddrs": to,
        "subject": "Fellerbuncher Error",
        "credentials": (user,rf'{pwd}'),
        "secure": (),
        "timeout": timeout
      },
      "queue_handler": {
        "class": "logging.handlers.QueueHandler",
        "handlers": [
          "stdout",
          "stderr",
          "fellerbuncher_json",
          "fellerbuncher_json_error",
          "fellerbuncher_mail"
        ],
        "respect_handler_level": True
      }
    },
    "loggers": {
      "root": {
        "level": "DEBUG",
        "handlers": [
          "queue_handler"
        ]
      }
    }
  }
  return harvestConfig


def Fellerbuncher() -> None:
  """Initialize the Fellerbuncher application."""
  
  # Configure logging
  harvestConfig = logHarvestConfiguration(
    host=config.EMAIL_HOST, 
    port=config.EMAIL_PORT[1], 
    sender=config.EMAIL_SENDER, 
    to=config.EMAIL_TO, 
    user=config.EMAIL_USER, 
    pwd=config.EMAIL_PWD,
    timeout=1
  )

  # Create logs directory if it doesn't exist
  logs_dir = pathlib.Path("logs")
  logs_dir.mkdir(parents=True, exist_ok=True)

  logging.config.dictConfig(harvestConfig)
  queue_handler = logging.getHandlerByName("queue_handler")
  if queue_handler is not None:
    queue_handler.listener.start()
    atexit.register(queue_handler.listener.stop)


if __name__ == "__main__":
  
  lumberjack = logging.getLogger(__name__)
  
  Fellerbuncher()
  logging.basicConfig(level="DEBUG")

  lumberjack.info("Fellerbuncher started", extra={"acdc": "EXTRA INFO"})
  lumberjack.debug("Debugging information", extra={"acdc": "EXTRA DEBUG"})
  lumberjack.warning("Warning message", extra={"acdc": "EXTRA WARNING"})
  lumberjack.error("Error message", extra={"acdc": "EXTRA ERROR"})
  lumberjack.critical("Critical error message", extra={"acdc": "EXTRA CRITICAL"})

  try:
      1 / 0
  except ZeroDivisionError:
      lumberjack.exception("exception message:\n")