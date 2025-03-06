from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.colors import HexColor, pink
import matplotlib.pyplot as plt
import numpy as np

def create_voice_pathology_report(detected,pitch,intensity,f1,f2,f3):
    try:
        # Create the PDF document
        doc = SimpleDocTemplate(
            "voice_analysis_report.pdf",
            pagesize=letter,
            rightMargin=0.7*inch,
            leftMargin=0.7*inch,
            topMargin=0.7*inch,
            bottomMargin=0.7*inch
        )

        # Custom styles with left alignment
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            textColor=HexColor('#DB4486'),
            fontSize=16,
            spaceAfter=5,
            alignment=0,
            borderPadding=0.5
        )
        
        section_style = ParagraphStyle(
            'SectionStyle',
            parent=styles['Normal'],
            fontSize=11,
            textColor=colors.white,
            backColor=HexColor('#FFB6C1'),
            spaceBefore=15,
            spaceAfter=10,
            leftIndent=4,
            alignment=0,
            borderPadding=2
        )

        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            alignment=0
        )
        n_style=ParagraphStyle(
            'Customn',
            parent=styles['Normal'],
            ontSize=10,
            spaceAfter=6,
            alignment=2
        )

        elements = []

        header_data = [[
            Paragraph('<img src="logo.jpg" width="200" height="30"/> ', title_style),
            Paragraph('Voice Analysis Report', n_style)
        ]]
        header_table = Table(header_data, colWidths=[4*inch, 4*inch])
        header_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elements.append(header_table)
        elements.append(Spacer(1, 20))

   

        # Patient Information section - Changed to paragraphs
        elements.append(Paragraph('Patient Information', section_style))
        elements.append(Paragraph('Analysis Date: 2025-02-09', normal_style))
        elements.append(Paragraph(f'Parkinson\'s Probability: {detected}',normal_style))

        # Acoustic Measurements section
        elements.append(Paragraph('Acoustic Measurements', section_style))
        measurements_data = [
            ['Parameter', 'Value', 'Normal Range', 'Unit'],
            ['Mean Pitch', pitch, '85-255', 'Hz'],
            ['Mean Intensity ', intensity, '65-80', 'dB'],
            ['First Formant Frequency (F1)', f1, '300-900', 'Hz'],
            ['Second Formant Frequency (F2)', f2, '850-2500 ', 'Hz'],
            ['Third Formant Frequency (F3)', f3, '2000-3500', 'Hz'],
        ]
        
        measurements_table = Table(
            measurements_data, 
            colWidths=[2.5*inch, 1.7*inch, 1.7*inch, 1*inch]
        )
        measurements_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#FFB6C1')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(measurements_table)

        # Detailed Analysis section
        elements.append(Paragraph('Detailed Analysis', section_style))
        elements.append(Paragraph('<b>VOICE PATHOLOGY MEDICAL REPORT</b>', normal_style))
        elements.append(Paragraph('<b>PATIENT INFORMATION</b>', normal_style))
        elements.append(Paragraph(f'Analysis Date: 2025-02-09', normal_style))
        elements.append(Paragraph(f'Parkinson\'s Probability: {detected}', normal_style))
        elements.append(Paragraph('<b>SUMMARY OF FINDINGS</b>', normal_style))
        
        if detected=="High":
            summary = """The acoustic and clinical analysis indicates vocal patterns consistent with early parkinsonian changes in voice production. Key findings include reduced pitch variability, 
            decreased vocal intensity, and altered formant characteristics. These abnormalities are typical indicators of the subtle motor changes affecting laryngeal control and respiratory support."""
            elements.append(Paragraph(summary, normal_style))

            elements.append(Paragraph('<b>ACOUSTIC ANALYSIS</b>', normal_style))
            acoustic_analysis = """<b>Fundamental Frequency</b><br/><br/>
Mean Pitch (F0): Significantly above the normal range, showing reduced pitch control and stability. This elevation is commonly associated with early parkinsonian voice changes.<br/><br/>
<b>Voice Intensity Measures</b><br/><br/>
The average vocal intensity falls below the typical range, indicating reduced respiratory support and diminished vocal projection typical in parkinsonian speech.<br/><br/>
<b>Formant Analysis</b><br/><br/>
• F1: Shows deviation from normal range, suggesting altered jaw opening and tongue height control<br/>
• F2: Demonstrates restricted movement range, indicating reduced tongue mobility<br/>
• F3: Values indicate changes in vocal tract configuration and articulation<br/><br/>
<b>Clinical Significance:</b> The combination of these acoustic measures, particularly the altered formant patterns and reduced intensity control, strongly suggests early parkinsonian voice changes."""
            elements.append(Paragraph(acoustic_analysis, normal_style))
            elements.append(Paragraph('<b>RECOMMENDATIONS</b>', normal_style))
            recommendations = """<b>1. Medical Management</b><br/>
• Referral to a neurologist for comprehensive evaluation<br/>
• Consider speech therapy assessment<br/><br/>
<b>2. Voice Therapy</b><br/>
• Early intervention with speech-language pathologist<br/>
• Focus on respiratory support and voice strengthening exercises<br/><br/>
<b>3. Follow-Up</b><br/>
• Regular monitoring of voice parameters every 3-4 months<br/>
• Track progression of vocal changes<br/><br/>
<b>4. Additional Testing</b><br/>
• Consider complete neurological examination<br/>
• Regular assessment of other motor symptoms"""
            elements.append(Paragraph(recommendations, normal_style))
        # Build the PDF
        doc.build(elements)
        print("PDF report generated successfully!")
        
    except Exception as e:
        print(f"Error generating PDF: {str(e)}")

if __name__ == '__main__':
    create_voice_pathology_report('High',2,3,4,5,6)