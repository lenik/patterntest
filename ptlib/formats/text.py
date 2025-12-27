"""Text report format with ANSI color support"""

from typing import List, Optional
from ..models import TestResult
from logger import log_info


# ANSI color codes
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    GREEN = '\033[32m'
    RED = '\033[31m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    CYAN = '\033[36m'
    GRAY = '\033[90m'


def format_table_row(cols, widths, alignments=None, use_color=False):
    """Format a table row with specified alignments
    
    Args:
        cols: List of column values
        widths: List of column widths
        alignments: List of alignment chars ('l'=left, 'r'=right, 'c'=center), defaults to left
        use_color: Whether ANSI codes are used
    """
    import re
    if alignments is None:
        alignments = ['l'] * len(cols)
    
    row = "|"
    for i, (col, width, align) in enumerate(zip(cols, widths, alignments)):
        content = str(col)
        # Remove ANSI codes for length calculation
        if use_color:
            content_no_ansi = re.sub(r'\033\[[0-9;]*m', '', content)
        else:
            content_no_ansi = content
        
        # Extract ANSI codes for proper padding
        ansi_prefix = ""
        ansi_suffix = ""
        if use_color:
            # Extract ANSI codes at the start
            prefix_match = re.match(r'(\033\[[0-9;]*m)+', content)
            if prefix_match:
                ansi_prefix = prefix_match.group(0)
            # Extract ANSI reset code at the end
            suffix_match = re.search(r'\033\[0m$', content)
            if suffix_match:
                ansi_suffix = suffix_match.group(0)
        
        visible_len = len(content_no_ansi)
        target_width = width - 2
        
        if visible_len > target_width:
            # Truncate based on visible length
            trunc_len = target_width - 3  # Leave room for "..."
            if use_color:
                truncated_visible = content_no_ansi[:trunc_len] + "..."
                content = ansi_prefix + truncated_visible + ansi_suffix
            else:
                content = content_no_ansi[:trunc_len] + "..."
            visible_len = len(content_no_ansi[:trunc_len] + "...")
        else:
            # Pad the visible content to target width
            padding_needed = target_width - visible_len
            if align == 'r':  # Right align
                padded_visible = ' ' * padding_needed + content_no_ansi
            elif align == 'c':  # Center align
                left_pad = padding_needed // 2
                right_pad = padding_needed - left_pad
                padded_visible = ' ' * left_pad + content_no_ansi + ' ' * right_pad
            else:  # Left align (default)
                padded_visible = content_no_ansi + ' ' * padding_needed
            
            # Re-apply ANSI codes around padded content
            if use_color:
                content = ansi_prefix + padded_visible + ansi_suffix
            else:
                content = padded_visible
        
        row += f" {content} |"
    return row


def generate_text_report(results: List[TestResult], program_path: str, mode: str,
                        output_file: Optional[str] = None, use_color: bool = False) -> str:
    """Generate text report with table and detailed results"""
    successful = sum(1 for r in results if r.success)
    failed = len(results) - successful
    
    lines = []
    
    # Header
    reset = Colors.RESET if use_color else ""
    bold = Colors.BOLD if use_color else ""
    lines.append(f"{bold}{'='*80}{reset}")
    lines.append(f"{bold}Pattern Test Report{reset}")
    lines.append(f"{bold}{'='*80}{reset}")
    lines.append("")
    lines.append(f"Tool: {program_path}")
    lines.append(f"Mode: {mode}")
    lines.append(f"Total tests: {len(results)}")
    
    if use_color:
        lines.append(f"Successful: {Colors.GREEN}{successful}{reset}")
        lines.append(f"Failed: {Colors.RED}{failed}{reset}")
    else:
        lines.append(f"Successful: {successful}")
        lines.append(f"Failed: {failed}")
    
    lines.append("")
    lines.append("")
    
    # Prepare all data for width calculation
    import re
    header_cols = ["Test Name", "Pattern", "Type", "Status", "Matches", "Expect", "Description"]
    
    # Collect all row data
    row_data = []
    for result in results:
        if result.success:
            status = "OK"
        elif result.partial:
            status = ".."
        else:
            status = ""  # Blank for NO
        match_count = len(result.matched_files) if not result.error else 0
        expect_count = len(result.test_case.expected_files)
        row_data.append([
            result.test_case.name,
            result.test_case.pattern,
            result.test_case.pattern_type,
            status,
            str(match_count),
            str(expect_count),
            result.test_case.description
        ])
    
    # Include headers and all data for width calculation
    all_rows = [header_cols] + row_data
    
    # Calculate column widths from actual data (including headers)
    col_widths = []
    for col_idx in range(len(header_cols)):
        max_width = 0
        for row in all_rows:
            if col_idx < len(row):
                content = str(row[col_idx])
                # Remove ANSI codes for width calculation
                if use_color:
                    content_no_ansi = re.sub(r'\033\[[0-9;]*m', '', content)
                else:
                    content_no_ansi = content
                max_width = max(max_width, len(content_no_ansi))
        # Add padding: 2 spaces + content, minimum width based on header
        col_widths.append(max(max_width + 2, len(header_cols[col_idx]) + 2))
    
    # Define alignments: center for headers, right for numbers, left for others
    header_alignments = ['c', 'c', 'c', 'c', 'c', 'c', 'c']  # All headers centered
    data_alignments = ['l', 'l', 'l', 'l', 'r', 'r', 'l']  # Matches and Expect right-aligned
    
    # Table border - each column section uses 'width' dashes to match row width
    border = "+" + "+".join("-" * w for w in col_widths) + "+"
    lines.append(border)
    lines.append(format_table_row(header_cols, col_widths, header_alignments, use_color))
    lines.append(border)
    
    # Table rows
    for row in row_data:
        status = row[3]
        pattern = row[1]
        
        cols = row.copy()
        
        if use_color:
            # Color the status column
            if status == "OK":
                cols[3] = f"{Colors.GREEN}{status}{reset}"
            elif status == "..":
                cols[3] = f"{Colors.YELLOW}{status}{reset}"
            elif status == "":
                cols[3] = f"{Colors.RED}{status}{reset}"
            else:
                cols[3] = f"{Colors.RED}{status}{reset}"
            # Color the pattern
            cols[1] = f"{Colors.CYAN}{pattern}{reset}"
        
        lines.append(format_table_row(cols, col_widths, data_alignments, use_color))
    
    lines.append(border)
    lines.append("")
    lines.append("")
    
    # Detailed results - only show when output file is specified
    if output_file:
        lines.append(f"{bold}{'='*80}{reset}")
        lines.append(f"{bold}Detailed Results{reset}")
        lines.append(f"{bold}{'='*80}{reset}")
        lines.append("")
        
        for i, result in enumerate(results, 1):
            if result.success:
                status = "OK"
                status_color = Colors.GREEN
            elif result.partial:
                status = ".."
                status_color = Colors.YELLOW
            else:
                status = "NO"
                status_color = Colors.RED
            
            lines.append(f"{bold}Test {i}: {result.test_case.name}{reset}")
            if use_color:
                lines.append(f"  Status: {status_color}{bold}{status}{reset}")
            else:
                lines.append(f"  Status: {status}")
            
            lines.append(f"  Pattern: {result.test_case.pattern}")
            lines.append(f"  Type: {result.test_case.pattern_type}")
            lines.append(f"  Description: {result.test_case.description}")
            
            if result.error:
                if use_color:
                    lines.append(f"  {Colors.RED}Error: {result.error}{reset}")
                else:
                    lines.append(f"  Error: {result.error}")
            else:
                lines.append(f"  Matched files: {len(result.matched_files)}")
                if result.matched_files:
                    for f in result.matched_files:
                        lines.append(f"    - {f}")
                else:
                    lines.append("    (no files matched)")
            
            lines.append("")
    
    text_content = "\n".join(lines)
    
    if output_file:
        # Write without ANSI codes to file
        text_plain = text_content
        if use_color:
            # Remove ANSI codes for file output
            import re
            text_plain = re.sub(r'\033\[[0-9;]*m', '', text_plain)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text_plain)
        log_info(f"Text report written to {output_file}")
    else:
        print(text_content)
    
    return text_content

