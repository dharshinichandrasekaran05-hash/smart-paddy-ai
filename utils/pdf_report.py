"""
utils/pdf_report.py — Smart Paddy AI: PDF Report Generator
Place at: smart_paddy_ai/utils/pdf_report.py

Generates a downloadable diagnostic report containing:
  - Header with logo/title
  - Uploaded image + Grad-CAM image side-by-side
  - Disease prediction + confidence
  - Per-class probability breakdown
  - Severity analysis
  - Crop Health Index
  - Full treatment/prevention/fertilizer recommendations
  - Date & time stamp
"""

import io
import datetime
from PIL import Image

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, Image as RLImage,
)


# ─────────────────────── COLOUR PALETTE ───────────────────────
GREEN  = colors.HexColor("#2d7a2d")
LIME   = colors.HexColor("#e8f5e9")
AMBER  = colors.HexColor("#fff3e0")
RED    = colors.HexColor("#ffebee")
DARK   = colors.HexColor("#1a1a2e")
GREY   = colors.HexColor("#f5f5f5")
WHITE  = colors.white


# ─────────────────────── PIL → ReportLab Image ────────────────
def _pil_to_rl_image(pil_img: Image.Image, width_cm: float, height_cm: float) -> RLImage:
    """Convert a PIL image to a ReportLab Image flowable."""
    buf = io.BytesIO()
    pil_img.save(buf, format="PNG")
    buf.seek(0)
    return RLImage(buf, width=width_cm * cm, height=height_cm * cm)


# ─────────────────────── STYLES ───────────────────────────────
def _build_styles():
    base = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=base["Title"],
        fontSize=20,
        textColor=GREEN,
        spaceAfter=4,
        alignment=TA_CENTER,
        fontName="Helvetica-Bold",
    )
    subtitle_style = ParagraphStyle(
        "SubTitle",
        parent=base["Normal"],
        fontSize=10,
        textColor=colors.grey,
        alignment=TA_CENTER,
        spaceAfter=12,
    )
    heading_style = ParagraphStyle(
        "SectionHeading",
        parent=base["Heading2"],
        fontSize=12,
        textColor=GREEN,
        spaceBefore=10,
        spaceAfter=4,
        fontName="Helvetica-Bold",
    )
    body_style = ParagraphStyle(
        "BodyText",
        parent=base["Normal"],
        fontSize=9,
        leading=14,
        textColor=DARK,
    )
    bullet_style = ParagraphStyle(
        "BulletItem",
        parent=base["Normal"],
        fontSize=9,
        leading=14,
        leftIndent=12,
        bulletIndent=4,
        textColor=DARK,
    )
    label_style = ParagraphStyle(
        "Label",
        parent=base["Normal"],
        fontSize=8,
        textColor=colors.grey,
    )

    return {
        "title":    title_style,
        "subtitle": subtitle_style,
        "heading":  heading_style,
        "body":     body_style,
        "bullet":   bullet_style,
        "label":    label_style,
    }


