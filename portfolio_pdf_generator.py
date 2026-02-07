"""
Portfolio PDF generator - detailed, multi-page showcase.

Generates comprehensive portfolio PDF with:
- Detailed project descriptions
- Professional layout with larger fonts
- Multi-page support for complete work showcase
"""

import os
import pathlib
from fpdf import FPDF


# ---------------------------------------------------------------------------
# Locate DejaVuSans.ttf
# ---------------------------------------------------------------------------
def _find_dejavu() -> str:
    """Return an absolute path to DejaVuSans.ttf."""
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
        "DejaVuSans.ttf font not found!\n\n"
        "Please download it from: https://dejavu-fonts.github.io/\n"
        "Then place it in the same folder as app.py\n\n"
        f"Searched in these locations:\n" + 
        "\n".join(f"  - {p}" for p in candidates)
    )


# ---------------------------------------------------------------------------
# Portfolio PDF class
# ---------------------------------------------------------------------------
class PortfolioPDF(FPDF):
    """Custom PDF class for portfolio with header/footer."""
    
    def __init__(self, candidate_name: str):
        super().__init__()
        self.candidate_name = candidate_name
        
    def header(self):
        """Page header."""
        if self.page_no() > 1:  # Skip header on first page
            self.set_font("DejaVu", "I", 8)
            self.set_text_color(100, 100, 100)
            self.cell(0, 10, f"{self.candidate_name} - Portfolio", align="L")
            self.ln(15)
    
    def footer(self):
        """Page footer."""
        self.set_y(-15)
        self.set_font("DejaVu", "I", 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")


# ---------------------------------------------------------------------------
# Main generator
# ---------------------------------------------------------------------------
def generate_portfolio_pdf(
    portfolio_content: str,
    candidate_name: str,
    filename: str = "output/portfolios/portfolio.pdf",
    include_image_placeholders: bool = False,
    project_images: dict = None
) -> str:
    """
    Generate detailed portfolio PDF with optional images.
    
    Args:
        portfolio_content: Full portfolio text with sections
        candidate_name: Name for header
        filename: Output path
        include_image_placeholders: If True, add gray boxes for images (default: False)
        project_images: Optional dict mapping project names to image paths
    
    Returns:
        Absolute path to generated PDF
    """
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    font_path = _find_dejavu()
    
    pdf = PortfolioPDF(candidate_name)
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_font("DejaVu", "", font_path, uni=True)
    pdf.add_font("DejaVu", "B", font_path, uni=True)
    pdf.add_font("DejaVu", "I", font_path, uni=True)
    
    pdf.add_page()
    pdf.set_margins(left=15, top=15, right=15)
    
    usable_width = pdf.w - 30
    
    lines = portfolio_content.split("\n")
    
    for line in lines:
        stripped = line.strip()
        
        if not stripped:
            pdf.ln(4)
            continue
        
        # Detect main title (first line or ALL CAPS)
        if pdf.page_no() == 1 and pdf.get_y() < 30:
            pdf.set_font("DejaVu", "B", 20)
            pdf.set_text_color(0, 51, 102)  # Dark blue
            pdf.cell(usable_width, 10, stripped, align="C")
            pdf.ln(12)
            continue
        
        # Detect section headers (ALL CAPS or ends with colon)
        if stripped.isupper() and len(stripped) > 3:
            pdf.ln(6)
            pdf.set_font("DejaVu", "B", 14)
            pdf.set_text_color(0, 51, 102)
            pdf.cell(usable_width, 8, stripped)
            pdf.ln(8)
            
            # Add subtle line under header
            pdf.set_draw_color(200, 200, 200)
            pdf.line(15, pdf.get_y(), pdf.w - 15, pdf.get_y())
            pdf.ln(4)
            continue
        
        # Detect subsection headers (Title Case with colon or bold indicators)
        if stripped.endswith(":") and not stripped.startswith(("-", "*", "•")):
            pdf.ln(3)
            pdf.set_font("DejaVu", "B", 11)
            pdf.set_text_color(0, 0, 0)
            pdf.multi_cell(usable_width, 6, stripped)
            pdf.ln(2)
            continue
        
        # Handle image placeholders/markers - ONLY if enabled
        if "[" in stripped and "Image" in stripped and "]" in stripped:
            if include_image_placeholders:
                # Add placeholder box
                pdf.ln(3)
                pdf.set_fill_color(240, 240, 240)
                pdf.set_draw_color(180, 180, 180)
                pdf.set_font("DejaVu", "I", 9)
                pdf.set_text_color(100, 100, 100)
                
                # Create placeholder box
                pdf.rect(15, pdf.get_y(), usable_width, 40, "DF")
                pdf.set_y(pdf.get_y() + 15)
                pdf.cell(usable_width, 10, stripped, align="C")
                pdf.ln(30)
            # If not including placeholders, skip the line entirely
            continue
        
        # Detect bullet points
        if stripped.startswith(("-", "*", "•")):
            bullet_text = stripped.lstrip("-*• ").strip()
            pdf.set_font("DejaVu", "", 10)
            pdf.set_text_color(0, 0, 0)
            pdf.set_x(20)  # Indent
            pdf.multi_cell(usable_width - 5, 5, f"• {bullet_text}")
            continue
        
        # Regular paragraph text
        pdf.set_font("DejaVu", "", 10)
        pdf.set_text_color(0, 0, 0)
        pdf.multi_cell(usable_width, 5, stripped)
    
    pdf.output(filename)
    return os.path.abspath(filename)