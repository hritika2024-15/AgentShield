from abc import ABC, abstractmethod
from utils.logger import setup_logger

class BaseAgent(ABC):
    def __init__(self, name):
        self.name = name
        self.logger = setup_logger(name, f"logs/{name}.log")
    
    @abstractmethod
    def run(self, *args, **kwargs):
        pass

    def log(self, message, level="info"):
        if level == "info":
            self.logger.info(message)
        elif level == "error":
            self.logger.error(message)
        elif level == "warning":
            self.logger.warning(message)
        elif level == "debug":
            self.logger.debug(message)
