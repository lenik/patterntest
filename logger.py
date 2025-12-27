"""Logging module with level support and CR-based functions"""

import sys
import os
from typing import Optional


# ANSI color codes
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    # Standard colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'


def _is_color_enabled() -> bool:
    """Check if color should be enabled (default: True if stdout is TTY)"""
    # Check if NO_COLOR environment variable is set
    if os.environ.get('NO_COLOR'):
        return False
    # Check if stdout is a TTY
    return sys.stdout.isatty()


class Logger:
    """Logger with level-based filtering and CR support"""
    
    def __init__(self, level: int = 1, use_color: Optional[bool] = None):
        """
        Initialize logger
        
        Args:
            level: Log level (0=mesg, 1=info, -1=warn, -2=error, 2=log, 3=debug)
            use_color: Enable color output (default: auto-detect from TTY)
        """
        self.level = level
        self._last_line_length = 0
        if use_color is None:
            self.use_color = _is_color_enabled()
        else:
            self.use_color = use_color
    
    def set_color(self, enabled: bool):
        """Enable or disable color output"""
        self.use_color = enabled
    
    def _get_color_for_level(self, level: int) -> str:
        """Get color code for a log level"""
        if not self.use_color:
            return ""
        
        color_map = {
            -2: Colors.RED,         # Error - red
            -1: Colors.YELLOW,      # Warn - yellow
            0: None, #Colors.BRIGHT_WHITE, # Mesg - bright white (default)
            1: Colors.GREEN,        # Info - green
            2: Colors.CYAN,         # Log - cyan
            3: Colors.BRIGHT_BLACK, # Debug - gray
        }
        return color_map.get(level, "")
    
    def _colorize(self, message: str, level: int) -> str:
        """Apply color to message based on level"""
        if not self.use_color:
            return message
        
        color = self._get_color_for_level(level)
        if color:
            return f"{color}{message}{Colors.RESET}"
        return message
    
    def set_level(self, level: int):
        """Set log level"""
        self.level = level
    
    def _should_log(self, msg_level: int) -> bool:
        """Check if message should be logged based on level
        
        Message is enabled when function log level ==== app log level
        """
        return msg_level <= self.level
    
    def _clear_line(self):
        """Clear the current line by padding with spaces"""
        if self._last_line_length > 0:
            # Write spaces to clear, then CR to return to start of line
            sys.stdout.write(' ' * self._last_line_length + '\r')
            sys.stdout.flush()
            self._last_line_length = 0
    
    def _write(self, message: str, end: str = '\n', level: int = 1):
        """Internal write function"""
        if not self._should_log(level):
            return
        
        # Apply color to message
        colored_message = self._colorize(message, level)
        
        if end == '\r':
            # Clear previous line if it exists
            self._clear_line()
            # Write message
            sys.stdout.write(colored_message)
            sys.stdout.write(end)
            sys.stdout.flush()
            # Calculate length without ANSI codes for clearing
            self._last_line_length = len(message)
        else:
            # If last line ended with \r, just print newline
            if self._last_line_length > 0:
                sys.stdout.write('\n')
                sys.stdout.flush()
                self._last_line_length = 0
            # Write message with newline
            print(colored_message, end=end)
            self._last_line_length = 0
    
    def log_error(self, message: str, level: int = -2):
        """Log error at level -2"""
        self._write(message, '\n', level)
    
    def log_warn(self, message: str, level: int = -1):
        """Log warning at level -1"""
        self._write(message, '\n', level)
    
    def log_mesg(self, message: str, level: int = 0):
        """Log message at level 0"""
        self._write(message, '\n', level)
    
    def log_info(self, message: str, level: int = 1):
        """Log info at level 1"""
        self._write(message, '\n', level)
    
    def log_log(self, message: str, level: int = 2):
        """Log at level 2"""
        self._write(message, '\n', level)
    
    def log_debug(self, message: str, level: int = 3):
        """Log debug at level 3"""
        self._write(message, '\n', level)
    
    def log_error_ecr(self, message: str, level: int = -2):
        """Log error with CR at level -2"""
        if level == self.level:
            self._write(message, '\r', level)
        else:
            self.log_error(message, level)
    
    def log_warn_ecr(self, message: str, level: int = -1):
        """Log warning with CR at level -1"""
        if level == self.level:
            self._write(message, '\r', level)
        else:
            self.log_warn(message, level)
    
    def log_mesg_ecr(self, message: str, level: int = 0):
        """Log message with CR (carriage return) at level 0"""
        if level == self.level:
            self._write(message, '\r', level)
        else:
            self.log_mesg(message, level)
    
    def log_info_ecr(self, message: str, level: int = 1):
        """Log info with CR at level 1"""
        if level == self.level:
            self._write(message, '\r', level)
        else:
            self.log_info(message, level)
    
    def log_log_ecr(self, message: str, level: int = 2):
        """Log with CR at level 2"""
        if level == self.level:
            self._write(message, '\r', level)
        else:
            self.log_log(message, level)
    
    def log_debug_ecr(self, message: str, level: int = 3):
        """Log debug with CR at level 3"""
        if level == self.level:
            self._write(message, '\r', level)
        else:
            self.log_debug(message, level)


# Global logger instance
_logger: Optional[Logger] = None


def init_logger(level: int = 1, use_color: Optional[bool] = None):
    """Initialize global logger
    
    Args:
        level: Log level (default: 1)
        use_color: Enable color output (default: auto-detect from TTY)
    """
    global _logger
    _logger = Logger(level, use_color)


def get_logger() -> Logger:
    """Get global logger instance"""
    global _logger
    if _logger is None:
        _logger = Logger(1)
    return _logger


# Convenience functions
def log_mesg(message: str):
    get_logger().log_mesg(message, 0)

def log_info(message: str):
    get_logger().log_info(message, 1)

def log_warn(message: str):
    get_logger().log_warn(message, -1)

def log_error(message: str):
    get_logger().log_error(message, -2)

def log_log(message: str):
    get_logger().log_log(message, 2)

def log_debug(message: str):
    get_logger().log_debug(message, 3)

def log_mesg_ecr(message: str):
    get_logger().log_mesg_ecr(message, 0)

def log_info_ecr(message: str):
    get_logger().log_info_ecr(message, 1)

def log_warn_ecr(message: str):
    get_logger().log_warn_ecr(message, -1)

def log_error_ecr(message: str):
    get_logger().log_error_ecr(message, -2)

def log_log_ecr(message: str):
    get_logger().log_log_ecr(message, 2)

def log_debug_ecr(message: str):
    get_logger().log_debug_ecr(message, 3)

