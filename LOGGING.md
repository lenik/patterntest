# Logging Framework Manual

## Overview

The logging framework provides level-based filtering, color support, and carriage-return (CR) based functions for progress updates.

## Initialization

```python
from logger import init_logger

# Initialize with default settings (level 1, auto-detect color)
init_logger()

# Initialize with specific level and color
init_logger(level=2, use_color=True)

# Initialize with quiet mode
init_logger(level=0, use_color=False)
```

## Log Levels

The logging framework uses numeric levels:

- **-2**: Error (red)
- **-1**: Warning (yellow)
- **0**: Message (default, no color)
- **1**: Info (green) - default level
- **2**: Log (cyan)
- **3**: Debug (gray)

Messages are displayed when the message level is **less than or equal to** the logger level.

### Level Examples

```python
init_logger(level=1)  # Shows: error, warn, mesg, info
init_logger(level=0)  # Shows: error, warn, mesg
init_logger(level=2)  # Shows: error, warn, mesg, info, log
init_logger(level=3)  # Shows: all levels including debug
```

## Basic Logging Functions

```python
from logger import log_error, log_warn, log_mesg, log_info, log_log, log_debug

log_error("Something went wrong")    # Level -2, always shown
log_warn("Warning message")          # Level -1
log_mesg("Important message")        # Level 0
log_info("Informational message")    # Level 1 (default)
log_log("Detailed log")              # Level 2
log_debug("Debug information")       # Level 3
```

## CR-Based Functions (Progress Updates)

Functions ending with `_ecr` use carriage return (`\r`) to overwrite the current line, useful for progress indicators:

```python
from logger import log_mesg_ecr, log_info_ecr

log_mesg_ecr("[1/10] Processing...")  # Overwrites current line
log_info_ecr("  Status: running")     # Overwrites current line
```

**Note**: CR-based functions only use `\r` when the message level **exactly matches** the logger level. Otherwise, they behave like normal logging functions.

### CR Function Behavior

```python
init_logger(level=0)

log_mesg_ecr("[1/5] Test 1")  # Uses \r (level 0 == logger level 0)
log_info_ecr("  Pattern: *")  # Uses \n (level 1 != logger level 0)
```

## Color Support

Colors are automatically enabled if:
- Output is to a TTY (terminal)
- `NO_COLOR` environment variable is not set

You can explicitly control colors:

```python
init_logger(level=1, use_color=True)   # Force enable
init_logger(level=1, use_color=False) # Force disable
```

### Color Codes by Level

- **Error** (-2): Red
- **Warning** (-1): Yellow
- **Message** (0): No color (default)
- **Info** (1): Green
- **Log** (2): Cyan
- **Debug** (3): Gray

## Advanced Usage

### Getting Logger Instance

```python
from logger import get_logger

logger = get_logger()
logger.set_level(2)
logger.set_color(False)
```

### Manual Level Control

```python
logger = get_logger()

# Change level at runtime
logger.set_level(3)  # Enable debug

# Change color at runtime
logger.set_color(True)
```

## Examples

### Progress Indicator

```python
from logger import init_logger, log_mesg_ecr, log_info
import sys

init_logger(level=0, use_color=True)

for i in range(1, 6):
    log_mesg_ecr(f"[{i}/5] Testing: test_{i}")
    sys.stdout.flush()
    # ... do work ...
    log_info(f"  Pattern: *")  # This won't show at level 0
    sys.stdout.flush()

print()  # Final newline
```

### Verbose Debugging

```python
from logger import init_logger, log_debug, log_info

init_logger(level=3, use_color=True)  # Enable debug

log_info("Starting process")
log_debug("Debug: variable x = 42")
log_debug("Debug: variable y = 100")
```

### Quiet Mode

```python
from logger import init_logger, log_error, log_mesg

init_logger(level=0, use_color=False)  # Quiet mode

log_mesg("Important message")  # Shown
log_info("Info message")       # Not shown (level 1 > 0)
log_error("Error occurred")   # Always shown
```

## Best Practices

1. **Use appropriate levels**: Reserve debug for development, info for normal operation
2. **CR functions for progress**: Use `_ecr` functions for progress indicators that update in place
3. **Level matching for CR**: Remember that CR functions only use `\r` when levels match exactly
4. **Color awareness**: Don't rely on colors for critical information
5. **Flush output**: Use `sys.stdout.flush()` after CR-based functions if needed

## Environment Variables

- `NO_COLOR`: If set, disables color output regardless of TTY detection

## Implementation Details

The logger maintains state about the last line written with `\r` to properly clear it when writing new lines. When a newline is written after a CR line, it simply prints a newline instead of clearing with spaces.

