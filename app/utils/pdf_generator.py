from fpdf import FPDF
from datetime import datetime
import os

def create_pdf(news_data):
    pdf = FPDF()
    pdf.add_page()
    
    # Header
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'RailPulse - Railway News', 0, 1, 'C')
    pdf.ln(10)
    
    # Content
    pdf.set_font('Arial', '', 12)
    for i, news in enumerate(news_data, 1):
        # Title
        pdf.set_font('Arial', 'B', 14)
        pdf.multi_cell(0, 10, f"{i}. {news['title']}")
        
        # Summary
        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(0, 10, news['summary'])
        
        # Metadata
        pdf.set_font('Arial', 'I', 10)
        pdf.cell(0, 10, f"Source: {news['source']}", 0, 1)
        pdf.cell(0, 10, f"Link: {news['link']}", 0, 1)
        pdf.cell(0, 10, f"Date: {news.get('date', 'N/A')}", 0, 1)
        pdf.ln(5)
    
    filename = f"railway_news_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf.output(filename)
    return filename
