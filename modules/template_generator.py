"""
Template Generator Module
Generates standardized contract templates for Indian SMEs
"""
from typing import Dict, List, Optional
from datetime import datetime
import json


class TemplateGenerator:
    """Generate standard contract templates"""
    
    def __init__(self):
        """Initialize template generator"""
        self.templates = self._load_template_definitions()
    
    def _load_template_definitions(self) -> Dict:
        """Load template definitions"""
        # Define standard templates for Indian SMEs
        return {
            "employment_agreement": {
                "name": "Employment Agreement",
                "description": """Standard employment contract for hiring employees in India.
• Covers job role, salary, working hours, and benefits
• Includes termination clause with notice period
• Contains confidentiality and non-compete provisions
• Compliant with Indian Contract Act, 1872 and Payment of Wages Act, 1936
• Suitable for permanent, full-time employees""",
                "sections": [
                    "Parties", "Position and Duties", "Compensation", "Working Hours",
                    "Benefits", "Leave Policy", "Termination", "Confidentiality",
                    "Non-Compete", "Dispute Resolution"
                ]
            },
            "vendor_contract": {
                "name": "Vendor/Supplier Contract",
                "description": """Agreement for goods or services procurement from vendors/suppliers.
• Defines scope of products/services to be supplied
• Specifies pricing, payment terms, and delivery schedules
• Includes quality standards and warranty provisions
• Contains liability and indemnification clauses
• Ideal for regular business-to-business purchases""",
                "sections": [
                    "Parties", "Scope of Work", "Pricing and Payment", "Delivery Terms",
                    "Quality Standards", "Warranties", "Liability", "Termination",
                    "Dispute Resolution"
                ]
            },
            "service_contract": {
                "name": "Service Agreement",
                "description": """Professional services contract for consultants, freelancers, or agencies.
• Clearly defines services, deliverables, and timelines
• Covers fee structure and payment milestones
• Addresses intellectual property ownership
• Includes confidentiality and non-disclosure terms
• Perfect for IT services, consulting, marketing, etc.""",
                "sections": [
                    "Parties", "Services Description", "Deliverables", "Timeline",
                    "Fees and Payment", "Intellectual Property", "Confidentiality",
                    "Termination", "Liability", "Dispute Resolution"
                ]
            },
            "lease_agreement": {
                "name": "Commercial Lease Agreement",
                "description": """Office/commercial space rental agreement for business premises.
• Covers rent amount, deposit, and lease duration
• Defines maintenance responsibilities and permitted use
• Includes renewal and termination conditions
• Addresses security deposit and rent escalation
• Suitable for offices, shops, warehouses, etc.""",
                "sections": [
                    "Parties", "Property Description", "Lease Term", "Rent and Deposit",
                    "Maintenance", "Use of Premises", "Termination", "Renewal",
                    "Dispute Resolution"
                ]
            },
            "partnership_deed": {
                "name": "Partnership Deed",
                "description": """Agreement for establishing a business partnership between two or more parties.
• Defines capital contribution from each partner
• Specifies profit and loss sharing ratio
• Covers roles, responsibilities, and decision-making authority
• Includes provisions for admission/retirement of partners
• Essential for LLPs and partnership firms""",
                "sections": [
                    "Partners", "Business Name and Nature", "Capital Contribution",
                    "Profit Sharing", "Management", "Decision Making",
                    "Addition/Removal of Partners", "Dissolution", "Dispute Resolution"
                ]
            },
            "nda": {
                "name": "Non-Disclosure Agreement",
                "description": """Confidentiality agreement to protect sensitive business information.
• Defines what constitutes confidential information
• Establishes obligations for both parties
• Specifies duration of confidentiality obligations
• Includes remedies for breach of confidentiality
• Use before sharing business plans, trade secrets, or proprietary data""",
                "sections": [
                    "Parties", "Definition of Confidential Information", "Obligations",
                    "Permitted Disclosures", "Term", "Return of Information",
                    "Remedies", "Dispute Resolution"
                ]
            }
        }
    
    def generate_template(self, template_type: str, custom_fields: Dict = None) -> str:
        """
        Generate a contract template
        
        Args:
            template_type: Type of template to generate
            custom_fields: Optional custom field values
            
        Returns:
            Generated template text
        """
        if template_type not in self.templates:
            return f"Template type '{template_type}' not found."
        
        template_info = self.templates[template_type]
        
        # Generate based on template type
        if template_type == "employment_agreement":
            return self._generate_employment_template(custom_fields)
        elif template_type == "vendor_contract":
            return self._generate_vendor_template(custom_fields)
        elif template_type == "service_contract":
            return self._generate_service_template(custom_fields)
        elif template_type == "lease_agreement":
            return self._generate_lease_template(custom_fields)
        elif template_type == "partnership_deed":
            return self._generate_partnership_template(custom_fields)
        elif template_type == "nda":
            return self._generate_nda_template(custom_fields)
        else:
            return self._generate_generic_template(template_info, custom_fields)
    
    def _generate_employment_template(self, fields: Dict = None) -> str:
        """Generate employment agreement template"""
        fields = fields or {}
        
        template = f"""EMPLOYMENT AGREEMENT

This Employment Agreement ("Agreement") is entered into on {fields.get('date', '[DATE]')} 
between:

1. {fields.get('employer_name', '[EMPLOYER NAME]')}, a company incorporated under the Companies Act, 2013, 
   having its registered office at {fields.get('employer_address', '[EMPLOYER ADDRESS]')} 
   (hereinafter referred to as the "Employer")

AND

2. {fields.get('employee_name', '[EMPLOYEE NAME]')}, residing at {fields.get('employee_address', '[EMPLOYEE ADDRESS]')} 
   (hereinafter referred to as the "Employee")

1. POSITION AND DUTIES
1.1 The Employee is appointed to the position of {fields.get('position', '[POSITION]')}.
1.2 The Employee shall report to {fields.get('reporting_to', '[REPORTING MANAGER]')}.
1.3 The Employee agrees to perform duties assigned and work in the best interests of the Employer.

2. COMPENSATION
2.1 The Employee shall receive a monthly salary of INR {fields.get('salary', '[AMOUNT]')}.
2.2 Payment shall be made on or before the {fields.get('payment_day', '[DAY]')} of each month.
2.3 Salary is subject to applicable tax deductions as per Indian law.

3. WORKING HOURS
3.1 Standard working hours are {fields.get('working_hours', '[HOURS]')} per day, {fields.get('working_days', '[DAYS]')} days per week.
3.2 The Employee may be required to work additional hours as per business requirements.

4. LEAVE POLICY
4.1 The Employee is entitled to annual leave as per company policy.
4.2 Leave must be applied for in advance and approved by the reporting manager.

5. PROBATION PERIOD
5.1 The Employee shall be on probation for {fields.get('probation_period', '3 months')}.
5.2 During probation, either party may terminate with {fields.get('probation_notice', '15 days')} notice.

6. TERMINATION
6.1 After probation, either party may terminate with {fields.get('notice_period', '30 days')} written notice.
6.2 The Employer may terminate immediately for cause including misconduct, breach of contract, or negligence.
6.3 Upon termination, all company property must be returned.

7. CONFIDENTIALITY
7.1 The Employee shall maintain confidentiality of all company information during and after employment.
7.2 Confidential information includes but is not limited to business plans, client data, and trade secrets.
7.3 Breach of confidentiality may result in legal action.

8. NON-COMPETE (if applicable)
8.1 During employment and for {fields.get('non_compete_period', '1 year')} after, the Employee shall not engage 
    in competing business within {fields.get('non_compete_area', '[GEOGRAPHIC AREA]')}.

9. GOVERNING LAW
9.1 This Agreement shall be governed by the laws of India.
9.2 Disputes shall be subject to the jurisdiction of {fields.get('jurisdiction', '[CITY]')} courts.

10. ENTIRE AGREEMENT
This Agreement constitutes the entire agreement between the parties.


EMPLOYER:                                    EMPLOYEE:

Name: {fields.get('employer_name', '[NAME]')}               Name: {fields.get('employee_name', '[NAME]')}
Signature: _________________              Signature: _________________
Date: ______________________              Date: ______________________
"""
        return template
    
    def _generate_vendor_template(self, fields: Dict = None) -> str:
        """Generate vendor contract template"""
        fields = fields or {}
        
        template = f"""VENDOR/SUPPLIER AGREEMENT

This Agreement is made on {fields.get('date', '[DATE]')} between:

BUYER: {fields.get('buyer_name', '[BUYER NAME]')}
Address: {fields.get('buyer_address', '[BUYER ADDRESS]')}

VENDOR: {fields.get('vendor_name', '[VENDOR NAME]')}
Address: {fields.get('vendor_address', '[VENDOR ADDRESS]')}

1. SCOPE OF SUPPLY
The Vendor agrees to supply {fields.get('products_services', '[PRODUCTS/SERVICES]')} 
as per specifications agreed upon.

2. PRICING
2.1 Price: INR {fields.get('price', '[AMOUNT]')} per {fields.get('unit', '[UNIT]')}
2.2 Prices are exclusive of applicable taxes unless stated otherwise.
2.3 Price revisions require 30 days advance written notice.

3. PAYMENT TERMS
3.1 Payment Terms: {fields.get('payment_terms', 'Net 30 days from invoice date')}
3.2 Payment method: {fields.get('payment_method', 'Bank transfer')}
3.3 Late payments shall attract interest at {fields.get('late_payment_rate', '12% per annum')}.

4. DELIVERY
4.1 Delivery Timeline: {fields.get('delivery_time', '[TIMELINE]')}
4.2 Delivery Location: {fields.get('delivery_location', '[LOCATION]')}
4.3 Risk passes to Buyer upon delivery and acceptance.

5. QUALITY STANDARDS
5.1 All supplies must meet agreed specifications and quality standards.
5.2 Buyer reserves the right to inspect and reject non-conforming goods.
5.3 Defective goods shall be replaced at Vendor's cost within {fields.get('replacement_time', '7 days')}.

6. WARRANTIES
6.1 Vendor warrants that supplies are free from defects.
6.2 Warranty period: {fields.get('warranty_period', '12 months')} from delivery.

7. LIABILITY
7.1 Vendor's total liability is limited to the value of the defective goods/services.
7.2 Neither party is liable for indirect or consequential damages.

8. TERM AND TERMINATION
8.1 Term: {fields.get('contract_term', '1 year')} from the date of this Agreement.
8.2 Either party may terminate with {fields.get('termination_notice', '30 days')} written notice.
8.3 Immediate termination allowed for material breach not cured within 15 days.

9. GOVERNING LAW
Governed by Indian law. Jurisdiction: {fields.get('jurisdiction', '[CITY]')} courts.


BUYER:                                    VENDOR:
Signature: _________________              Signature: _________________
Date: ______________________              Date: ______________________
"""
        return template
    
    def _generate_service_template(self, fields: Dict = None) -> str:
        """Generate service agreement template"""
        fields = fields or {}
        
        template = f"""SERVICE AGREEMENT

Date: {fields.get('date', '[DATE]')}

CLIENT: {fields.get('client_name', '[CLIENT NAME]')}
SERVICE PROVIDER: {fields.get('provider_name', '[PROVIDER NAME]')}

1. SERVICES
The Service Provider shall provide the following services:
{fields.get('services_description', '[DETAILED DESCRIPTION OF SERVICES]')}

2. DELIVERABLES
Expected deliverables include:
{fields.get('deliverables', '[LIST OF DELIVERABLES]')}

3. TIMELINE
Project Start: {fields.get('start_date', '[DATE]')}
Project End: {fields.get('end_date', '[DATE]')}
Key Milestones: {fields.get('milestones', '[MILESTONES]')}

4. FEES AND PAYMENT
4.1 Total Fee: INR {fields.get('total_fee', '[AMOUNT]')}
4.2 Payment Schedule:
    - {fields.get('payment_schedule', 'Milestone-based or monthly')}
4.3 Payment within {fields.get('payment_days', '15 days')} of invoice.

5. INTELLECTUAL PROPERTY
5.1 All IP created shall belong to {fields.get('ip_owner', 'Client')}.
5.2 Provider retains rights to pre-existing IP and general methodologies.

6. CONFIDENTIALITY
Both parties agree to maintain confidentiality of shared information.

7. LIABILITY
Maximum liability limited to {fields.get('liability_cap', 'total fees paid')}.

8. TERMINATION
Either party may terminate with {fields.get('termination_notice', '30 days')} notice.

9. GOVERNING LAW
Indian law. Jurisdiction: {fields.get('jurisdiction', '[CITY]')}.


CLIENT:                                    SERVICE PROVIDER:
Signature: _________________              Signature: _________________
"""
        return template
    
    def _generate_lease_template(self, fields: Dict = None) -> str:
        """Generate lease agreement template"""
        fields = fields or {}
        
        return f"""COMMERCIAL LEASE AGREEMENT

LANDLORD: {fields.get('landlord_name', '[NAME]')}
TENANT: {fields.get('tenant_name', '[NAME]')}

1. PROPERTY
Address: {fields.get('property_address', '[ADDRESS]')}
Area: {fields.get('property_area', '[AREA]')}

2. LEASE TERM
Period: {fields.get('lease_period', '[PERIOD]')} 
From: {fields.get('start_date', '[DATE]')}

3. RENT
Monthly Rent: INR {fields.get('rent_amount', '[AMOUNT]')}
Security Deposit: INR {fields.get('deposit_amount', '[AMOUNT]')}

4. PAYMENT
Rent due on {fields.get('rent_day', '[DAY]')} of each month.

5. USE OF PREMISES
For: {fields.get('permitted_use', '[PURPOSE]')} only.

6. MAINTENANCE
Tenant responsible for: {fields.get('tenant_maintenance', '[ITEMS]')}
Landlord responsible for: {fields.get('landlord_maintenance', '[ITEMS]')}

7. TERMINATION
Notice period: {fields.get('notice_period', '2 months')}

LANDLORD:                    TENANT:
Signature: _____________     Signature: _____________
"""
    
    def _generate_partnership_template(self, fields: Dict = None) -> str:
        """Generate partnership deed template"""
        fields = fields or {}
        
        return f"""PARTNERSHIP DEED

Partners:
{fields.get('partners', '[PARTNER NAMES]')}

1. BUSINESS
Name: {fields.get('business_name', '[NAME]')}
Nature: {fields.get('business_nature', '[NATURE]')}

2. CAPITAL
{fields.get('capital_details', '[CAPITAL CONTRIBUTION BY EACH PARTNER]')}

3. PROFIT SHARING
{fields.get('profit_sharing', '[PROFIT SHARING RATIO]')}

4. MANAGEMENT
{fields.get('management_structure', '[MANAGEMENT DETAILS]')}

5. DISSOLUTION
{fields.get('dissolution_terms', '[DISSOLUTION TERMS]')}
"""
    
    def _generate_nda_template(self, fields: Dict = None) -> str:
        """Generate NDA template"""
        fields = fields or {}
        
        return f"""NON-DISCLOSURE AGREEMENT

DISCLOSING PARTY: {fields.get('disclosing_party', '[NAME]')}
RECEIVING PARTY: {fields.get('receiving_party', '[NAME]')}

1. CONFIDENTIAL INFORMATION
All information shared is confidential.

2. OBLIGATIONS
Receiving Party shall not disclose or use confidential information.

3. TERM
Duration: {fields.get('term', '2 years')} from date of disclosure.

4. EXCLUSIONS
Does not include publicly available information.

SIGNATURES:
_________________    _________________
"""
    
    def _generate_generic_template(self, template_info: Dict, fields: Dict = None) -> str:
        """Generate generic template structure"""
        template = f"""{template_info['name'].upper()}

Description: {template_info['description']}

SECTIONS:
"""
        for section in template_info['sections']:
            template += f"\n{section}:\n[To be filled]\n"
        
        return template
    
    def list_available_templates(self) -> List[Dict]:
        """
        List all available templates
        
        Returns:
            List of template info dictionaries
        """
        return [
            {
                "id": key,
                "name": value["name"],
                "description": value["description"],
                "sections": len(value["sections"])
            }
            for key, value in self.templates.items()
        ]
    
    def get_template_fields(self, template_type: str) -> List[str]:
        """
        Get required fields for a template
        
        Returns:
            List of field names
        """
        # Define required fields for each template type
        template_fields = {
            "employment_agreement": [
                "employer_name", "employer_address", "employee_name", "employee_address",
                "position", "salary", "working_hours", "notice_period", "jurisdiction"
            ],
            "vendor_contract": [
                "buyer_name", "vendor_name", "products_services", "price",
                "payment_terms", "delivery_time", "contract_term"
            ],
            "service_contract": [
                "client_name", "provider_name", "services_description", "total_fee",
                "start_date", "end_date", "deliverables"
            ],
            "lease_agreement": [
                "landlord_name", "tenant_name", "property_address", "rent_amount",
                "deposit_amount", "lease_period", "start_date"
            ],
            "partnership_deed": [
                "partners", "business_name", "business_nature", "capital_details",
                "profit_sharing"
            ],
            "nda": [
                "disclosing_party", "receiving_party", "term"
            ]
        }
        
        return template_fields.get(template_type, [])
