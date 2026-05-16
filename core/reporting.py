from pathlib import Path
from datetime import datetime
import re
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

def _clean(md: str) -> str:
    return re.sub(r"[#*_`>]", "", md).strip()

def build_pdf_report(title: str, markdown_content: str, output_dir: str = "reports") -> str:
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    path = Path(output_dir) / f"metavista_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

    doc = SimpleDocTemplate(str(path), pagesize=letter)
    styles = getSampleStyleSheet()
    story = [Paragraph(title, styles["Title"]), Spacer(1, 12)]

    for line in markdown_content.splitlines():
        line = line.strip()
        if not line:
            story.append(Spacer(1, 8))
        elif line.startswith("#"):
            story.append(Paragraph(_clean(line), styles["Heading2"]))
        else:
            story.append(Paragraph(_clean(line), styles["BodyText"]))

    doc.build(story)
    return str(path)
