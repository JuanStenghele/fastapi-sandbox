import sys


from constants import LOGGER_NAME


LOGGING_CONFIG = {
  "version": 1,
  "disable_existing_loggers": False,
  "formatters": {
    "standard": {
      "format": "%(asctime)s - %(levelname)s - %(message)s",
      "datefmt": "%Y-%m-%d %H:%M:%S"
    },
    "standard_with_filepath": {
      "format": "%(asctime)s - %(levelname)s - %(message)s (%(pathname)s:%(lineno)d)",
      "datefmt": "%Y-%m-%d %H:%M:%S"
    }
  },
  "handlers": {
    "console": {
      "class": "logging.StreamHandler",
      "stream": sys.stdout,
      "formatter": "standard"
    },
    "console_with_filepath": {
      "class": "logging.StreamHandler",
      "stream": sys.stdout,
      "formatter": "standard_with_filepath"
    }
  },
  "loggers": {
    "uvicorn": {
      "handlers": ["console"],
      "level": "INFO",
      "propagate": False
    },
    "fastapi": {
      "handlers": ["console"],
      "level": "INFO",
      "propagate": False
    },
    LOGGER_NAME: {
      "handlers": ["console_with_filepath"],
      "level": "DEBUG",
      "propagate": False
    }
  }
}
