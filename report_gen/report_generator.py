import template
import config
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
import re


def format_bold(text):
    return re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)

def create_pdf(filename, report_content):
    PAGE_WIDTH, PAGE_HEIGHT = A4
    MARGIN_LEFT = 60
    MARGIN_RIGHT = 60

    doc = SimpleDocTemplate(filename, pagesize=A4, leftMargin=MARGIN_LEFT, rightMargin=MARGIN_RIGHT)

    styles = getSampleStyleSheet()
    normal_style = styles["Normal"]
    normal_style.leading = 14  # Adjust line spacing
    bold_style = ParagraphStyle("Heading", parent=styles["Heading2"], fontSize=14, spaceAfter=10)

    elements = []

    # Page 1: Disclaimer
    elements.append(Paragraph("Disclaimer", bold_style))
    elements.append(Paragraph(format_bold(template.discl).replace("\n", "<br/>"), normal_style))
    elements.append(PageBreak())

    # Page 2: Introduction
    elements.append(Paragraph("Introduction", bold_style))
    elements.append(Paragraph(format_bold(template.intro).replace("\n", "<br/>"), normal_style))
    elements.append(PageBreak())

    # Page 3: Table of Contents
    elements.append(Paragraph("Table of Contents", bold_style))
    elements.append(Paragraph(format_bold(template.report_structure).replace("\n", "<br/>"), normal_style))
    elements.append(PageBreak())

    # Page 4+: Main Report Content
    elements.append(Paragraph(f"COMPREHENSIVE HEALTH ANALYSIS PREPARED FOR {config.PATIENT_NAME}", bold_style))
    elements.append(Paragraph(format_bold(report_content).replace("\n", "<br/>"), normal_style))

    doc.build(elements)
