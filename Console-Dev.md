# Console Application Development Guide

**Author:** Lenik (patterntest@bodz.net)  
**License:** GPL  
**Date:** 2026

This guide describes best practices for developing console applications with logging, color support, and multi-format output capabilities, based on the patterns used in the patterntest project.

## Table of Contents

1. [Logging Framework](#logging-framework)
2. [Color Support](#color-support)
3. [Multi-Format Output](#multi-format-output)
4. [Command-Line Interface](#command-line-interface)
5. [Best Practices](#best-practices)
6. [Example Implementation](#example-implementation)

## Logging Framework

### Overview

A well-designed logging framework is essential for console applications. It should provide:

- **Level-based filtering**: Control verbosity with numeric levels
- **Color coding**: Visual distinction between message types
- **CR-based progress**: Overwrite lines for progress indicators
- **TTY detection**: Automatically disable colors when not appropriate

### Log Levels

Use a numeric level system for flexibility:

```python
# Level hierarchy (lower = more important)
-2: Error    # Always shown, red
-1: Warning  # Yellow
 0: Message  # Default, no color
 1: Info     # Green (default level)
 2: Log      # Cyan (verbose)
 3: Debug    # Gray (very verbose)
```

### Implementation Pattern

```python
class Logger:
    def __init__(self, level: int = 1, use_color: Optional[bool] = None):
        self.level = level
        self._last_line_length = 0
        if use_color is None:
            self.use_color = _is_color_enabled()  # Auto-detect
        else:
            self.use_color = use_color
    
    def _should_log(self, msg_level: int) -> bool:
        """Message shown when msg_level <= logger.level"""
        return msg_level <= self.level
    
    def log_error(self, message: str, level: int = -2):
        """Always shown, colored red"""
        if self._should_log(level):
            self._write(message, '\n', level)
    
    def log_info_ecr(self, message: str, level: int = 1):
        """CR-based: uses \r only when level matches exactly"""
        if level == self.level:
            self._write(message, '\r', level)
        else:
            self.log_info(message, level)
```

### Key Features

1. **Level-based filtering**: Messages with level <= logger level are shown
2. **CR functions**: Use `\r` for progress when levels match exactly
3. **Color mapping**: Each level has an associated color
4. **TTY detection**: Automatically disable colors for non-terminals

### Usage Example

```python
from logger import init_logger, log_mesg_ecr, log_info, log_error

# Initialize with level 0 (quiet mode)
init_logger(level=0, use_color=True)

# Progress indicator (uses \r)
log_mesg_ecr("[1/10] Processing...")
sys.stdout.flush()

# Info won't show (level 1 > 0)
log_info("  Details...")

# Error always shows
log_error("Something went wrong")
```

## Color Support

### ANSI Color Codes

Use standard ANSI escape sequences for portability:

```python
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    CYAN = '\033[36m'
    # ... more colors
```

### Color Detection

Respect user preferences and environment:

```python
def _is_color_enabled() -> bool:
    # Check NO_COLOR environment variable
    if os.environ.get('NO_COLOR'):
        return False
    # Check if stdout is a TTY
    return sys.stdout.isatty()
```

### Color Application

Apply colors consistently by level:

```python
def _colorize(self, message: str, level: int) -> str:
    if not self.use_color:
        return message
    
    color = self._get_color_for_level(level)
    if color:
        return f"{color}{message}{Colors.RESET}"
    return message
```

### Color Best Practices

1. **Always reset**: Use `Colors.RESET` after colored text
2. **Respect NO_COLOR**: Check environment variable
3. **TTY detection**: Only use colors for terminals
4. **Consistent mapping**: Use same colors for same message types
5. **Don't rely on color**: Ensure messages are readable without color

## Multi-Format Output

### Design Pattern

Separate format generation from data processing:

```python
# Dispatcher pattern
def generate_report(data, format_type='text', output_file=None, use_color=False):
    if format_type == 'html':
        return generate_html_report(data, output_file)
    elif format_type == 'text':
        return generate_text_report(data, output_file, use_color)
    # ... more formats
```

### Format Detection

Auto-detect format from file extension:

```python
def detect_format_from_extension(filename: str) -> str:
    if not filename:
        return 'text'  # Default for stdout
    
    ext = os.path.splitext(filename)[1].lower()
    format_map = {
        '.html': 'html',
        '.pdf': 'pdf',
        '.csv': 'csv',
        '.md': 'markdown',
        '.txt': 'text',
    }
    return format_map.get(ext, 'text')
```

### Format-Specific Considerations

#### Text Format

- **Brief for stdout**: Show summary table only
- **Detailed for files**: Include full details
- **Color support**: Use ANSI codes when appropriate
- **Table formatting**: Dynamic column widths from data

```python
def generate_text_report(data, output_file=None, use_color=False):
    # ... generate report ...
    
    if output_file:
        # Detailed version with all information
        # Remove ANSI codes for file
    else:
        # Brief version - table only
        # Keep ANSI codes for terminal
```

#### HTML Format

- **Interactive elements**: Expandable rows, hover effects
- **CSS styling**: Professional appearance
- **Escape HTML**: Prevent XSS issues
- **Responsive design**: Works on different screen sizes

#### CSV Format

- **Machine-readable**: Simple, parseable format
- **No formatting**: Raw data only
- **Consistent columns**: Same structure across all rows

#### LaTeX/PDF Format

- **Professional documents**: Suitable for reports
- **Escape special chars**: LaTeX has many special characters
- **Page breaks**: Handle long content appropriately

### Output Strategy

```python
# In main application
if args.output:
    format_type = detect_format_from_extension(args.output)
    use_color = False  # Usually disable for files
else:
    format_type = 'text'  # Default for stdout
    use_color = True  # Enable for terminal

generate_report(data, format_type, args.output, use_color)
```

## Command-Line Interface

### Argument Parsing

Use argparse with good defaults:

```python
parser = argparse.ArgumentParser(
    description='Application description',
    formatter_class=argparse.RawDescriptionHelpFormatter
)

# Verbosity control
parser.add_argument(
    '-v', '--verbose',
    action='count',
    default=0,
    help='Increase verbosity (-v, -vv, -vvv)'
)
parser.add_argument(
    '-q', '--quiet',
    action='count',
    default=0,
    help='Decrease verbosity (-q, -qq)'
)

# Color control
parser.add_argument(
    '--color',
    action='store_true',
    default=None,
    help='Enable colors (default: auto-detect)'
)
parser.add_argument(
    '--no-color',
    action='store_false',
    dest='color',
    help='Disable colors'
)

# Format selection
parser.add_argument(
    '--html', '--latex', '--csv',  # etc.
    action='store_const',
    const='html',  # or 'latex', 'csv', etc.
    dest='format',
    help='Generate HTML report'
)
parser.add_argument(
    '-o', '--output',
    help='Output file (format auto-detected from extension)'
)
```

### Level Calculation

```python
# Default level is 1 (info)
# -v increases: 1 -> 2 -> 3
# -q decreases: 1 -> 0 -> -1 -> -2
log_level = 1 + args.verbose - args.quiet
log_level = max(-2, min(3, log_level))  # Clamp to valid range

init_logger(log_level, use_color=args.color)
```

### Format Selection Logic

```python
# Priority: explicit format > file extension > default
if args.format:
    format_type = args.format
elif args.output:
    format_type = detect_format_from_extension(args.output)
else:
    format_type = 'text'  # Default for stdout

# Color: enable for text format on terminal
use_color = args.color and format_type == 'text'
if not args.output and format_type == 'text':
    use_color = True  # Default to color for stdout
```

## Best Practices

### 1. Logging

- **Use appropriate levels**: Don't use error for warnings
- **Progress indicators**: Use CR functions for updates
- **Level matching**: CR functions only work when levels match exactly
- **Flush output**: Use `sys.stdout.flush()` after CR functions if needed

### 2. Colors

- **Auto-detect by default**: Let users override with flags
- **Respect environment**: Check `NO_COLOR` and TTY
- **Consistent mapping**: Same colors for same message types
- **Accessibility**: Don't rely solely on color for information

### 3. Output Formats

- **Brief for stdout**: Don't overwhelm terminal output
- **Detailed for files**: Include all information in saved reports
- **Format detection**: Auto-detect from file extension
- **Color in files**: Usually strip ANSI codes for file output

### 4. Error Handling

- **Abnormal exits**: Catch and report subprocess failures
- **Timeout handling**: Set reasonable timeouts for external commands
- **Error messages**: Provide clear, actionable error messages
- **Exit codes**: Use appropriate exit codes (0=success, non-zero=error)

### 5. User Experience

- **Progress feedback**: Show progress for long operations
- **Verbosity control**: Multiple levels for different use cases
- **Default behavior**: Sensible defaults that work for most users
- **Help text**: Clear, comprehensive help messages

## Example Implementation

### Complete Example

```python
#!/usr/bin/env python3
"""Example console application"""

import sys
import argparse
from logger import init_logger, log_mesg_ecr, log_info, log_error, log_warn
from formats import generate_text_report, generate_html_report

def process_data(input_file):
    """Process data and return results"""
    results = []
    # ... processing logic ...
    return results

def main():
    parser = argparse.ArgumentParser(description='Example console app')
    parser.add_argument('input', help='Input file')
    parser.add_argument('-o', '--output', help='Output file')
    parser.add_argument('--html', action='store_const', const='html', dest='format')
    parser.add_argument('--color', action='store_true', default=None)
    parser.add_argument('--no-color', action='store_false', dest='color')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.add_argument('-q', '--quiet', action='count', default=0)
    
    args = parser.parse_args()
    
    # Calculate log level
    log_level = 1 + args.verbose - args.quiet
    log_level = max(-2, min(3, log_level))
    
    # Initialize logger
    init_logger(log_level, use_color=args.color)
    
    # Determine format
    format_type = args.format or ('html' if args.output and args.output.endswith('.html') else 'text')
    use_color = args.color if args.color is not None else (format_type == 'text' and not args.output)
    
    try:
        # Process with progress
        log_mesg_ecr("[1/3] Reading input...")
        sys.stdout.flush()
        data = read_input(args.input)
        
        log_mesg_ecr("[2/3] Processing...")
        sys.stdout.flush()
        results = process_data(data)
        
        log_mesg_ecr("[3/3] Generating report...")
        sys.stdout.flush()
        
        # Generate report
        if format_type == 'html':
            generate_html_report(results, args.output)
        else:
            generate_text_report(results, args.output, use_color)
        
        log_info("Complete!")
        
    except Exception as e:
        log_error(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
```

### Key Patterns

1. **Level calculation**: `1 + verbose - quiet`, clamped to valid range
2. **Format detection**: Explicit > extension > default
3. **Color logic**: Enable for text format on terminal
4. **Progress updates**: Use CR functions with flush
5. **Error handling**: Catch exceptions, log errors, exit with code

## Summary

A well-designed console application should:

1. **Provide flexible logging** with multiple verbosity levels
2. **Support colors** with automatic detection and user override
3. **Offer multiple output formats** with auto-detection
4. **Show progress** for long-running operations
5. **Handle errors gracefully** with clear messages
6. **Respect user preferences** (NO_COLOR, TTY detection)
7. **Provide sensible defaults** that work for most users

Following these patterns will create console applications that are user-friendly, professional, and maintainable.

---

**Author:** Lenik (patterntest@bodz.net)  
**License:** GPL  
**Date:** 2026

