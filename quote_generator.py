from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime, timedelta
import os

def generate_quote_pdf(
    inquiry_details: dict,  
    rate_details: dict,
    output_path: str
) -> str:
    """Generate professional PDF quote for customer"""

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=1.5*cm,
        leftMargin=1.5*cm,
        topMargin=1.5*cm,
        bottomMargin=1.5*cm
    )

    elements = []
    styles = getSampleStyleSheet()

    # ── Custom Styles ────────────────────────────────────────────────
    header_style = ParagraphStyle(
        'Header',
        parent=styles['Normal'],
        fontSize=22,
        textColor=colors.white,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold',
        spaceAfter=5
    )

    subheader_style = ParagraphStyle(
        'SubHeader',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.white,
        alignment=TA_CENTER,
        fontName='Helvetica'
    )

    section_title_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#1e3a5f'),
        fontName='Helvetica-Bold',
        spaceAfter=8,
        spaceBefore=12
    )

    small_style = ParagraphStyle(
        'Small',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#666666'),
        fontName='Helvetica'
    )

    # ── Header Section ───────────────────────────────────────────────
    header_data = [[
        Paragraph("ABC INTERNATIONAL LOGISTICS", 
        ParagraphStyle(
            'Header',
            parent=styles['Normal'],
            fontSize=18,
            textColor=colors.white,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
            spaceAfter=5
        ))
    ]]
    header_table = Table(header_data, colWidths=[18*cm])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#1e3a5f')),
        ('TOPPADDING', (0,0), (-1,-1), 15),
        ('BOTTOMPADDING', (0,0), (-1,-1), 15),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    elements.append(header_table)

    # Sub header
    sub_data = [[
        Paragraph("PECHS Shahrah-e-Faisal, Karachi, Pakistan", subheader_style),
    ]]
    sub_table = Table(sub_data, colWidths=[18*cm])
    sub_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#2196F3')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 20),
        ('RIGHTPADDING', (0,0), (-1,-1), 20),
    ]))
    elements.append(sub_table)
    elements.append(Spacer(1, 15))

    # ── Quote Title & Reference ──────────────────────────────────────
    today = datetime.now()
    valid_until = today + timedelta(days=3)

    quote_info_data = [
        [
            Paragraph("<b>FREIGHT QUOTATION</b>", ParagraphStyle(
                'QuoteTitle',
                parent=styles['Normal'],
                fontSize=16,
                textColor=colors.HexColor('#1e3a5f'),
                fontName='Helvetica-Bold'
            )),
            Paragraph(
                f"<b>Quote Ref:</b>"
                f"{inquiry_details.get('reference_number', 'FR-2026-0001')}<br/>"
                f"<b>Date:</b> {today.strftime('%d %B %Y')}<br/>"
                f"<b>Valid Until:</b> {valid_until.strftime('%d %B %Y')}",
                ParagraphStyle(
                    'QuoteRef',
                    parent=styles['Normal'],
                    fontSize=10,
                    textColor=colors.HexColor('#333333'),
                    fontName='Helvetica',
                    alignment=TA_RIGHT
                )
            )
        ]
    ]
    quote_info_table = Table(quote_info_data, colWidths=[10*cm, 8*cm])
    quote_info_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))
    elements.append(quote_info_table)
    elements.append(HRFlowable(width="100%", thickness=2,
                               color=colors.HexColor('#2196F3')))
    elements.append(Spacer(1, 10))

    # ── Customer Details ─────────────────────────────────────────────
    elements.append(Paragraph("CUSTOMER DETAILS", section_title_style))

    customer_data = [
        [
            "Customer Name:", 
            inquiry_details.get('customer_name', 'N/A'),
         "Company:", 
         inquiry_details.get('company_name', 'N/A')
        ],
        [
            "Email:", 
            inquiry_details.get('email', 'N/A'),
         "Phone:", 
         inquiry_details.get('phone', 'N/A')
        ],
        [
            "Country:",
            inquiry_details.get('country', 'N/A'),
            "",
            ""
        ],
    ]
    customer_table = Table(customer_data, colWidths=[3.5*cm, 6*cm, 3.5*cm, 5*cm])
    customer_table.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTNAME', (2,0), (2,-1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor('#333333')),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f0f7ff')),
        ('ROWBACKGROUNDS', (0,0), (-1,-1),
         [colors.HexColor('#f0f7ff'), colors.HexColor('#e0efff')]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#ccddee')),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(customer_table)
    elements.append(Spacer(1, 10))

    # ── Services Required ─────────────────────────────────────────────
    elements.append(Paragraph("SERVICES REQUIRED", section_title_style))

    services_data = [[
        "Services:",
        inquiry_details.get('services_required', 'N/A')
    ]]
    services_table = Table(services_data, colWidths = [3.5*cm, 14.5*cm])
    services_table.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f0fff0')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#bbddbb')),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(services_table)
    elements.append(Spacer(1,10))

    # ── Cargo Requirements ───────────────────────────────────────────
    elements.append(Paragraph("CARGO REQUIREMENTS", section_title_style))

    # Wrap message in Paragraph for long text
    message_para = Paragraph(
        inquiry_details.get('message', 'N/A'),
        ParagraphStyle(
            'MessageStyle',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#333333'),
            fontName='Helvetica'
        )
    )

    message_data = [["Requirements:", message_para]]
    message_table = Table(message_data, colWidths=[3.5*cm, 14.5*cm])
    message_table.setStyle(TableStyle([
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#fffaf0')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#ddcc99')),
        ('PADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    elements.append(message_table)
    elements.append(Spacer(1, 10))
     
     
    # ── Rate Breakdown ───────────────────────────────────────────────
    elements.append(Paragraph("RATE BREAKDOWN (USD)", section_title_style))

    rate_data = [
        ["DESCRIPTION", "AMOUNT (USD)"],
        ["Ocean/Air Freight Rate",
         f"$ {rate_details.get('ocean_freight', '0')}"],
        ["Origin Charges (THC, BL Fee, Seal)",
         f"$ {rate_details.get('origin_charges', '0')}"],
        ["Destination Charges (THC, Customs)",
         f"$ {rate_details.get('destination_charges', '0')}"],
        ["Inland Transportation",
         f"$ {rate_details.get('inland_transport', '0')}"],
        ["Insurance",
         f"$ {rate_details.get('insurance', '0')}"],
    ]

    # Calculate total
    try:
        total = (
            float(rate_details.get('ocean_freight', 0)) +
            float(rate_details.get('origin_charges', 0)) +
            float(rate_details.get('destination_charges', 0)) +
            float(rate_details.get('inland_transport', 0)) +
            float(rate_details.get('insurance', 0))
        )
    except:
        total = 0

    rate_data.append(["TOTAL AMOUNT", f"$ {total:.2f}"])

    rate_table = Table(rate_data, colWidths=[13*cm, 5*cm])
    rate_table.setStyle(TableStyle([
        # Header row
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e3a5f')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 11),
        ('ALIGN', (1,0), (1,-1), 'RIGHT'),
        # Data rows
        ('FONTNAME', (0,1), (-1,-2), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-2), 10),
        ('ROWBACKGROUNDS', (0,1), (-1,-2),
         [colors.white, colors.HexColor('#f5f5f5')]),
        # Total row
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#2196F3')),
        ('TEXTCOLOR', (0,-1), (-1,-1), colors.white),
        ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,-1), (-1,-1), 12),
        # Grid
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cccccc')),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(rate_table)
    elements.append(Spacer(1, 10))

    # ── Transit & Remarks ────────────────────────────────────────────
    transit_data = [
        ["Transit Time:",
         f"{rate_details.get('transit_time', 'N/A')} days",
         "Remarks:",
         rate_details.get('remarks', 'N/A')],
    ]
    transit_table = Table(transit_data, colWidths=[3.5*cm, 4*cm, 3.5*cm, 7*cm])
    transit_table.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTNAME', (2,0), (2,-1), 'Helvetica-Bold'),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#fff3cd')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#ddcc99')),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(transit_table)
    elements.append(Spacer(1, 10))

    # ── Bank Details ─────────────────────────────────────────────────
    elements.append(Paragraph("BANK DETAILS", section_title_style))

    bank_data = [
        ["Bank Name:", "Meezan Bank Limited",
         "Account Title:", "ABC International Logistics"],
        ["Account Number:", "0123-4567890-001",
         "IBAN:", "PK12MEZN0001234567890001"],
        ["Branch:", "PECHS Branch, Karachi",
         "Swift Code:", "MEZNPKKA"],
    ]
    bank_table = Table(bank_data, colWidths=[3.5*cm, 6*cm, 3.5*cm, 5*cm])
    bank_table.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTNAME', (2,0), (2,-1), 'Helvetica-Bold'),
        ('ROWBACKGROUNDS', (0,0), (-1,-1),
         [colors.HexColor('#f9f9f9'), colors.HexColor('#f0f0f0')]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cccccc')),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(bank_table)
    elements.append(Spacer(1, 10))

    # ── Terms & Conditions ───────────────────────────────────────────
    elements.append(Paragraph("TERMS & CONDITIONS", section_title_style))

    terms = [
        "1. Quotation validity: 3 days from date of issue unless otherwise stated.",
        "2. All rates are in USD and subject to change based on carrier availability and fuel surcharges.",
        "3. Payment must be made before cargo release unless credit terms are agreed in writing.",
        "4. Transit times are estimates only and not guaranteed.",
        "5. Cargo insurance is not included unless specifically requested and confirmed.",
        "6. Client is responsible for providing accurate and complete shipping documents.",
        "7. Customs duties, taxes, and inspection fees are not included in freight rates.",
        "8. Liability is limited to the value of freight charges paid.",
        "9. We are not liable for delays caused by weather, strikes, or events beyond our control.",
        "10. DG cargo must be declared at time of booking. Undeclared DG will be subject to penalties.",
    ]

    for term in terms:
        elements.append(Paragraph(term, small_style))
    elements.append(Spacer(1, 10))

    # ── Footer ───────────────────────────────────────────────────────
    footer_data = [[
        Paragraph(
            "Thank you for choosing ABC International Logistics! | "
            "a.wahab.mu@gmail.com | +92-333-2191264 | Karachi, Pakistan",
            ParagraphStyle(
                'Footer',
                parent=styles['Normal'],
                fontSize=9,
                textColor=colors.white,
                alignment=TA_CENTER,
                fontName='Helvetica'
            )
        )
    ]]
    footer_table = Table(footer_data, colWidths=[18*cm])
    footer_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#1e3a5f')),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    elements.append(footer_table)

    # Build PDF
    doc.build(elements)
    return output_path