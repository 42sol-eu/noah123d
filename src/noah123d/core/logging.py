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
    basicConfig, DEBUG, INFO, WARNING, ERROR, CRITICAL
)  #!md| [docs](https://docs.python.org/3/library/logging.html)

# Configure logging to use RichHandler for beautiful output
basicConfig(
    level=DEBUG,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()]
)
