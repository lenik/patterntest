"""PDF report format (converted from LaTeX)"""

import os
import sys
import subprocess
import tempfile
from typing import List, Optional
from ..models import TestResult
from logger import log_info, log_error
from .latex import generate_latex_report


def generate_pdf_report(results: List[TestResult], program_path: str, mode: str,
                        output_file: Optional[str] = None) -> str:
    """Generate PDF report by converting LaTeX"""
    # Generate LaTeX first
    latex_content = generate_latex_report(results, program_path, mode, None)
    
    # Create temporary LaTeX file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.tex', delete=False, encoding='utf-8') as f:
        tex_file = f.name
        f.write(latex_content)
    
    try:
        # Determine output PDF file
        if output_file:
            pdf_file = output_file
            if not pdf_file.endswith('.pdf'):
                pdf_file = output_file + '.pdf'
        else:
            pdf_file = tex_file.replace('.tex', '.pdf')
        
        # Run pdflatex
        cmd = ['pdflatex', '-interaction=nonstopmode', '-output-directory', os.path.dirname(tex_file) or '.', tex_file]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Clean up auxiliary files
        base_name = os.path.splitext(tex_file)[0]
        for ext in ['.aux', '.log', '.out']:
            aux_file = base_name + ext
            if os.path.exists(aux_file):
                try:
                    os.remove(aux_file)
                except:
                    pass
        
        # Check if PDF was created
        expected_pdf = base_name + '.pdf'
        if os.path.exists(expected_pdf):
            if output_file and expected_pdf != pdf_file:
                import shutil
                shutil.move(expected_pdf, pdf_file)
            log_info(f"PDF report written to {pdf_file}")
            return pdf_file
        else:
            log_error(f"PDF generation failed. LaTeX output:\n{result.stdout}\n{result.stderr}")
            return None
            
    except subprocess.TimeoutExpired:
        log_error("PDF generation timed out")
        return None
    except FileNotFoundError:
        log_error("pdflatex not found. Please install LaTeX (e.g., texlive)")
        return None
    except Exception as e:
        log_error(f"Error generating PDF: {e}")
        return None
    finally:
        # Clean up temporary LaTeX file
        try:
            os.remove(tex_file)
        except:
            pass

