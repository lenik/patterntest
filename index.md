# Pattern Test - Documentation Index

## Overview

Pattern Test is a comprehensive testing framework for validating pattern matching behavior across different command-line tools (tar, rsync, find, glob).

## Project Structure

```
patterntest/
├── ptlib/                    # Main library package
│   ├── __init__.py          # Package initialization
│   ├── main.py              # CLI entry point
│   ├── models.py            # Data models (TestCase, TestResult, TestMode)
│   ├── tester.py            # PatternTester class
│   ├── report.py            # Report generation dispatcher
│   ├── utils.py             # Utility functions (dir creation, file listing)
│   ├── formats/             # Report format generators
│   │   ├── text.py         # Text/ASCII table format
│   │   ├── html.py         # HTML interactive format
│   │   ├── latex.py        # LaTeX format
│   │   ├── pdf.py          # PDF format (via LaTeX)
│   │   ├── csv.py          # CSV format
│   │   └── markdown.py     # Markdown format
│   ├── modes/              # Tool-specific test implementations
│   │   ├── base.py         # BaseMode abstract class
│   │   ├── tar.py          # Tar pattern testing
│   │   ├── rsync.py        # Rsync pattern testing
│   │   ├── find.py         # Find pattern testing
│   │   └── glob.py         # Python glob testing
│   └── patterns/           # Test case definitions
│       ├── wildcards.py    # Wildcard patterns (*, ?)
│       ├── charset.py      # Character set patterns ([a-z], [^abc])
│       ├── extglob.py      # Extended glob patterns
│       ├── path.py         # Path patterns (**, subdirs)
│       └── regex.py        # Regex patterns
├── logger.py               # Logging framework
├── dirunpack               # Directory unpacking tool
├── patterntest             # Main executable script
├── example.dir             # Test directory structure definition
├── README.md               # User documentation
├── LOGGING.md              # Logging framework manual
└── Makefile                # Build and installation

```

## Key Components

### 1. Pattern Tester (`ptlib/tester.py`)

The `PatternTester` class orchestrates test execution:

- Creates test directory structure from `.dir` file
- Runs tests for each test case
- Compares matched files with expected files
- Determines success/partial/failure status
- Logs unmatched files

### 2. Test Modes (`ptlib/modes/`)

Each mode implements `BaseMode` interface:

- **TarMode**: Tests tar's `--exclude` patterns
- **RsyncMode**: Tests rsync's `--include`/`--exclude` patterns
- **FindMode**: Tests find's `-name`/`-path` patterns
- **GlobMode**: Tests Python's fnmatch patterns

### 3. Test Cases (`ptlib/patterns/`)

Test cases are organized by pattern type:

- **Wildcards**: Basic glob patterns
- **Character Sets**: Character class patterns
- **Extended Globs**: Advanced glob patterns
- **Path Patterns**: Directory and path matching
- **Regex**: Regular expression patterns

### 4. Report Formats (`ptlib/formats/`)

Multiple output formats:

- **Text**: Brief table (stdout) or detailed (file)
- **HTML**: Interactive with expandable rows
- **LaTeX/PDF**: Professional documents
- **CSV**: Machine-readable
- **Markdown**: Documentation-friendly

## Data Flow

1. **CLI Parsing** (`ptlib/main.py`)
   - Parse arguments
   - Initialize logger
   - Filter test cases if `-t/--test` specified

2. **Test Execution** (`ptlib/tester.py`)
   - Create test directory from `example.dir`
   - For each test case:
     - Call mode-specific `test_pattern()`
     - Compare results with expected files
     - Determine success/partial/failure
     - Log results

3. **Report Generation** (`ptlib/report.py`)
   - Collect all test results
   - Generate report in requested format
   - Output to file or stdout

## Pattern Matching Behavior

### Tar

- Supports `--exclude` patterns
- No native `--include` (uses fnmatch filtering)
- Patterns match against full paths or basenames

### Rsync

- Supports `--include` and `--exclude` patterns
- Patterns are path-based, not basename-based
- For basename patterns like `*.txt`, need `--include='*/'` first
- Supports globstar `**` in rsync 3.x

### Find

- Uses `-name` for basename matching
- Uses `-path` for full path matching
- No support for extended globs or regex (without `-regex`)

### Glob

- Python's fnmatch patterns
- Supports basic wildcards and character sets
- No support for extended globs or regex

## Status Determination

- **OK**: Matched files exactly equal expected files
- **..**: Some files matched (subset of expected)
- **(blank)**: No match or error occurred

## Logging Levels

- **-2**: Error (always shown)
- **-1**: Warning
- **0**: Message
- **1**: Info (default)
- **2**: Log
- **3**: Debug

CR-based functions (`*_ecr`) use `\r` only when message level exactly matches logger level.

## Installation

### Standard Installation

```bash
make install PREFIX=/usr/local
```

### Development Installation

```bash
make install-debug
```

Creates symlinks in `/usr` pointing to project directory (doesn't respect DESTDIR/PREFIX).

## Testing Workflow

1. Define test directory structure in `example.dir`
2. Define test cases in `ptlib/patterns/*.py`
3. Run tests: `patterntest /bin/tar`
4. Review results in chosen format
5. Fix expected files or mode implementations as needed

## Extension Points

### Adding New Test Cases

Add to appropriate file in `ptlib/patterns/`:

```python
TestCase(
    "test_name",
    "pattern",
    "Description",
    ["expected", "files"],
    "pattern_type"
)
```

### Adding New Report Format

1. Create `ptlib/formats/newformat.py`
2. Implement `generate_newformat_report()` function
3. Add to `ptlib/formats/__init__.py`
4. Add to `ptlib/report.py` dispatcher

### Adding New Test Mode

1. Create `ptlib/modes/newmode.py`
2. Inherit from `BaseMode`
3. Implement `test_pattern()` method
4. Add to `ptlib/modes/__init__.py`
5. Add to `ptlib/tester.py` mode factory

## Common Issues

1. **Expected file counts wrong**: Check actual files in test directory, update expected lists
2. **Rsync only matches root files**: Need `--include='*/'` for recursive basename patterns
3. **Patterns not supported**: Some tools don't support extended globs or regex
4. **Path mismatches**: Ensure paths are relative to test directory root

