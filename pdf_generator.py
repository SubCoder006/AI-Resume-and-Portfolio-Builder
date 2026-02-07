"""
Optimized PDF resume export - strictly 1 page, compact formatting.

Generates ATS-friendly resume with:
- Name: Bold, 16pt
- Headers: Bold, 11pt  
- Content: Regular, 9pt
- Tight spacing to fit everything on one page
"""

import os
import re
import pathlib
from fpdf import FPDF


# ---------------------------------------------------------------------------
# Locate DejaVuSans.ttf
# ---------------------------------------------------------------------------
def _find_dejavu() -> str:
    """Return an absolute path to DejaVuSans.ttf or raise with instructions."""
    project_root = pathlib.Path(__file__).resolve().parent
    local = project_root / "DejaVuSans.ttf"
    if local.exists():
        return str(local)

    try:
        import fpdf as _fpdf_mod
        pkg = pathlib.Path(_fpdf_mod.__file__).parent
        bundled = list(pkg.rglob("DejaVuSans.ttf"))
        if bundled:
            return str(bundled[0])
    except Exception:
        pass

    candidates = [
        pathlib.Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
        pathlib.Path("/usr/share/fonts/TTF/DejaVuSans.ttf"),
        pathlib.Path.home() / "anaconda3" / "Library" / "Fonts" / "DejaVuSans.ttf",
        pathlib.Path("C:/Windows/Fonts/DejaVuSans.ttf"),
    ]
    for p in candidates:
        if p.exists():
            return str(p)

    raise FileNotFoundError(
        f"DejaVuSans.ttf not found. Place it in project root.\n"
        f"Download from: https://dejavu-fonts.github.io/"
    )


# ---------------------------------------------------------------------------
# Sanitize text
# ---------------------------------------------------------------------------
_EMOJI_RE = re.compile(
    "["
    "\U0001F600-\U0001F64F"
    "\U0001F300-\U0001F5FF"
    "\U0001F680-\U0001F6FF"
    "\U0001F1E0-\U0001F1FF"
    "\U00002702-\U000027B0"
    "\U000024C2-\U0001F251"
    "\U0001f926-\U0001f937"
    "\U00010000-\U0010ffff"
    "]+",
    flags=re.UNICODE,
)


def _sanitize(text: str) -> str:
    """Remove emojis and normalize text."""
    return _EMOJI_RE.sub("", text).replace("\u2022", "-").replace("\xa0", " ").replace("\t", " ").strip()


# ---------------------------------------------------------------------------
# One-page resume generator
# ---------------------------------------------------------------------------
def generate_pdf_resume(
    full_resume_text: str,
    filename: str = "output/resumes/resume.pdf",
) -> str:
    """
    Export ONE-PAGE ATS-optimized resume with compact formatting.
    
    Font sizes:
    - Name: 16pt bold
    - Section headers: 11pt bold
    - Content: 9pt regular
    """
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    font_path = _find_dejavu()

    pdf = FPDF()
    pdf.set_auto_page_break(auto=False)  # Strict 1-page control
    pdf.add_font("DejaVu", "", font_path, uni=True)
    pdf.add_font("DejaVu", "B", font_path, uni=True)
    
    pdf.add_page()
    pdf.set_margins(left=10, top=10, right=10)
    
    usable_width = pdf.w - 20  # 10mm margins on each side
    clean_text = _sanitize(full_resume_text)
    lines = clean_text.split("\n")
    
    is_first_line = True
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            pdf.ln(2)  # Minimal spacing for blank lines
            continue
        
        # Detect name (first non-empty line)
        if is_first_line:
            pdf.set_font("DejaVu", "B", 16)
            pdf.cell(usable_width, 6, stripped, align="C")
            pdf.ln(6)
            is_first_line = False
            continue
        
        # Detect section headers (ALL CAPS or ends with colon)
        is_header = stripped.isupper() or stripped.endswith(":")
        
        # Detect bullet points
        is_bullet = stripped.startswith(("-", "*", "•"))
        
        if is_header:
            pdf.ln(3)  # Small gap before headers
            pdf.set_font("DejaVu", "B", 11)
            pdf.set_x(10)
            pdf.multi_cell(usable_width, 4, stripped)
            pdf.ln(1)
        elif is_bullet:
            bullet_text = stripped.lstrip("-*• ").strip()
            pdf.set_font("DejaVu", "", 9)
            pdf.set_x(14)  # Indent bullets
            pdf.multi_cell(usable_width - 4, 3.5, f"• {bullet_text}")
        else:
            pdf.set_font("DejaVu", "", 9)
            pdf.set_x(10)
            pdf.multi_cell(usable_width, 3.5, stripped)
    
    pdf.output(filename)
    return os.path.abspath(filename)