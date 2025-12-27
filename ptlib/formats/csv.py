"""CSV report format"""

import csv
from typing import List, Optional
from ..models import TestResult
from logger import log_info


def generate_csv_report(results: List[TestResult], program_path: str, mode: str,
                        output_file: Optional[str] = None) -> str:
    """Generate CSV report"""
    import io
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        'Test Name', 'Pattern', 'Type', 'Description', 'Status', 
        'Match Count', 'Expect', 'Error', 'Matched Files'
    ])
    
    # Write data rows
    for result in results:
        if result.success:
            status = "OK"
        elif result.partial:
            status = ".."
        else:
            status = ""  # Blank for NO
        match_count = len(result.matched_files) if not result.error else 0
        expect_count = len(result.test_case.expected_files)
        error = result.error if result.error else ""
        matched_files = "; ".join(result.matched_files) if result.matched_files else ""
        
        writer.writerow([
            result.test_case.name,
            result.test_case.pattern,
            result.test_case.pattern_type,
            result.test_case.description,
            status,
            match_count,
            expect_count,
            error,
            matched_files
        ])
    
    csv_content = output.getvalue()
    output.close()
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            f.write(csv_content)
        log_info(f"CSV report written to {output_file}")
    else:
        print(csv_content)
    
    return csv_content

