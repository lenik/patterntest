"""Main entry point for pattern testing"""

import os
import sys
import argparse
from .models import TestMode
from .tester import PatternTester
from .patterns import get_all_tests
from .report import generate_report
from logger import init_logger, log_error, log_info, log_warn


def detect_format_from_extension(filename: str) -> str:
    """Detect report format from file extension
    
    Args:
        filename: Output filename
        
    Returns:
        Format type: 'html', 'latex', 'pdf', 'csv', 'text', 'markdown'
    """
    if not filename:
        return 'text'
    
    ext = os.path.splitext(filename)[1].lower()
    
    format_map = {
        '.html': 'html',
        '.htm': 'html',
        '.tex': 'latex',
        '.pdf': 'pdf',
        '.csv': 'csv',
        '.txt': 'text',
        '.md': 'markdown',
        '.markdown': 'markdown',
    }
    
    return format_map.get(ext, 'text')


def main():
    parser = argparse.ArgumentParser(
        description='Test include/exclude patterns for various tools',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        'program',
        help='Path to the program to test (e.g., /bin/tar, /usr/bin/rsync)'
    )
    parser.add_argument(
        '-m', '--mode',
        choices=['tar', 'rsync', 'find', 'glob'],
        help='Test mode (default: auto-detect from program name)'
    )
    parser.add_argument(
        '-e', '--example-dir',
        default='example.dir',
        help='Path to example.dir file (default: example.dir)'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output file for report (default: print to stdout)'
    )
    parser.add_argument(
        '--html',
        action='store_const',
        const='html',
        dest='format',
        help='Generate HTML report'
    )
    parser.add_argument(
        '--latex',
        action='store_const',
        const='latex',
        dest='format',
        help='Generate LaTeX report'
    )
    parser.add_argument(
        '--pdf',
        action='store_const',
        const='pdf',
        dest='format',
        help='Generate PDF report (converted from LaTeX)'
    )
    parser.add_argument(
        '--csv',
        action='store_const',
        const='csv',
        dest='format',
        help='Generate CSV report'
    )
    parser.add_argument(
        '--text',
        action='store_const',
        const='text',
        dest='format',
        help='Generate text report (default for stdout)'
    )
    parser.add_argument(
        '--markdown',
        action='store_const',
        const='markdown',
        dest='format',
        help='Generate Markdown report'
    )
    parser.add_argument(
        '--color',
        action='store_true',
        default=None,
        help='Enable ANSI color codes (default: auto-detect from TTY)'
    )
    parser.add_argument(
        '--no-color',
        action='store_false',
        dest='color',
        help='Disable ANSI color codes'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='count',
        default=0,
        help='Increase verbosity (can be used multiple times: -v, -vv, -vvv)'
    )
    parser.add_argument(
        '-q', '--quiet',
        action='count',
        default=0,
        help='Decrease verbosity (can be used multiple times: -q, -qq)'
    )
    parser.add_argument(
        '--keep-temp',
        action='store_true',
        help='Keep temporary directories after testing'
    )
    parser.add_argument(
        '-t', '--test',
        help='Specify which tests to include. NAME can be test case name or index number, multiple separated by comma'
    )
    
    args = parser.parse_args()
    
    # Determine log level
    # Default is 1 (info)
    # -v increases: 1 -> 2 -> 3
    # -q decreases: 1 -> 0 -> -1 -> -2
    log_level = 1 + args.verbose - args.quiet
    # Clamp to valid range
    log_level = max(-2, min(3, log_level))
    
    # Initialize logger with color support
    # --color enables, --no-color disables, default is auto-detect
    init_logger(log_level, use_color=args.color)
    
    # Determine format
    # If format is explicitly specified, use it
    # Otherwise, guess from output file extension, fallback to text for stdout
    if args.format:
        format_type = args.format
    elif args.output:
        format_type = detect_format_from_extension(args.output)
    else:
        format_type = 'text'  # Default when printing to stdout
    
    # Determine mode
    mode = None
    if args.mode:
        mode = TestMode(args.mode)
    
    # Create tester
    tester = PatternTester(args.program, mode)
    
    try:
        # Check if example.dir exists
        if not os.path.exists(args.example_dir):
            log_error(f"{args.example_dir} not found")
            sys.exit(1)
        
        # Get all test cases
        all_test_cases = get_all_tests()
        
        # Filter test cases if -t/--test is specified
        if args.test:
            test_names = [name.strip() for name in args.test.split(',')]
            test_cases = []
            for name in test_names:
                # Try as index first
                try:
                    idx = int(name) - 1  # Convert to 0-based index
                    if 0 <= idx < len(all_test_cases):
                        test_cases.append(all_test_cases[idx])
                    else:
                        log_warn(f"Test index {name} out of range (1-{len(all_test_cases)})")
                except ValueError:
                    # Not a number, try as name
                    found = False
                    for test_case in all_test_cases:
                        if test_case.name == name:
                            test_cases.append(test_case)
                            found = True
                            break
                    if not found:
                        log_warn(f"Test case '{name}' not found")
        else:
            test_cases = all_test_cases
        
        if not test_cases:
            log_error("No test cases to run")
            sys.exit(1)
        
        # Run tests
        tester.run_tests(args.example_dir, test_cases)
        
        # Generate report
        # Use color for text format when --color is specified or when outputting to stdout
        use_color = args.color and format_type == 'text'
        if not args.output and format_type == 'text':
            use_color = True  # Default to color for stdout text output
        
        generate_report(tester.results, args.program, tester.mode.value, args.output, format_type, use_color)
        
    except KeyboardInterrupt:
        log_warn("\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        log_error(f"{e}")
        import traceback
        from logger import get_logger
        if get_logger().level >= 3:  # Debug level
            traceback.print_exc()
        sys.exit(1)
    finally:
        if not args.keep_temp:
            tester.cleanup()


if __name__ == '__main__':
    main()

