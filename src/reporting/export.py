import io

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def export_alerts_to_excel(alerts: list) -> io.BytesIO:
    """Exports active alerts to an Excel file using openpyxl."""
    df = pd.DataFrame(alerts)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Active Alerts")
    output.seek(0)
    return output


def export_risk_report_pdf(metrics: dict, alerts: list) -> io.BytesIO:
    """Generates a PDF summary report using ReportLab."""
    output = io.BytesIO()
    doc = SimpleDocTemplate(output, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    story.append(Paragraph("PortfolioSentinel Risk Report", styles["Title"]))
    story.append(Spacer(1, 12))

    # Executive Summary
    story.append(Paragraph("Executive Summary", styles["Heading2"]))
    story.append(
        Paragraph(metrics.get("summary_text", "No summary provided."), styles["Normal"])
    )
    story.append(Spacer(1, 12))

    # Key Metrics Table
    story.append(Paragraph("Key Risk Metrics", styles["Heading2"]))
    data = [
        ["Metric", "Value"],
        ["Total Exposure", f"${metrics.get('total_exposure', 0)/1e6:,.2f}M"],
        ["Portfolio VaR (95%)", f"{metrics.get('var_95', 0):.2%}"],
        ["Expected Credit Loss", f"${metrics.get('expected_loss', 0)/1e6:,.2f}M"],
        ["Active Alerts", str(len(alerts))],
    ]
    table = Table(data, colWidths=[200, 200])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f77b4")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ]
        )
    )
    story.append(table)
    story.append(Spacer(1, 20))

    # Alerts
    story.append(Paragraph("Active Critical Alerts", styles["Heading2"]))
    critical_alerts = [a for a in alerts if a["severity"] == "Critical"]

    if not critical_alerts:
        story.append(Paragraph("No critical alerts at this time.", styles["Normal"]))
    else:
        for alert in critical_alerts:
            story.append(
                Paragraph(
                    f"- {alert['category']}: {alert['message']}", styles["Normal"]
                )
            )

    doc.build(story)
    output.seek(0)
    return output
