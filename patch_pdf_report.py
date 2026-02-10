"""
PDF Evidence Report Endpoint for Protevio Backend
===================================================
Add this endpoint to /root/protevio/backend/server.py

This generates a professional PDF evidence report when users find
their face on unauthorized websites. Useful for:
- DMCA takedown requests
- Legal proceedings
- Law enforcement reports
- GDPR right to erasure claims

Usage: POST /api/generate-report
Body: { "results": [...], "search_image_url": "..." }
Returns: PDF file download
"""

ENDPOINT_CODE = r'''
# ============================
# PDF EVIDENCE REPORT
# ============================
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.pdfgen import canvas as pdfcanvas
import uuid as _uuid

class ProtevioReportTemplate:
    """Custom page template with header/footer"""
    def __init__(self, report_id, generated_at):
        self.report_id = report_id
        self.generated_at = generated_at

    def on_page(self, canvas, doc):
        canvas.saveState()
        w, h = A4

        # Header bar
        canvas.setFillColor(HexColor('#1a1f2e'))
        canvas.rect(0, h - 28*mm, w, 28*mm, fill=1, stroke=0)

        # Header text
        canvas.setFillColor(HexColor('#5b9aff'))
        canvas.setFont('Helvetica-Bold', 16)
        canvas.drawString(20*mm, h - 18*mm, 'PROTEVIO AI')

        canvas.setFillColor(white)
        canvas.setFont('Helvetica', 8)
        canvas.drawRightString(w - 20*mm, h - 13*mm, f'Evidence Report')
        canvas.drawRightString(w - 20*mm, h - 18*mm, f'ID: {self.report_id}')
        canvas.drawRightString(w - 20*mm, h - 23*mm, f'Generated: {self.generated_at}')

        # Footer
        canvas.setFillColor(HexColor('#9ca3b8'))
        canvas.setFont('Helvetica', 7)
        canvas.drawString(20*mm, 12*mm,
            f'Protevio AI Evidence Report | {self.report_id} | protevio.com')
        canvas.drawRightString(w - 20*mm, 12*mm, f'Page {canvas.getPageNumber()}')

        # Footer line
        canvas.setStrokeColor(HexColor('#3a4562'))
        canvas.setLineWidth(0.5)
        canvas.line(20*mm, 17*mm, w - 20*mm, 17*mm)

        canvas.restoreState()


@app.route('/api/generate-report', methods=['POST'])
@require_auth
def generate_evidence_report():
    """Generate a PDF evidence report from search results"""
    try:
        data = request.get_json()
        results = data.get('results', [])
        search_date = data.get('search_date', datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC'))
        user_email = data.get('email', '')

        if not results:
            return jsonify({'error': 'No results to include in report'}), 400

        report_id = f'PRT-{datetime.now().strftime("%Y%m%d")}-{str(_uuid.uuid4())[:8].upper()}'
        generated_at = datetime.now().strftime('%B %d, %Y at %H:%M UTC')

        # Build PDF
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer, pagesize=A4,
            topMargin=35*mm, bottomMargin=25*mm,
            leftMargin=20*mm, rightMargin=20*mm
        )

        # Styles
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(
            'ReportTitle', parent=styles['Title'],
            fontSize=22, textColor=HexColor('#1a1f2e'),
            spaceAfter=6*mm, fontName='Helvetica-Bold'
        ))
        styles.add(ParagraphStyle(
            'SectionHead', parent=styles['Heading2'],
            fontSize=13, textColor=HexColor('#1a1f2e'),
            spaceBefore=8*mm, spaceAfter=4*mm,
            fontName='Helvetica-Bold',
            borderWidth=0, borderPadding=0,
            leftIndent=0
        ))
        styles.add(ParagraphStyle(
            'BodyGray', parent=styles['Normal'],
            fontSize=9, textColor=HexColor('#4a5568'),
            leading=14
        ))
        styles.add(ParagraphStyle(
            'Small', parent=styles['Normal'],
            fontSize=8, textColor=HexColor('#718096'),
            leading=11
        ))
        styles.add(ParagraphStyle(
            'Disclaimer', parent=styles['Normal'],
            fontSize=7, textColor=HexColor('#a0aec0'),
            leading=10, alignment=TA_CENTER
        ))

        story = []

        # Title
        story.append(Paragraph('Evidence Report', styles['ReportTitle']))
        story.append(Paragraph(
            'Facial Recognition Search Results Documentation',
            styles['BodyGray']
        ))
        story.append(Spacer(1, 6*mm))

        # Report metadata table
        meta_data = [
            ['Report ID:', report_id],
            ['Generated:', generated_at],
            ['Platform:', 'Protevio AI (protevio.com)'],
            ['Search Date:', search_date],
            ['Total Matches:', str(len(results))],
        ]
        if user_email:
            meta_data.append(['Requested By:', user_email])

        meta_table = Table(meta_data, colWidths=[35*mm, 120*mm])
        meta_table.setStyle(TableStyle([
            ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 9),
            ('FONT', (1, 0), (1, -1), 'Helvetica', 9),
            ('TEXTCOLOR', (0, 0), (0, -1), HexColor('#1a1f2e')),
            ('TEXTCOLOR', (1, 0), (1, -1), HexColor('#4a5568')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
            ('LEFTPADDING', (0, 0), (0, -1), 0),
        ]))
        story.append(meta_table)
        story.append(Spacer(1, 6*mm))

        # Divider
        story.append(HRFlowable(
            width="100%", thickness=1,
            color=HexColor('#e2e8f0'), spaceAfter=4*mm
        ))

        # Summary section
        story.append(Paragraph('Summary', styles['SectionHead']))

        domains = {}
        for r in results:
            d = r.get('domain', r.get('source_domain', 'Unknown'))
            domains[d] = domains.get(d, 0) + 1

        summary_text = (
            f'A facial recognition search conducted on <b>{search_date}</b> using the '
            f'Protevio AI platform identified <b>{len(results)} match(es)</b> across '
            f'<b>{len(domains)} website(s)</b>. The following table provides a detailed '
            f'record of each match found, including the source URL, domain, and similarity score.'
        )
        story.append(Paragraph(summary_text, styles['BodyGray']))
        story.append(Spacer(1, 4*mm))

        # Domain breakdown
        if len(domains) > 1:
            story.append(Paragraph('Matches by Domain:', styles['BodyGray']))
            story.append(Spacer(1, 2*mm))
            domain_rows = [['Domain', 'Matches Found']]
            for d, count in sorted(domains.items(), key=lambda x: -x[1]):
                domain_rows.append([d, str(count)])

            domain_table = Table(domain_rows, colWidths=[100*mm, 40*mm])
            domain_table.setStyle(TableStyle([
                ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 8),
                ('FONT', (0, 1), (-1, -1), 'Helvetica', 8),
                ('BACKGROUND', (0, 0), (-1, 0), HexColor('#1a1f2e')),
                ('TEXTCOLOR', (0, 0), (-1, 0), white),
                ('TEXTCOLOR', (0, 1), (-1, -1), HexColor('#4a5568')),
                ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#e2e8f0')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f7fafc')]),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ]))
            story.append(domain_table)
            story.append(Spacer(1, 6*mm))

        # Detailed results
        story.append(Paragraph('Detailed Results', styles['SectionHead']))
        story.append(HRFlowable(
            width="100%", thickness=0.5,
            color=HexColor('#e2e8f0'), spaceAfter=4*mm
        ))

        for i, result in enumerate(results):
            url = result.get('source_url', result.get('url', 'N/A'))
            domain = result.get('domain', result.get('source_domain', 'N/A'))
            similarity = result.get('similarity', result.get('score', result.get('distance', 0)))
            if isinstance(similarity, (int, float)):
                similarity = f'{similarity:.1%}' if similarity <= 1 else f'{similarity}%'

            page_url = result.get('page_url', result.get('source_page', ''))

            entry_data = [
                ['Match #', str(i + 1)],
                ['Image URL:', str(url)[:90]],
                ['Domain:', str(domain)],
                ['Similarity:', str(similarity)],
            ]
            if page_url:
                entry_data.append(['Page URL:', str(page_url)[:90]])

            entry_table = Table(entry_data, colWidths=[28*mm, 130*mm])
            entry_table.setStyle(TableStyle([
                ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 8),
                ('FONT', (1, 0), (1, -1), 'Helvetica', 8),
                ('TEXTCOLOR', (0, 0), (0, 0), HexColor('#5b9aff')),
                ('TEXTCOLOR', (0, 1), (0, -1), HexColor('#1a1f2e')),
                ('TEXTCOLOR', (1, 0), (1, -1), HexColor('#4a5568')),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('TOPPADDING', (0, 0), (-1, -1), 2),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
                ('LEFTPADDING', (0, 0), (0, -1), 0),
                ('BACKGROUND', (0, 0), (-1, 0), HexColor('#f0f4ff')),
            ]))

            story.append(KeepTogether([
                entry_table,
                Spacer(1, 3*mm),
                HRFlowable(width="100%", thickness=0.3, color=HexColor('#e2e8f0')),
                Spacer(1, 3*mm),
            ]))

        # Legal section
        story.append(Spacer(1, 8*mm))
        story.append(Paragraph('Legal Notice', styles['SectionHead']))
        story.append(Paragraph(
            'This report documents the results of a facial recognition similarity search '
            'conducted using the Protevio AI platform. The information contained herein is '
            'provided for evidentiary and informational purposes and may be used to support:',
            styles['BodyGray']
        ))
        story.append(Spacer(1, 2*mm))
        legal_items = [
            'DMCA takedown requests under 17 U.S.C. Section 512',
            'GDPR right to erasure requests under Article 17',
            'Legal proceedings related to unauthorized use of personal images',
            'Reports to law enforcement regarding identity theft or harassment',
        ]
        for item in legal_items:
            story.append(Paragraph(f'&bull;&nbsp;&nbsp;{item}', styles['BodyGray']))
        story.append(Spacer(1, 4*mm))
        story.append(Paragraph(
            'Protevio AI matches faces based on mathematical similarity of facial features. '
            'A high similarity score indicates a strong visual match but does not constitute '
            'definitive identification. Results should be verified independently.',
            styles['Small']
        ))

        # Disclaimer
        story.append(Spacer(1, 10*mm))
        story.append(HRFlowable(
            width="100%", thickness=0.5,
            color=HexColor('#e2e8f0'), spaceAfter=4*mm
        ))
        story.append(Paragraph(
            'This document was automatically generated by Protevio AI (protevio.com). '
            f'Report ID: {report_id}. The authenticity of this report can be verified by '
            'contacting support@protevio.com with the report ID.',
            styles['Disclaimer']
        ))

        # Build
        template = ProtevioReportTemplate(report_id, generated_at)
        doc.build(story, onFirstPage=template.on_page, onLaterPages=template.on_page)

        buffer.seek(0)
        filename = f'protevio_evidence_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'

        return send_file(
            buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )

    except Exception as e:
        print(f"[REPORT] Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Failed to generate report'}), 500
'''

# Also need this import at the top of server.py
IMPORTS_NEEDED = """
# Add these imports at the top of server.py if not already present:
from flask import send_file
import io
"""

if __name__ == '__main__':
    print("=" * 60)
    print("PDF EVIDENCE REPORT ENDPOINT")
    print("=" * 60)
    print(IMPORTS_NEEDED)
    print("\nPaste the endpoint code into server.py")
    print("Install: pip install reportlab")
