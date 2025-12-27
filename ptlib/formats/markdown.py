"""Markdown report format"""

from typing import List, Optional
from ..models import TestResult
from logger import log_info


def escape_markdown(text: str) -> str:
    """Escape markdown special characters"""
    # Basic escaping for code blocks
    return text.replace('`', '\\`').replace('*', '\\*').replace('_', '\\_')


def generate_markdown_report(results: List[TestResult], program_path: str, mode: str,
                            output_file: Optional[str] = None) -> str:
    """Generate Markdown report"""
    successful = sum(1 for r in results if r.success)
    failed = len(results) - successful
    
    lines = []
    
    # Header
    lines.append("# Pattern Test Report")
    lines.append("")
    lines.append(f"**Tool:** {program_path}")
    lines.append(f"**Mode:** {mode}")
    lines.append(f"**Total tests:** {len(results)}")
    lines.append(f"**Successful:** {successful}")
    lines.append(f"**Failed:** {failed}")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Table
    lines.append("## Test Results Summary")
    lines.append("")
    lines.append("| Test Name | Pattern | Type | Status | Matches | Expect | Description |")
    lines.append("|-----------|---------|------|--------|---------|--------|-------------|")
    
    for result in results:
        if result.success:
            status = "✅ OK"
        elif result.partial:
            status = "⚠️ .."
        else:
            status = ""  # Blank for NO
        match_count = len(result.matched_files) if not result.error else 0
        expect_count = len(result.test_case.expected_files)
        
        # Escape markdown in table cells
        name = escape_markdown(result.test_case.name)
        pattern = f"`{escape_markdown(result.test_case.pattern)}`"
        pattern_type = escape_markdown(result.test_case.pattern_type)
        desc = escape_markdown(result.test_case.description)
        
        lines.append(f"| {name} | {pattern} | {pattern_type} | {status} | {match_count} | {expect_count} | {desc} |")
    
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Detailed results
    lines.append("## Detailed Results")
    lines.append("")
    
    for i, result in enumerate(results, 1):
        if result.success:
            status = "✅ OK"
        elif result.partial:
            status = "⚠️ .."
        else:
            status = ""  # Blank for NO
        
        lines.append(f"### Test {i}: {escape_markdown(result.test_case.name)}")
        lines.append("")
        lines.append(f"- **Status:** {status}")
        lines.append(f"- **Pattern:** `{escape_markdown(result.test_case.pattern)}`")
        lines.append(f"- **Type:** {escape_markdown(result.test_case.pattern_type)}")
        lines.append(f"- **Description:** {escape_markdown(result.test_case.description)}")
        
        if result.error:
            lines.append(f"- **Error:** `{escape_markdown(result.error)}`")
        else:
            lines.append(f"- **Matched files:** {len(result.matched_files)}")
            if result.matched_files:
                lines.append("")
                lines.append("  ```")
                for f in result.matched_files:
                    lines.append(f"  {f}")
                lines.append("  ```")
            else:
                lines.append("  _(no files matched)_")
        
        lines.append("")
    
    markdown_content = "\n".join(lines)
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        log_info(f"Markdown report written to {output_file}")
    else:
        print(markdown_content)
    
    return markdown_content

