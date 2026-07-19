"""
GridForge Logging Service
"""

import logging
from pathlib import Path


class Logger:
    """
    Central logging service.
    """

    _logger = None

    @classmethod
    def get_logger(cls):

        if cls._logger:
            return cls._logger

        logger = logging.getLogger("GridForge")

        logger.setLevel(logging.INFO)

        if not logger.handlers:

            formatter = logging.Formatter(
                "%(asctime)s | %(levelname)s | %(message)s"
            )

            log_dir = Path.home() / "GridForge"

            log_dir.mkdir(exist_ok=True)

            log_file = log_dir / "gridforge.log"

            handler = logging.FileHandler(log_file)

            handler.setFormatter(formatter)

            logger.addHandler(handler)

        cls._logger = logger

        return logger