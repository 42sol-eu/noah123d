# -*- coding: utf-8 -*-
"""
Simple constants for build123d projects.
----
file:
    name:       logging.py
    uuid:       ff1080ab-fa81-4ea1-a505-382d3c8fed82
description:    Simple constants for build123d projects
authors:         felix@42sol.eu
project:
    name:       noah123d
    uuid:       93fe70d7-2d29-4ebf-bf0e-51d75dbfda30
    url:        https://github.com/42sol-eu/noah123d
"""

from rich.logging import (
    RichHandler
)  #!md| [docs](https://rich.readthedocs.io/en/stable/logging.html)
from logging import (
    basicConfig,
    debug, info, warning, error, critical
)  #!md| [docs](https://docs.python.org/3/library/logging.html)

import logging


# Configure logging to use RichHandler for beautiful output
basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()]
)

class Log:
    @staticmethod
    def debug(msg, *args, **kwargs):
        logging.debug(msg, *args, **kwargs)

    @staticmethod
    def info(msg, *args, **kwargs):
        logging.info(msg, *args, **kwargs)

    @staticmethod
    def warning(msg, *args, **kwargs):
        logging.warning(msg, *args, **kwargs)

    @staticmethod
    def error(cls, msg, *args, **kwargs):
        logging.error(msg, *args, **kwargs)

    @staticmethod
    def critical(msg, *args, **kwargs):
        logging.critical(msg, *args, **kwargs)
