# Pattern Test

A comprehensive testing tool for include/exclude patterns used by various command-line tools like tar, rsync, find, and glob.

## Description

Pattern Test helps you verify how different tools handle pattern matching syntaxes including wildcards, regex, extended globs, character sets, and path patterns. It tests tools like tar, rsync, find, and compares their pattern matching capabilities.

## Features

- Test pattern matching for multiple tools (tar, rsync, find, glob)
- Support for various pattern types:
  - Wildcards (`*`, `?`)
  - Character sets (`[a-z]`, `[^abc]`, `[[:alnum:]]`)
  - Extended globs (`?(...)`, `*(...)`, `+(...)`, `@(...)`, `!(...)`)
  - Path patterns (`**/*.txt`, `some subdir/*`)
  - Regex patterns (`file\.txt`, `\d+`, etc.)
- Multiple output formats: text, HTML, LaTeX, PDF, CSV, Markdown
- Detailed test reports with expected vs actual matches
- Color-coded output for easy reading
- Test filtering by name or index

## Installation

### From Source

```bash
make install
```

Or with custom prefix:

```bash
make install PREFIX=/usr/local
```

For development (symlinks to project directory):

```bash
make install-debug
```

### Dependencies

- Python 3.6+
- tar, rsync, find (for testing those tools)
- LaTeX (optional, for PDF generation)

## Usage

### Basic Usage

```bash
patterntest /bin/tar
patterntest /usr/bin/rsync
patterntest /usr/bin/find
```

### Options

```
positional arguments:
  program               Path to the program to test

optional arguments:
  -h, --help            show this help message and exit
  -m, --mode MODE       Test mode: tar, rsync, find, glob
  -e, --example-dir DIR Path to example.dir file (default: example.dir)
  -o, --output FILE     Output file for report
  -t, --test NAMES      Specify which tests to include (name or index, comma-separated)
  --html                Generate HTML report
  --latex               Generate LaTeX report
  --pdf                 Generate PDF report
  --csv                 Generate CSV report
  --text                Generate text report (default for stdout)
  --markdown            Generate Markdown report
  --color               Enable ANSI color codes
  --no-color            Disable ANSI color codes
  -v, --verbose         Increase verbosity (-v, -vv, -vvv)
  -q, --quiet           Decrease verbosity (-q, -qq)
  --keep-temp           Keep temporary directories after testing
```

### Examples

Test tar with specific test cases:

```bash
patterntest /bin/tar -t 1,3,match_txt_extension
```

Generate HTML report:

```bash
patterntest /usr/bin/rsync --html -o report.html
```

Test with verbose output:

```bash
patterntest /usr/bin/find -vv
```

## Test Structure

Tests are organized by pattern type:

- **Wildcards**: Basic `*` and `?` patterns
- **Character Sets**: `[a-z]`, `[^abc]`, character classes
- **Extended Globs**: `?(...)`, `*(...)`, `+(...)`, `@(...)`, `!(...)`
- **Path Patterns**: Directory matching, globstar `**`, anchors
- **Regex**: Regular expression patterns

## Report Formats

- **Text**: Human-readable table format (default for stdout)
- **HTML**: Interactive HTML report with expandable details
- **LaTeX/PDF**: Professional document format
- **CSV**: Machine-readable format
- **Markdown**: Markdown-formatted report

## Status Indicators

- **OK**: Test passed (matched files exactly match expected)
- **..**: Partial success (some files matched but not all expected)
- **(blank)**: Test failed (no match or error)

## Tools

### dirunpack

Unpack `.dir` files to actual directory structure:

```bash
./dirunpack example.dir -o output_dir
```

Creates directory structure with 0-sized files as specified in the `.dir` file.

## Development

### Project Structure

```
patterntest/
├── ptlib/           # Main library
│   ├── formats/     # Report format generators
│   ├── modes/      # Tool-specific test modes
│   └── patterns/   # Test case definitions
├── logger.py        # Logging framework
├── dirunpack        # Directory unpacking tool
└── example.dir      # Test directory structure definition
```

### Running Tests

```bash
# Test all patterns
patterntest /bin/tar

# Test specific pattern
patterntest /bin/tar -t match_txt_extension
```

## License

GPL

## Author

Lenik (patterntest@bodz.net) - 2026

