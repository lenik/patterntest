"""Report generation dispatcher"""

from typing import List, Optional
from .models import TestResult
from .formats import (
    generate_html_report,
    generate_latex_report,
    generate_pdf_report,
    generate_csv_report,
    generate_text_report,
    generate_markdown_report,
)


def generate_report(results: List[TestResult], program_path: str, mode: str,
                   output_file: Optional[str] = None, format_type: str = 'text',
                   use_color: bool = False):
    """Generate test report in specified format
    
    Args:
        results: List of test results
        program_path: Path to the program being tested
        mode: Test mode
        output_file: Output file path (optional)
        format_type: Report format ('html', 'latex', 'pdf', 'csv', 'text', 'markdown')
        use_color: Enable ANSI color codes for text format
    """
    if format_type == 'html':
        generate_html_report(results, program_path, mode, output_file)
    elif format_type == 'latex':
        generate_latex_report(results, program_path, mode, output_file)
    elif format_type == 'pdf':
        generate_pdf_report(results, program_path, mode, output_file)
    elif format_type == 'csv':
        generate_csv_report(results, program_path, mode, output_file)
    elif format_type == 'text':
        generate_text_report(results, program_path, mode, output_file, use_color)
    elif format_type == 'markdown':
        generate_markdown_report(results, program_path, mode, output_file)
    else:
        raise ValueError(f"Unknown format: {format_type}")
