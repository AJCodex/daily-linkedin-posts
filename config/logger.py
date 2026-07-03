"""
Structured logging utility for the entire pipeline.
Replaces print() statements with proper logging infrastructure.
"""

import logging
import logging.handlers
import os
from config.constants import LOG_FILE, LOG_LEVEL, LOG_FORMAT, LOG_DATE_FORMAT


def setup_logging(name: str, log_file: str = LOG_FILE) -> logging.Logger:
    """
    Configure and return a logger with both file and console handlers.
    
    Args:
        name: Module name for the logger
        log_file: Path to log file (default: config/constants.LOG_FILE)
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Avoid duplicate handlers if logger already configured
    if logger.handlers:
        return logger
    
    logger.setLevel(getattr(logging, LOG_LEVEL.upper(), logging.INFO))
    
    # Ensure log directory exists
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    # File handler (all levels)
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT))
    
    # Console handler (INFO and above only)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(
        "%(levelname)-8s | %(message)s",
        datefmt=LOG_DATE_FORMAT
    ))
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


class LoggerFactory:
    """Factory for getting loggers throughout the pipeline."""
    
    _loggers = {}
    
    @staticmethod
    def get(name: str) -> logging.Logger:
        """Get or create a logger by name."""
        if name not in LoggerFactory._loggers:
            LoggerFactory._loggers[name] = setup_logging(name)
        return LoggerFactory._loggers[name]


# Convenience functions
def get_logger(name: str) -> logging.Logger:
    """Quick access to get a logger."""
    return LoggerFactory.get(name)
