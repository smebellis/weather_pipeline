import logging
import threading


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
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
            )

            handler.setFormatter(formatter)
            self.logger.addHandler(handler)


def get_logger(name):
    instance = LoggerSingleton()
    logger = instance.logger
    return logger.getChild(name)
