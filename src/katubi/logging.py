from typing import Optional

import structlog


def get_logger(area: Optional[str] = None) -> structlog.stdlib.BoundLogger:
    """
    Get a logger.
    """
    if area:
        name = "katubi." + area
    else:
        name = "katubi"

    return structlog.get_logger(name)
