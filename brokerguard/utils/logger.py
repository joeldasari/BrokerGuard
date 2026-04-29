"""Logging utilities for BrokerGuard."""

from __future__ import annotations

import logging
from pathlib import Path


def setup_logger(log_file: str = "brokerguard.log", level: int = logging.INFO) -> logging.Logger:
    """Configure and return the application logger."""
    logger = logging.getLogger("brokerguard")
    logger.setLevel(level)

    # Avoid adding duplicate handlers when scanner is called multiple times.
    if logger.handlers:
        return logger

    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(Path(log_file), encoding="utf-8")
    file_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    return logger
