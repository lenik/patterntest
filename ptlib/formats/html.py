"""HTML report format"""

from typing import List, Optional
from ..models import TestResult
from logger import log_info


def escape_html(text: str) -> str:
    """Escape HTML special characters"""
    return (text.replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;')
                .replace("'", '&#39;'))


def generate_html_report(results: List[TestResult], program_path: str, mode: str,
                         output_file: Optional[str] = None) -> str:
    """Generate HTML report with table and expand/collapse"""
    successful = sum(1 for r in results if r.success)
    failed = len(results) - successful
    
    html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Pattern Test Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            border-bottom: 3px solid #4CAF50;
            padding-bottom: 10px;
        }}
        .summary {{
            background-color: #f9f9f9;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 10px;
        }}
        .summary-item {{
            margin: 5px 0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background-color: white;
        }}
        thead {{
            background-color: #4CAF50;
            color: white;
        }}
        th {{
            padding: 12px;
            text-align: left;
            font-weight: bold;
            border-bottom: 2px solid #45a049;
        }}
        tbody tr {{
            border-bottom: 1px solid #ddd;
            cursor: pointer;
            transition: background-color 0.2s;
        }}
        tbody tr:hover {{
            background-color: #f5f5f5;
        }}
        tbody tr.expanded {{
            background-color: #f9f9f9;
        }}
        td {{
            padding: 10px 12px;
            vertical-align: top;
        }}
        .status {{
            display: inline-block;
            padding: 4px 10px;
            border-radius: 4px;
            font-weight: bold;
            font-size: 0.85em;
        }}
        .status.success {{
            background-color: #4CAF50;
            color: white;
        }}
        .status.warning {{
            background-color: #FFC107;
            color: black;
        }}
        .status.failed {{
            background-color: #f44336;
            color: white;
        }}
        .pattern {{
            font-family: monospace;
            background-color: #e8e8e8;
            padding: 3px 8px;
            border-radius: 3px;
            font-size: 0.9em;
        }}
        .expand-icon {{
            display: inline-block;
            width: 16px;
            text-align: center;
            font-weight: bold;
            margin-right: 5px;
        }}
        .detail-panel {{
            display: none;
            padding: 15px;
            background-color: #fafafa;
            border-top: 2px solid #ddd;
        }}
        .detail-panel.expanded {{
            display: block;
        }}
        .detail-section {{
            margin: 10px 0;
        }}
        .detail-label {{
            font-weight: bold;
            color: #555;
            margin-right: 10px;
        }}
        .error {{
            color: #f44336;
            font-weight: bold;
            font-family: monospace;
            background-color: #ffebee;
            padding: 8px;
            border-radius: 4px;
            margin-top: 5px;
        }}
        .file-list {{
            font-family: monospace;
            background-color: #f0f0f0;
            padding: 10px;
            border-radius: 4px;
            max-height: 300px;
            overflow-y: auto;
            margin-top: 5px;
        }}
        .file-item {{
            padding: 3px 0;
            border-bottom: 1px solid #e0e0e0;
        }}
        .file-item:last-child {{
            border-bottom: none;
        }}
        .type-badge {{
            display: inline-block;
            padding: 2px 8px;
            border-radius: 3px;
            font-size: 0.8em;
            background-color: #2196F3;
            color: white;
        }}
    </style>
    <script>
        function toggleRow(rowId) {{
            var row = document.getElementById('row-' + rowId);
            var panel = document.getElementById('panel-' + rowId);
            var icon = document.getElementById('icon-' + rowId);
            
            if (panel.classList.contains('expanded')) {{
                panel.classList.remove('expanded');
                row.classList.remove('expanded');
                icon.textContent = '+';
            }} else {{
                panel.classList.add('expanded');
                row.classList.add('expanded');
                icon.textContent = '−';
            }}
        }}
    </script>
</head>
<body>
    <div class="container">
        <h1>Pattern Test Report</h1>
        <div class="summary">
            <div class="summary-item"><strong>Tool:</strong> {program_path}</div>
            <div class="summary-item"><strong>Mode:</strong> {mode}</div>
            <div class="summary-item"><strong>Total tests:</strong> {total}</div>
            <div class="summary-item"><strong>Successful:</strong> <span class="status success">{successful}</span></div>
            <div class="summary-item"><strong>Failed:</strong> <span class="status failed">{failed}</span></div>
        </div>
        <table>
            <thead>
                <tr>
                    <th style="width: 30px;"></th>
                    <th style="width: 200px;">Test Name</th>
                    <th style="width: 250px;">Pattern</th>
                    <th style="width: 100px;">Type</th>
                    <th style="width: 80px;">Status</th>
                    <th style="width: 100px;">Matches</th>
                    <th style="width: 80px;">Expect</th>
                    <th>Description</th>
                </tr>
            </thead>
            <tbody>
""".format(
        program_path=escape_html(program_path),
        mode=escape_html(mode),
        total=len(results),
        successful=successful,
        failed=failed
    )
    
    for i, result in enumerate(results):
        if result.success:
            status_class = "success"
            status_text = "OK"
        elif result.partial:
            status_class = "warning"
            status_text = ".."
        else:
            status_class = "failed"
            status_text = ""  # Blank for NO
        match_count = len(result.matched_files) if not result.error else 0
        expect_count = len(result.test_case.expected_files)
        
        html += f"""
                <tr id="row-{i}" onclick="toggleRow({i})">
                    <td><span id="icon-{i}" class="expand-icon">+</span></td>
                    <td><strong>{escape_html(result.test_case.name)}</strong></td>
                    <td><span class="pattern">{escape_html(result.test_case.pattern)}</span></td>
                    <td><span class="type-badge">{escape_html(result.test_case.pattern_type)}</span></td>
                    <td><span class="status {status_class}">{status_text}</span></td>
                    <td>{match_count}</td>
                    <td>{expect_count}</td>
                    <td>{escape_html(result.test_case.description)}</td>
                </tr>
                <tr>
                    <td colspan="8" class="detail-panel" id="panel-{i}">
                        <div class="detail-section">
                            <span class="detail-label">Test Name:</span>
                            {escape_html(result.test_case.name)}
                        </div>
                        <div class="detail-section">
                            <span class="detail-label">Pattern:</span>
                            <span class="pattern">{escape_html(result.test_case.pattern)}</span>
                        </div>
                        <div class="detail-section">
                            <span class="detail-label">Type:</span>
                            <span class="type-badge">{escape_html(result.test_case.pattern_type)}</span>
                        </div>
                        <div class="detail-section">
                            <span class="detail-label">Description:</span>
                            {escape_html(result.test_case.description)}
                        </div>
                        <div class="detail-section">
                            <span class="detail-label">Status:</span>
                            <span class="status {status_class}">{status_text}</span>
                        </div>
"""
        
        if result.error:
            html += f"""
                        <div class="detail-section">
                            <span class="detail-label">Error:</span>
                            <div class="error">{escape_html(result.error)}</div>
                        </div>
"""
        else:
            html += f"""
                        <div class="detail-section">
                            <span class="detail-label">Matched Files ({len(result.matched_files)}):</span>
"""
            if result.matched_files:
                html += '                            <div class="file-list">\n'
                for f in result.matched_files:
                    html += f'                                <div class="file-item">{escape_html(f)}</div>\n'
                html += '                            </div>\n'
            else:
                html += '                            <div class="file-list">(no files matched)</div>\n'
        
        html += """                    </div>
                </tr>
"""
    
    html += """            </tbody>
        </table>
    </div>
</body>
</html>
"""
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        log_info(f"HTML report written to {output_file}")
    else:
        print(html)
    
    return html

