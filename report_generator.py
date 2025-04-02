"""
PDF and Excel report generation for the Carbon Footprint Calculator
"""
import io
import base64
from datetime import datetime
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def generate_pdf_report(organization_name, industry, reporting_year, num_employees,
                        total_emissions, emissions_by_scope, emissions_by_category,
                        recommendations):
    """
    Generate a PDF report of carbon footprint calculation results.
    
    Parameters:
    - organization_name: Name of the organization
    - industry: Industry type
    - reporting_year: Year of reporting
    - num_employees: Number of employees
    - total_emissions: Total emissions in tonnes CO2e
    - emissions_by_scope: Dictionary with emissions by scope
    - emissions_by_category: Dictionary with emissions by category
    - recommendations: Dictionary with recommendations
    
    Returns:
    - PDF file as bytes
    """
    # Create a file-like object for the PDF
    buffer = io.BytesIO()
    
    # Create the PDF document
    doc = SimpleDocTemplate(buffer, pagesize=letter, 
                            leftMargin=0.5*inch, rightMargin=0.5*inch,
                            topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    heading_style = styles['Heading1']
    subheading_style = styles['Heading2']
    normal_style = styles['Normal']
    
    # Custom styles
    table_title_style = ParagraphStyle(
        'TableTitle',
        parent=styles['Heading3'],
        fontSize=12,
        leading=14,
        spaceBefore=10,
        spaceAfter=4
    )
    
    # Content elements
    elements = []
    
    # Title and header
    elements.append(Paragraph(f"Carbon Footprint Report", title_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Organization info
    elements.append(Paragraph(f"Organization: {organization_name}", styles['Heading3']))
    elements.append(Paragraph(f"Industry: {industry}", normal_style))
    elements.append(Paragraph(f"Reporting Year: {reporting_year}", normal_style))
    elements.append(Paragraph(f"Number of Employees: {num_employees}", normal_style))
    elements.append(Paragraph(f"Report Generated: {datetime.now().strftime('%B %d, %Y')}", normal_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Total emissions
    elements.append(Paragraph("Total Carbon Footprint", heading_style))
    elements.append(Paragraph(f"{total_emissions:.2f} tonnes CO₂e", normal_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Emissions by scope
    elements.append(Paragraph("Emissions by Scope", subheading_style))
    
    # Create table data
    scope_data = [['Scope', 'Emissions (tonnes CO₂e)', 'Percentage']]
    for scope, value in emissions_by_scope.items():
        percentage = (value / total_emissions) * 100 if total_emissions > 0 else 0
        scope_data.append([scope, f"{value:.2f}", f"{percentage:.1f}%"])
    
    # Create table
    scope_table = Table(scope_data, colWidths=[2*inch, 2*inch, 1.5*inch])
    scope_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgreen),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elements.append(scope_table)
    elements.append(Spacer(1, 0.2*inch))
    
    # Emissions by category
    elements.append(Paragraph("Emissions by Category", subheading_style))
    
    # Create table data
    category_data = [['Category', 'Emissions (tonnes CO₂e)', 'Percentage']]
    sorted_categories = sorted(emissions_by_category.items(), key=lambda x: x[1], reverse=True)
    
    for category, value in sorted_categories:
        percentage = (value / total_emissions) * 100 if total_emissions > 0 else 0
        category_data.append([category, f"{value:.2f}", f"{percentage:.1f}%"])
    
    # Create table
    category_table = Table(category_data, colWidths=[3*inch, 2*inch, 1.5*inch])
    category_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgreen),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elements.append(category_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Top recommendations
    elements.append(Paragraph("Key Recommendations", subheading_style))
    
    # Find top 3 emission categories
    top_categories = [cat for cat, _ in sorted_categories[:3]]
    
    for category in top_categories:
        if category in recommendations:
            elements.append(Paragraph(f"{category}:", table_title_style))
            rec_list = recommendations[category]
            for rec in rec_list[:3]:  # Only show top 3 recommendations per category
                elements.append(Paragraph(f"• {rec}", normal_style))
            elements.append(Spacer(1, 0.1*inch))
    
    # Build the PDF
    doc.build(elements)
    
    # Get the PDF data
    pdf_data = buffer.getvalue()
    buffer.close()
    
    return pdf_data

def generate_excel_report(organization_name, industry, reporting_year, num_employees,
                         total_emissions, emissions_by_scope, emissions_by_category,
                         recommendations):
    """
    Generate an Excel report of carbon footprint calculation results.
    
    Parameters are the same as generate_pdf_report.
    
    Returns:
    - Excel file as bytes
    """
    buffer = io.BytesIO()
    
    # Create a new Excel writer object
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        workbook = writer.book
        
        # Summary sheet
        summary_data = {
            "Metric": ["Organization", "Industry", "Reporting Year", "Number of Employees", 
                      "Total Emissions (tonnes CO₂e)"],
            "Value": [organization_name, industry, reporting_year, num_employees, 
                     f"{total_emissions:.2f}"]
        }
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        # Format Summary sheet
        summary_sheet = writer.sheets['Summary']
        summary_sheet.set_column('A:A', 25)
        summary_sheet.set_column('B:B', 20)
        
        # Emissions by Scope sheet
        scope_data = {
            "Scope": list(emissions_by_scope.keys()),
            "Emissions (tonnes CO₂e)": list(emissions_by_scope.values()),
            "Percentage": [(value / total_emissions) * 100 if total_emissions > 0 else 0 
                          for value in emissions_by_scope.values()]
        }
        scope_df = pd.DataFrame(scope_data)
        scope_df.to_excel(writer, sheet_name='Emissions by Scope', index=False)
        
        # Format Scope sheet
        scope_sheet = writer.sheets['Emissions by Scope']
        scope_sheet.set_column('A:A', 15)
        scope_sheet.set_column('B:B', 25)
        scope_sheet.set_column('C:C', 15)
        
        # Emissions by Category sheet
        category_data = {
            "Category": list(emissions_by_category.keys()),
            "Emissions (tonnes CO₂e)": list(emissions_by_category.values()),
            "Percentage": [(value / total_emissions) * 100 if total_emissions > 0 else 0 
                          for value in emissions_by_category.values()]
        }
        category_df = pd.DataFrame(category_data)
        category_df = category_df.sort_values("Emissions (tonnes CO₂e)", ascending=False)
        category_df.to_excel(writer, sheet_name='Emissions by Category', index=False)
        
        # Format Category sheet
        category_sheet = writer.sheets['Emissions by Category']
        category_sheet.set_column('A:A', 25)
        category_sheet.set_column('B:B', 25)
        category_sheet.set_column('C:C', 15)
        
        # Recommendations sheet
        recommendations_data = []
        for category, recs in recommendations.items():
            for rec in recs:
                recommendations_data.append({"Category": category, "Recommendation": rec})
        
        if recommendations_data:
            rec_df = pd.DataFrame(recommendations_data)
            rec_df.to_excel(writer, sheet_name='Recommendations', index=False)
            
            # Format Recommendations sheet
            rec_sheet = writer.sheets['Recommendations']
            rec_sheet.set_column('A:A', 25)
            rec_sheet.set_column('B:B', 60)
    
    # Get the Excel data
    excel_data = buffer.getvalue()
    buffer.close()
    
    return excel_data

def get_download_link(file_data, file_name, display_text):
    """
    Generate a download link for a given file.
    
    Parameters:
    - file_data: File data as bytes
    - file_name: Name of the file to download
    - display_text: Text to display for the download link
    
    Returns:
    - HTML string with the download link
    """
    b64 = base64.b64encode(file_data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{file_name}" class="download-button">{display_text}</a>'
    return href