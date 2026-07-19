"""
Dependency Injection Container
"""

from ..config.configuration import Configuration
from ..utils.logger import Logger


class Container:

    def __init__(self):

        self.configuration = Configuration()

        self.logger = Logger.get_logger()