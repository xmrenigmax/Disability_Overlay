# src/utils/logger.py
import os
import logging
from logging.handlers import RotatingFileHandler
from kivy.utils import platform
from typing import Optional

class AppLogger:
    """
    Centralized logging configuration for application.
    
    Features:
    - Log level management
    - File and console output
    - Log rotation
    - Platform-specific paths
    """
    
    # Log levels
    LEVELS = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    
    def __init__(self):
        self.logger = logging.getLogger('AppLogger')
        self.logger.setLevel(logging.INFO)
        
        # Prevent duplicate handlers
        if not self.logger.handlers:
            self._setup_logger()
    
    def _setup_logger(self) -> None:
        """Configure logger with handlers"""
        try:
            # Create formatters
            file_formatter = logging.Formatter(
                '%(asctime)s [%(levelname)s] %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            console_formatter = logging.Formatter(
                '[%(levelname)s] %(message)s'
            )
            
            # Add file handler
            file_handler = self._create_file_handler()
            if file_handler:
                file_handler.setFormatter(file_formatter)
                self.logger.addHandler(file_handler)
            
            # Add console handler
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)
            
        except Exception as e:
            print(f"Logger setup failed: {str(e)}")
    
    def _create_file_handler(self) -> Optional[RotatingFileHandler]:
        """Create platform-specific file handler"""
        try:
            # Get platform-specific log directory
            if platform == 'android':
                from android.storage import app_storage_path #type: ignore
                log_dir = os.path.join(app_storage_path(), 'logs')
            elif platform == 'ios':
                log_dir = os.path.expanduser('~/Documents/logs')
            else:  # Windows
                log_dir = os.path.join(os.getenv('APPDATA', ''), 'AccessibilityScanner', 'logs')
            
            # Create log directory if needed
            os.makedirs(log_dir, exist_ok=True)
            
            # Create rotating file handler
            log_file = os.path.join(log_dir, 'app.log')
            handler = RotatingFileHandler(
                log_file,
                maxBytes=1024 * 1024,  # 1MB
                backupCount=5
            )
            return handler
            
        except Exception as e:
            print(f"File handler creation failed: {str(e)}")
            return None
    
    def set_level(self, level: str) -> None:
        """Set logging level"""
        if level.upper() in self.LEVELS:
            self.logger.setLevel(self.LEVELS[level.upper()])
    
    def debug(self, message: str) -> None:
        """Log debug message"""
        self.logger.debug(message)
    
    def info(self, message: str) -> None:
        """Log info message"""
        self.logger.info(message)
    
    def warning(self, message: str) -> None:
        """Log warning message"""
        self.logger.warning(message)
    
    def error(self, message: str) -> None:
        """Log error message"""
        self.logger.error(message)
    
    def critical(self, message: str) -> None:
        """Log critical message"""
        self.logger.critical(message)

# Global logger instance
app_logger = AppLogger()

# Convenience functions
def debug(message: str) -> None:
    app_logger.debug(message)

def info(message: str) -> None:
    app_logger.info(message)

def warning(message: str) -> None:
    app_logger.warning(message)

def error(message: str) -> None:
    app_logger.error(message)

def critical(message: str) -> None:
    app_logger.critical(message)