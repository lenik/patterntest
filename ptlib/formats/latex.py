"""LaTeX report format"""

from typing import List, Optional
from ..models import TestResult
from logger import log_info


def escape_latex(text: str) -> str:
    """Escape LaTeX special characters"""
    special_chars = {
        '\\': r'\textbackslash{}',
        '{': r'\{',
        '}': r'\}',
        '$': r'\$',
        '&': r'\&',
        '%': r'\%',
        '#': r'\#',
        '^': r'\textasciicircum{}',
        '_': r'\_',
        '~': r'\textasciitilde{}',
    }
    result = text
    for char, replacement in special_chars.items():
        result = result.replace(char, replacement)
    return result


def generate_latex_report(results: List[TestResult], program_path: str, mode: str,
                          output_file: Optional[str] = None) -> str:
    """Generate LaTeX report with table"""
    successful = sum(1 for r in results if r.success)
    failed = len(results) - successful
    
    latex = r"""\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{geometry}
\usepackage{booktabs}
\usepackage{longtable}
\usepackage{xcolor}
\usepackage{array}
\usepackage{listings}
\usepackage{fancyhdr}
\usepackage{hyperref}

\geometry{margin=0.8in}

\definecolor{successcolor}{RGB}{76, 175, 80}
\definecolor{failcolor}{RGB}{244, 67, 54}
\definecolor{warningcolor}{RGB}{255, 193, 7}

\pagestyle{fancy}
\fancyhf{}
\fancyhead[C]{Pattern Test Report}
\fancyfoot[C]{\thepage}

\title{Pattern Test Report}
\author{Lenik (patterntest@bodz.net)}
\date{\today}

\begin{document}
\maketitle

\section*{Summary}
\begin{itemize}
    \item \textbf{Tool:} """ + escape_latex(program_path) + r"""
    \item \textbf{Mode:} """ + escape_latex(mode) + r"""
    \item \textbf{Total tests:} """ + str(len(results)) + r"""
    \item \textbf{Successful:} \textcolor{successcolor}{\textbf{""" + str(successful) + r"""}}
    \item \textbf{Failed:} \textcolor{failcolor}{\textbf{""" + str(failed) + r"""}}
\end{itemize}

\section*{Test Results}

\begin{longtable}{p{0.18\textwidth}p{0.22\textwidth}p{0.08\textwidth}p{0.08\textwidth}p{0.08\textwidth}p{0.08\textwidth}p{0.28\textwidth}}
\toprule
\textbf{Test Name} & \textbf{Pattern} & \textbf{Type} & \textbf{Status} & \textbf{Matches} & \textbf{Expect} & \textbf{Description} \\
\midrule
\endfirsthead
\toprule
\textbf{Test Name} & \textbf{Pattern} & \textbf{Type} & \textbf{Status} & \textbf{Matches} & \textbf{Expect} & \textbf{Description} \\
\midrule
\endhead
\bottomrule
\endfoot
\bottomrule
\endlastfoot
"""
    
    for i, result in enumerate(results, 1):
        if result.success:
            status_color = "successcolor"
            status_text = "OK"
        elif result.partial:
            status_color = "warningcolor"
            status_text = ".."
        else:
            status_color = "failcolor"
            status_text = ""  # Blank for NO
        match_count = len(result.matched_files) if not result.error else 0
        expect_count = len(result.test_case.expected_files)
        
        # Truncate long patterns for table
        pattern = escape_latex(result.test_case.pattern)
        if len(pattern) > 40:
            pattern = pattern[:37] + "..."
        
        latex += f"""
{escape_latex(result.test_case.name)} & \\texttt{{{pattern}}} & {escape_latex(result.test_case.pattern_type)} & \\textcolor{{{status_color}}}{{\\textbf{{{status_text}}}}} & {match_count} & {expect_count} & {escape_latex(result.test_case.description)} \\\\
"""
    
    latex += r"""\end{longtable}

\newpage
\section*{Detailed Results}

"""
    
    for i, result in enumerate(results, 1):
        if result.success:
            status_color = "successcolor"
            status_text = "OK"
        elif result.partial:
            status_color = "warningcolor"
            status_text = ".."
        else:
            status_color = "failcolor"
            status_text = ""  # Blank for NO
        
        latex += f"""
\\subsection*{{Test {i}: {escape_latex(result.test_case.name)}}}
\\textcolor{{{status_color}}}{{\\textbf{{{status_text}}}}}

\\begin{{description}}
    \\item[Pattern:] \\texttt{{{escape_latex(result.test_case.pattern)}}}
    \\item[Type:] {escape_latex(result.test_case.pattern_type)}
    \\item[Description:] {escape_latex(result.test_case.description)}
"""
        
        if result.error:
            latex += f"    \\item[Error:] \\textcolor{{failcolor}}{{{escape_latex(result.error)}}}\n"
        else:
            latex += f"    \\item[Matched files:] {len(result.matched_files)}\n"
            if result.matched_files:
                latex += "    \\begin{itemize}\n"
                for f in result.matched_files[:50]:  # Limit to 50 files
                    latex += f"        \\item \\texttt{{{escape_latex(f)}}}\n"
                if len(result.matched_files) > 50:
                    latex += f"        \\item ... and {len(result.matched_files) - 50} more files\n"
                latex += "    \\end{itemize}\n"
        
        latex += "\\end{description}\n\n"
    
    latex += "\\end{document}\n"
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(latex)
        log_info(f"LaTeX report written to {output_file}")
    else:
        print(latex)
    
    return latex

