import logging
import threading
import os
from logging.handlers import TimedRotatingFileHandler


class LoggerSingleton:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(LoggerSingleton, cls).__new__(cls)
                    cls._instance._initialize_logger()
        return cls._instance

    def _initialize_logger(self):
        self.logger = logging.getLogger("WeatherPipelineLogger")
        self.logger.setLevel(logging.INFO)

        if not self.logger.handlers:
            console_handler = logging.StreamHandler()
            console_formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
            )

            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)

            os.makedirs("logs", exist_ok=True)

            # File handler with timed rotation (daily)
            file_handler = TimedRotatingFileHandler(
                filename="logs/pipeline.log",
                when="midnight",
                interval=1,
                backupCount=7,
                encoding="utf-8",
                delay=False,
            )
            file_formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
            )
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)


def get_logger(name):
    instance = LoggerSingleton()
    return instance.logger.getChild(name)
