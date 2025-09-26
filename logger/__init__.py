# logger/__init__.py

import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime
from config import config

import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime
from config import config

class CustomLogger:
    """Custom logger with rotating files and configurable level."""

    def __init__(self, logger_name="CustomBot"):
        base_dir = os.path.dirname(os.path.abspath(__file__)) 
        log_dir = os.path.join(base_dir, config.get("logging", {}).get("log_directory", "logs"))
        os.makedirs(log_dir, exist_ok=True) 

        log_level = config.get("logging", {}).get("level", "INFO").upper()
        max_bytes = config.get("logging", {}).get("max_bytes", 10_485_760)  
        backup_count = config.get("logging", {}).get("backup_count", 5)
        rotate = config.get("logging", {}).get("rotate", True)

        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        log_file = os.path.join(log_dir, f"log_{timestamp}.log")

        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(getattr(logging, log_level, logging.INFO))

        if rotate:
            handler = RotatingFileHandler(
                log_file, maxBytes=max_bytes, backupCount=backup_count
            )
        else:
            handler = logging.FileHandler(log_file)

        formatter = logging.Formatter("[%(asctime)s] %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)

        if not self.logger.handlers:
            self.logger.addHandler(handler)

    def get_logger(self):
        return self.logger