# flake8: noqa
import structlog

from katubi.settings import *

# -------
# Logging
# -------

# Add indentation to the JSON logging to make it easier to read.
LOGGING["formatters"]["json"]["processor"] = structlog.processors.JSONRenderer(indent=4)  # type: ignore[index]