# ─────────────────────── MAIN GENERATOR ───────────────────────
def generate_pdf_report(
    original_image:  Image.Image,
    gradcam_image:   Image.Image | None,
    disease:         str,
    confidence:      float,
    all_probs:       dict,
    severity:        dict,
    health_index:    dict,
    advisory:        dict,
    location:        str = "",
    farmer_name:     str = "",
) -> bytes:
    """
    Build and return a PDF report as raw bytes.

    Parameters
    ----------
    original_image : PIL Image — uploaded leaf photo
    gradcam_image  : PIL Image | None — Grad-CAM overlay
    disease        : str — predicted disease name
    confidence     : float — 0–1 model confidence
    all_probs      : dict — {class_name: pct_float}
    severity       : dict — from severity.estimate_severity()
    health_index   : dict — from severity.crop_health_index()
    advisory       : dict — from advisory.get_advisory()
    location       : str — optional farmer location
    farmer_name    : str — optional farmer name
    """
    buf    = io.BytesIO()
    doc    = SimpleDocTemplate(
        buf,
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )
    styles = _build_styles()
    story  = []

    ts = datetime.datetime.now().strftime("%d %B %Y  %H:%M:%S")

    # ── HEADER ────────────────────────────────────────────────
    story.append(Paragraph("🌾 Smart Paddy AI", styles["title"]))
    story.append(Paragraph(
        "Rice Disease Detection &amp; Agricultural Decision Support Report",
        styles["subtitle"]
    ))
    story.append(HRFlowable(width="100%", thickness=1, color=GREEN))
    story.append(Spacer(1, 0.3 * cm))

    # Meta table
    meta_data = [
        ["Report Date:", ts,           "Farmer:",   farmer_name or "—"],
        ["Location:",    location or "—", "Model:","EfficientNetB0"],
    ]
    meta_table = Table(meta_data, colWidths=[3 * cm, 5 * cm, 3 * cm, 5 * cm])
    meta_table.setStyle(TableStyle([
        ("FONTSIZE",    (0, 0), (-1, -1), 8),
        ("TEXTCOLOR",   (0, 0), (0, -1), colors.grey),
        ("TEXTCOLOR",   (2, 0), (2, -1), colors.grey),
        ("FONTNAME",    (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME",    (2, 0), (2, -1), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 0.4 * cm))

    # ── IMAGES ────────────────────────────────────────────────
    story.append(Paragraph("Leaf Image Analysis", styles["heading"]))

    img_row = [_pil_to_rl_image(original_image.resize((224, 224)), 7, 7)]
    labels_row = ["Original Image"]

    if gradcam_image is not None:
        img_row.append(_pil_to_rl_image(gradcam_image.resize((224, 224)), 7, 7))
        labels_row.append("Grad-CAM Heatmap (Infected Regions)")

    img_table = Table([img_row], colWidths=[8 * cm] * len(img_row))
    img_table.setStyle(TableStyle([
        ("ALIGN",   (0, 0), (-1, -1), "CENTER"),
        ("VALIGN",  (0, 0), (-1, -1), "MIDDLE"),
        ("BOX",     (0, 0), (0, 0), 1, colors.lightgrey),
        ("BOX",     (1, 0), (1, 0), 1, colors.lightgrey) if len(img_row) > 1 else ("", (0,0),(0,0), 0, WHITE),
    ]))
    story.append(img_table)

    lbl_table = Table(
        [[Paragraph(l, styles["label"]) for l in labels_row]],
        colWidths=[8 * cm] * len(labels_row)
    )
    lbl_table.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ]))
    story.append(lbl_table)
    story.append(Spacer(1, 0.4 * cm))

    # ── PREDICTION RESULTS ────────────────────────────────────
    story.append(Paragraph("Prediction Results", styles["heading"]))

    # Severity colour choice
    sev_pct   = severity.get("percentage", 0)
    sev_label = severity.get("label", "N/A")
    sev_bg    = LIME if sev_pct < 31 else (AMBER if sev_pct < 71 else RED)

    pred_data = [
        ["Detected Disease",  disease,
         "Confidence",        f"{confidence * 100:.1f}%"],
        ["Severity",          f"{sev_label}  ({sev_pct}%)",
         "Crop Health Index", f"{health_index['score']}/100  — {health_index['category']}"],
    ]
    pred_table = Table(pred_data, colWidths=[4 * cm, 5 * cm, 4 * cm, 5 * cm])
    pred_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), GREY),
        ("BACKGROUND", (0, 0), (0, 0), GREEN),
        ("TEXTCOLOR",  (0, 0), (0, 0), WHITE),
        ("FONTNAME",   (0, 0), (0, 0), "Helvetica-Bold"),
        ("FONTSIZE",   (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [GREY, sev_bg]),
        ("BOX",        (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ("INNERGRID",  (0, 0), (-1, -1), 0.25, colors.lightgrey),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(pred_table)
    story.append(Spacer(1, 0.3 * cm))

    # Per-class probabilities
    story.append(Paragraph("Class Probability Breakdown", styles["heading"]))
    sorted_probs = sorted(all_probs.items(), key=lambda x: -x[1])
    prob_rows    = [[
        Paragraph(cls, styles["body"]),
        Paragraph(f"{pct:.1f}%", styles["body"]),
        Paragraph("█" * int(pct / 5), styles["body"]),
    ] for cls, pct in sorted_probs]

    prob_table = Table(
        [["Class", "Probability", "Visual"]] + prob_rows,
        colWidths=[5 * cm, 3 * cm, 9 * cm],
    )
    prob_table.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, 0), GREEN),
        ("TEXTCOLOR",    (0, 0), (-1, 0), WHITE),
        ("FONTNAME",     (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",     (0, 0), (-1, -1), 8),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, GREY]),
        ("INNERGRID",    (0, 0), (-1, -1), 0.25, colors.lightgrey),
        ("BOX",          (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ("TOPPADDING",   (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 4),
    ]))
    story.append(prob_table)
    story.append(Spacer(1, 0.3 * cm))

    # ── ADVISORY ──────────────────────────────────────────────
    story.append(Paragraph("Agricultural Advisory", styles["heading"]))

    # Description
    story.append(Paragraph(
        advisory.get("description", ""), styles["body"]
    ))
    story.append(Spacer(1, 0.2 * cm))

    # Treatment
    story.append(Paragraph("Treatment:", styles["body"]))
    for item in advisory.get("treatment", []):
        story.append(Paragraph(f"• {item}", styles["bullet"]))

    story.append(Spacer(1, 0.15 * cm))

    # Prevention
    story.append(Paragraph("Prevention:", styles["body"]))
    for item in advisory.get("prevention", []):
        story.append(Paragraph(f"• {item}", styles["bullet"]))

    story.append(Spacer(1, 0.15 * cm))

    # Fertilizer + irrigation
    adv_data = [
        ["Fertilizer Advice", advisory.get("fertilizer", "—")],
        ["Irrigation Advice", advisory.get("irrigation", "—")],
    ]
    adv_table = Table(adv_data, colWidths=[4 * cm, 14 * cm])
    adv_table.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (0, -1), LIME),
        ("FONTNAME",     (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE",     (0, 0), (-1, -1), 9),
        ("INNERGRID",    (0, 0), (-1, -1), 0.25, colors.lightgrey),
        ("BOX",          (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ("TOPPADDING",   (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 5),
    ]))
    story.append(adv_table)
    story.append(Spacer(1, 0.5 * cm))

    # ── FOOTER ────────────────────────────────────────────────
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.lightgrey))
    story.append(Spacer(1, 0.2 * cm))
    story.append(Paragraph(
        "Generated by Smart Paddy AI — Research-Oriented Agricultural Decision Support System",
        ParagraphStyle("Footer", fontSize=7, textColor=colors.grey, alignment=TA_CENTER)
    ))
    story.append(Paragraph(
        f"Report generated on {ts}  |  AI Model: EfficientNetB0 Transfer Learning",
        ParagraphStyle("Footer2", fontSize=7, textColor=colors.grey, alignment=TA_CENTER)
    ))

    doc.build(story)
    return buf.getvalue()