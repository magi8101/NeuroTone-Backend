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
        elements.append(Paragraph(f'Parkinson detected: {detected}',normal_style))

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
        elements.append(Paragraph('Analysis Date: 2025-02-09 Predicted Condition: Vocal Polyp (89.33%)', normal_style))
        elements.append(Paragraph('<b>SUMMARY OF FINDINGS</b>', normal_style))
        
        summary = """The acoustic and clinical analysis reveals <b>significant</b> voice abnormalities consistent with a vocal polyp. The
        patient exhibits altered voice quality, increased perturbation measures, and deviations in fundamental
        frequency, suggesting a structural lesion on the vocal fold. These findings are clinically significant as they
        indicate impaired vocal fold function and potential chronic voice discomfort."""
        elements.append(Paragraph(summary, normal_style))

        elements.append(Paragraph('<b>ACOUSTIC ANALYSIS</b>', normal_style))
        acoustic_analysis = """Fundamental Frequency:
        - Mean: 267.23 Hz - Standard Deviation: 60.16 Hz - Clinical Significance: The mean fundamental frequency
        is within normal limits for an adult male voice. However, the elevated standard deviation indicates instability in
        pitch production, which is often associated with vocal fold lesions such as polyps.
        
        Voice Perturbation Measures:
        - Jitter: 2.34% - Shimmer: 79.80% - Harmonic Ratio: 0.003 - Clinical Significance: The jitter value is within
        normal limits, suggesting relatively stable pitch variations. However, the significantly elevated shimmer and
        reduced harmonic ratio indicate increased amplitude variations and poor harmonic structure, respectively.
        These findings are characteristic of a vocal polyp, which disrupts smooth vibration of the vocal folds.
        
        Additional Measurements:
        - Voice Period: 0.0037 seconds - Voiced Segments Ratio: 0.73 - Formant Frequency: 1463.52 Hz - Clinical
        Significance: The voice period is slightly prolonged, reflecting irregular vocal fold closure. The voiced"""
        elements.append(Paragraph(acoustic_analysis, normal_style))

        # Build the PDF
        doc.build(elements)
        print("PDF report generated successfully!")
        
    except Exception as e:
        print(f"Error generating PDF: {str(e)}")

if __name__ == '__main__':
    create_voice_pathology_report('High',2,3,4,5,6)