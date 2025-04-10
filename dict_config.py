dict_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "base": {
            "format": "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
        }
    },
    "filters": {},
    "handlers": {
        "filehandler": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "filename": "calculator_logs.log",
            "mode": "a",
            "formatter": "base",
            "filters": []
        }
    },
    "loggers": {
        "logger": {
            "level": "DEBUG",
            "handlers": ["filehandler"],
            "propagate": False
        }
    }
}
