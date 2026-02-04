"""
Report Generator Module
Generates PDF reports for contract analysis
"""
from typing import Dict, List
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import json
import os
from pathlib import Path


class ReportGenerator:
    """Generate PDF reports for contract analysis"""
    
    def __init__(self, output_dir: str = None):
        """Initialize report generator"""
        self.output_dir = Path(output_dir) if output_dir else Path("data/reports")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize styles
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f4788'),
            spaceAfter=30,
            alignment=TA_CENTER
        ))
        
        # Heading style
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2c5aa0'),
            spaceAfter=12,
            spaceBefore=12
        ))
        
        # Risk High
        self.styles.add(ParagraphStyle(
            name='RiskHigh',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.red,
            spaceAfter=6
        ))
        
        # Risk Medium
        self.styles.add(ParagraphStyle(
            name='RiskMedium',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.orange,
            spaceAfter=6
        ))
        
        # Risk Low
        self.styles.add(ParagraphStyle(
            name='RiskLow',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.green,
            spaceAfter=6
        ))
    
    def generate_full_report(self, analysis_results: Dict, output_filename: str = None) -> str:
        """
        Generate comprehensive PDF report
        
        Args:
            analysis_results: Complete analysis results dictionary
            output_filename: Optional custom filename
            
        Returns:
            Path to generated PDF
        """
        if not output_filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"contract_analysis_{timestamp}.pdf"
        
        output_path = self.output_dir / output_filename
        
        # Create PDF document
        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Build content
        story = []
        
        # Title page
        story.extend(self._create_title_page(analysis_results))
        story.append(PageBreak())
        
        # Executive Summary
        story.extend(self._create_executive_summary(analysis_results))
        story.append(PageBreak())
        
        # Risk Assessment
        story.extend(self._create_risk_section(analysis_results))
        story.append(PageBreak())
        
        # Entity Information
        story.extend(self._create_entity_section(analysis_results))
        
        # Clause Analysis
        story.extend(self._create_clause_section(analysis_results))
        story.append(PageBreak())
        
        # Recommendations
        story.extend(self._create_recommendations_section(analysis_results))
        
        # Build PDF
        doc.build(story)
        
        return str(output_path)
    
    def _create_title_page(self, results: Dict) -> List:
        """Create title page"""
        elements = []
        
        # Title
        elements.append(Spacer(1, 2*inch))
        elements.append(Paragraph("Contract Analysis Report", self.styles['CustomTitle']))
        elements.append(Spacer(1, 0.5*inch))
        
        # Contract info
        contract_type = results.get('contract_classification', {}).get('contract_type', 'Unknown')
        elements.append(Paragraph(f"<b>Contract Type:</b> {contract_type}", self.styles['Normal']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Date
        report_date = datetime.now().strftime("%B %d, %Y")
        elements.append(Paragraph(f"<b>Report Generated:</b> {report_date}", self.styles['Normal']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Risk level
        risk_level = results.get('risk_assessment', {}).get('overall_level', 'Unknown')
        risk_color = {'HIGH': 'red', 'MEDIUM': 'orange', 'LOW': 'green'}.get(risk_level, 'black')
        elements.append(Paragraph(
            f"<b>Overall Risk Level:</b> <font color='{risk_color}'>{risk_level}</font>",
            self.styles['Normal']
        ))
        
        elements.append(Spacer(1, 1*inch))
        elements.append(Paragraph(
            "<i>This report is generated by Legal Assistant AI for informational purposes. "
            "Please consult with a qualified legal professional for legal advice.</i>",
            self.styles['Normal']
        ))
        
        return elements
    
    def _create_executive_summary(self, results: Dict) -> List:
        """Create executive summary section"""
        elements = []
        
        elements.append(Paragraph("Executive Summary", self.styles['CustomHeading']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Contract summary
        summary = results.get('llm_summary', 'No summary available.')
        elements.append(Paragraph(summary, self.styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Key statistics table
        risk_assessment = results.get('risk_assessment', {})
        
        data = [
            ['Metric', 'Value'],
            ['Overall Risk Score', f"{risk_assessment.get('overall_score', 0)}/100"],
            ['Total Risks Identified', str(risk_assessment.get('total_risks_found', 0))],
            ['High Priority Risks', str(len(risk_assessment.get('high_priority_risks', [])))],
            ['Clauses Analyzed', str(len(results.get('clause_analysis', [])))],
        ]
        
        table = Table(data, colWidths=[3*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        
        return elements
    
    def _create_risk_section(self, results: Dict) -> List:
        """Create risk assessment section"""
        elements = []
        
        elements.append(Paragraph("Risk Assessment", self.styles['CustomHeading']))
        elements.append(Spacer(1, 0.2*inch))
        
        risk_assessment = results.get('risk_assessment', {})
        
        # Overall assessment
        elements.append(Paragraph("<b>Overall Assessment</b>", self.styles['Heading3']))
        elements.append(Paragraph(
            risk_assessment.get('recommendation', 'No recommendation available.'),
            self.styles['Normal']
        ))
        elements.append(Spacer(1, 0.2*inch))
        
        # High priority risks
        high_priority = risk_assessment.get('high_priority_risks', [])
        if high_priority:
            elements.append(Paragraph("<b>High Priority Risks</b>", self.styles['Heading3']))
            
            for i, risk in enumerate(high_priority[:10], 1):  # Limit to top 10
                risk_text = f"{i}. <b>{risk.get('risk_type', 'Unknown')}</b> (Clause: {risk.get('clause_id', 'N/A')})"
                elements.append(Paragraph(risk_text, self.styles['RiskHigh']))
                
                if risk.get('description'):
                    elements.append(Paragraph(f"   {risk['description']}", self.styles['Normal']))
                
                elements.append(Spacer(1, 0.1*inch))
        
        # Risk mitigation strategies
        mitigation = results.get('mitigation_strategies', [])
        if mitigation:
            elements.append(Spacer(1, 0.3*inch))
            elements.append(Paragraph("<b>Risk Mitigation Strategies</b>", self.styles['Heading3']))
            
            for strategy in mitigation[:5]:  # Top 5 strategies
                elements.append(Paragraph(
                    f"<b>{strategy.get('risk_category', 'Category')}</b>",
                    self.styles['Normal']
                ))
                elements.append(Paragraph(
                    f"Strategy: {strategy.get('strategy', '')}",
                    self.styles['Normal']
                ))
                elements.append(Spacer(1, 0.1*inch))
        
        return elements
    
    def _create_entity_section(self, results: Dict) -> List:
        """Create entity information section"""
        elements = []
        
        elements.append(Paragraph("Key Information Extracted", self.styles['CustomHeading']))
        elements.append(Spacer(1, 0.2*inch))
        
        entities = results.get('entities', {})
        
        # Parties
        parties = entities.get('parties', [])
        if parties:
            elements.append(Paragraph("<b>Parties Involved</b>", self.styles['Heading3']))
            for party in parties[:5]:  # Limit to 5
                elements.append(Paragraph(
                    f"• {party.get('name', 'Unknown')} ({party.get('role', 'Role')})",
                    self.styles['Normal']
                ))
            elements.append(Spacer(1, 0.2*inch))
        
        # Amounts
        amounts = entities.get('amounts', [])
        if amounts:
            elements.append(Paragraph("<b>Financial Terms</b>", self.styles['Heading3']))
            for amount in amounts[:5]:
                elements.append(Paragraph(
                    f"• {amount.get('amount', 'Amount')}",
                    self.styles['Normal']
                ))
            elements.append(Spacer(1, 0.2*inch))
        
        # Dates
        dates = entities.get('dates', [])
        if dates:
            elements.append(Paragraph("<b>Important Dates</b>", self.styles['Heading3']))
            for date in dates[:5]:
                elements.append(Paragraph(
                    f"• {date.get('date', 'Date')}",
                    self.styles['Normal']
                ))
            elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _create_clause_section(self, results: Dict) -> List:
        """Create clause analysis section"""
        elements = []
        
        elements.append(Paragraph("Clause-by-Clause Analysis", self.styles['CustomHeading']))
        elements.append(Spacer(1, 0.2*inch))
        
        clause_analysis = results.get('clause_analysis', [])
        
        # Show top risky clauses
        risky_clauses = [c for c in clause_analysis if c.get('risks')]
        risky_clauses.sort(key=lambda x: len(x.get('risks', [])), reverse=True)
        
        for clause in risky_clauses[:10]:  # Top 10 risky clauses
            clause_id = clause.get('clause_id', 'Unknown')
            clause_type = clause.get('clause_type', 'Unknown')
            
            elements.append(Paragraph(
                f"<b>Clause {clause_id}: {clause_type}</b>",
                self.styles['Heading4']
            ))
            
            # Show risks
            for risk in clause.get('risks', []):
                severity = risk.get('severity', 'MEDIUM')
                style = f'Risk{severity.title()}' if severity in ['HIGH', 'MEDIUM', 'LOW'] else 'Normal'
                
                elements.append(Paragraph(
                    f"• [{severity}] {risk.get('risk_type', 'Unknown Risk')}",
                    self.styles.get(style, self.styles['Normal'])
                ))
            
            elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _create_recommendations_section(self, results: Dict) -> List:
        """Create recommendations section"""
        elements = []
        
        elements.append(Paragraph("Recommendations", self.styles['CustomHeading']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Negotiation points
        negotiation_points = results.get('negotiation_points', [])
        if negotiation_points:
            elements.append(Paragraph("<b>Negotiation Points</b>", self.styles['Heading3']))
            
            for point in negotiation_points:
                elements.append(Paragraph(f"• {point}", self.styles['Normal']))
                elements.append(Spacer(1, 0.1*inch))
        
        # Compliance notes
        elements.append(Spacer(1, 0.3*inch))
        elements.append(Paragraph("<b>Compliance Notes</b>", self.styles['Heading3']))
        elements.append(Paragraph(
            "This contract should be reviewed for compliance with applicable Indian laws including "
            "the Indian Contract Act, 1872, and other relevant legislation. Consult with a legal "
            "professional for specific compliance requirements.",
            self.styles['Normal']
        ))
        
        return elements
    
    def generate_summary_report(self, analysis_results: Dict, output_filename: str = None) -> str:
        """
        Generate a shorter summary report
        
        Returns:
            Path to generated PDF
        """
        if not output_filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"contract_summary_{timestamp}.pdf"
        
        output_path = self.output_dir / output_filename
        
        doc = SimpleDocTemplate(str(output_path), pagesize=letter)
        story = []
        
        # Title
        story.append(Paragraph("Contract Analysis Summary", self.styles['CustomTitle']))
        story.append(Spacer(1, 0.3*inch))
        
        # Executive summary
        story.extend(self._create_executive_summary(analysis_results))
        story.append(Spacer(1, 0.3*inch))
        
        # Key risks
        story.extend(self._create_risk_section(analysis_results))
        
        doc.build(story)
        
        return str(output_path)
    
    def export_to_json(self, analysis_results: Dict, output_filename: str = None) -> str:
        """
        Export analysis results to JSON
        
        Returns:
            Path to JSON file
        """
        if not output_filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"contract_analysis_{timestamp}.json"
        
        output_path = self.output_dir / output_filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(analysis_results, f, indent=2, ensure_ascii=False)
        
        return str(output_path)
    
    def create_audit_log(self, analysis_results: Dict, user_info: Dict = None) -> str:
        """
        Create audit log entry
        
        Returns:
            Path to audit log file
        """
        timestamp = datetime.now().isoformat()
        audit_dir = Path("data/audit_logs")
        audit_dir.mkdir(parents=True, exist_ok=True)
        
        audit_entry = {
            "timestamp": timestamp,
            "contract_type": analysis_results.get('contract_classification', {}).get('contract_type'),
            "risk_level": analysis_results.get('risk_assessment', {}).get('overall_level'),
            "user_info": user_info or {},
            "analysis_summary": {
                "total_risks": analysis_results.get('risk_assessment', {}).get('total_risks_found', 0),
                "high_priority_risks": len(analysis_results.get('risk_assessment', {}).get('high_priority_risks', [])),
                "clauses_analyzed": len(analysis_results.get('clause_analysis', []))
            }
        }
        
        # Append to audit log
        audit_file = audit_dir / f"audit_log_{datetime.now().strftime('%Y%m')}.json"
        
        logs = []
        if audit_file.exists():
            with open(audit_file, 'r') as f:
                logs = json.load(f)
        
        logs.append(audit_entry)
        
        with open(audit_file, 'w') as f:
            json.dump(logs, f, indent=2)
        
        return str(audit_file)
