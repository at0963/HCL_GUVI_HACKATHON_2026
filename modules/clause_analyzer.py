"""
Clause Analyzer Module
Analyzes and classifies contract clauses
"""
import re
from typing import List, Dict, Optional
from modules.nlp_processor import NLPProcessor


class ClauseAnalyzer:
    """Analyze contract clauses in detail"""
    
    def __init__(self, nlp=None):
        """Initialize clause analyzer"""
        self.nlp_processor = NLPProcessor(nlp)
        
        # Define clause type keywords
        self.clause_keywords = {
            "Payment Terms": [
                "payment", "fee", "compensation", "remuneration", "salary",
                "invoice", "due", "price", "cost", "charge"
            ],
            "Termination": [
                "terminate", "termination", "cancel", "cancellation", "end",
                "expire", "cessation", "dissolve", "dissolution"
            ],
            "Indemnity": [
                "indemnify", "indemnification", "hold harmless", "defend",
                "protect", "compensate for loss"
            ],
            "Confidentiality": [
                "confidential", "secret", "proprietary", "non-disclosure",
                "nda", "confidentiality"
            ],
            "Intellectual Property": [
                "intellectual property", "copyright", "patent", "trademark",
                "ip rights", "ownership", "proprietary rights"
            ],
            "Liability": [
                "liability", "liable", "responsible", "responsibility",
                "damages", "accountable"
            ],
            "Dispute Resolution": [
                "dispute", "arbitration", "mediation", "litigation",
                "court", "jurisdiction", "governing law"
            ],
            "Force Majeure": [
                "force majeure", "act of god", "unforeseeable",
                "beyond control", "natural disaster"
            ],
            "Warranties": [
                "warrant", "warranty", "guarantee", "represent",
                "representation", "assure", "certification"
            ],
            "Non-compete": [
                "non-compete", "non-competition", "restrictive covenant",
                "compete", "competitive"
            ],
            "Auto-Renewal": [
                "auto-renew", "automatic renewal", "automatically renew",
                "extend", "extension"
            ],
            "Lock-in Period": [
                "lock-in", "lock in period", "minimum term",
                "committed period"
            ]
        }
    
    def analyze_clauses(self, text: str) -> List[Dict]:
        """
        Analyze all clauses in contract
        
        Returns:
            List of clause analysis dictionaries
        """
        # Extract clauses
        clauses = self.nlp_processor.extract_clauses(text)
        
        analyzed_clauses = []
        
        for i, clause in enumerate(clauses):
            analysis = self.analyze_single_clause(clause["text"], i + 1)
            analysis["clause_id"] = clause.get("clause_id", f"C{i+1}")
            analysis["original_text"] = clause["text"]
            analyzed_clauses.append(analysis)
        
        return analyzed_clauses
    
    def analyze_single_clause(self, clause_text: str, clause_number: int) -> Dict:
        """
        Analyze a single clause
        
        Returns:
            Dictionary with clause analysis
        """
        clause_lower = clause_text.lower()
        
        # Classify clause type
        clause_type = self._classify_clause_type(clause_text)
        
        # Extract obligations
        obligations = self._extract_clause_obligations(clause_text)
        
        # Detect risks
        risks = self._detect_clause_risks(clause_text, clause_type)
        
        # Check for ambiguities
        ambiguities = self.nlp_processor.detect_ambiguities(clause_text)
        
        # Identify key terms
        key_terms = self.nlp_processor.extract_key_terms(clause_text, top_n=5)
        
        return {
            "clause_number": clause_number,
            "clause_type": clause_type,
            "obligations": obligations,
            "risks": risks,
            "ambiguities": ambiguities,
            "key_terms": [term[0] for term in key_terms],
            "word_count": len(clause_text.split())
        }
    
    def _classify_clause_type(self, clause_text: str) -> str:
        """Classify clause type based on keywords"""
        clause_lower = clause_text.lower()
        
        # Count matches for each clause type
        type_scores = {}
        for clause_type, keywords in self.clause_keywords.items():
            score = sum(1 for keyword in keywords if keyword in clause_lower)
            if score > 0:
                type_scores[clause_type] = score
        
        if type_scores:
            # Return type with highest score
            return max(type_scores.items(), key=lambda x: x[1])[0]
        
        return "General Provisions"
    
    def _extract_clause_obligations(self, clause_text: str) -> Dict:
        """Extract obligations from clause"""
        return self.nlp_processor.extract_obligations(clause_text)
    
    def _detect_clause_risks(self, clause_text: str, clause_type: str) -> List[Dict]:
        """
        Detect potential risks in clause
        
        Returns:
            List of risk dictionaries
        """
        risks = []
        clause_lower = clause_text.lower()
        
        # Risk patterns
        risk_patterns = {
            "Unlimited Liability": {
                "pattern": r'\b(unlimited|without limit|no cap|uncapped)\s+(?:liability|damages|obligation)',
                "severity": "HIGH",
                "category": "liability"
            },
            "Harsh Penalties": {
                "pattern": r'\b(penalty|liquidated damages|forfeit|fine)\b',
                "severity": "MEDIUM",
                "category": "penalty_clauses"
            },
            "Unilateral Termination": {
                "pattern": r'\b(?:may|can|shall)\s+terminate\s+(?:at|with)\s+(?:any\s+time|will|discretion)',
                "severity": "HIGH",
                "category": "unilateral_termination"
            },
            "Auto-Renewal": {
                "pattern": r'\b(?:automatically|auto)\s+(?:renew|extend|continue)',
                "severity": "MEDIUM",
                "category": "auto_renewal"
            },
            "Broad Indemnity": {
                "pattern": r'\bindemnify\s+(?:and\s+hold\s+harmless|from\s+(?:any|all))',
                "severity": "HIGH",
                "category": "indemnity"
            },
            "IP Transfer": {
                "pattern": r'\b(?:transfer|assign|convey)\s+(?:all|any)?\s*(?:intellectual\s+property|ip|copyright|patent)',
                "severity": "HIGH",
                "category": "non_compete"
            },
            "Non-Compete": {
                "pattern": r'\bnon-compete|restrictive\s+covenant|not\s+compete',
                "severity": "MEDIUM",
                "category": "non_compete"
            },
            "Late Payment": {
                "pattern": r'\b(?:interest|penalty|charge)\s+(?:on|for)\s+(?:late|delayed|overdue)\s+payment',
                "severity": "MEDIUM",
                "category": "payment_terms"
            },
            "Jurisdiction Issues": {
                "pattern": r'\b(?:exclusive|sole)\s+jurisdiction',
                "severity": "MEDIUM",
                "category": "arbitration"
            },
            "Liability Limitation": {
                "pattern": r'\b(?:not|no|limited)\s+(?:liable|responsibility|obligation)',
                "severity": "MEDIUM",
                "category": "liability"
            }
        }
        
        for risk_name, risk_info in risk_patterns.items():
            if re.search(risk_info["pattern"], clause_lower):
                risks.append({
                    "risk_type": risk_name,
                    "severity": risk_info["severity"],
                    "category": risk_info["category"],
                    "description": f"Clause contains {risk_name.lower()} language"
                })
        
        # Check clause type specific risks
        if clause_type == "Termination":
            if "without cause" in clause_lower or "at will" in clause_lower:
                risks.append({
                    "risk_type": "Termination Without Cause",
                    "severity": "HIGH",
                    "category": "unilateral_termination",
                    "description": "Contract can be terminated without specific cause"
                })
        
        if clause_type == "Payment Terms":
            if "advance" in clause_lower or "upfront" in clause_lower:
                risks.append({
                    "risk_type": "Advance Payment",
                    "severity": "MEDIUM",
                    "category": "payment_terms",
                    "description": "Requires advance or upfront payment"
                })
        
        return risks
    
    def identify_unfavorable_clauses(self, analyzed_clauses: List[Dict]) -> List[Dict]:
        """
        Identify potentially unfavorable clauses
        
        Returns:
            List of unfavorable clauses with reasons
        """
        unfavorable = []
        
        for clause in analyzed_clauses:
            # Check if clause has high-severity risks
            high_risks = [r for r in clause.get("risks", []) if r["severity"] == "HIGH"]
            
            if high_risks:
                unfavorable.append({
                    "clause_id": clause["clause_id"],
                    "clause_type": clause["clause_type"],
                    "reasons": [r["risk_type"] for r in high_risks],
                    "text": clause.get("original_text", "")[:200] + "...",
                    "severity": "HIGH"
                })
            
            # Check for multiple ambiguities
            elif len(clause.get("ambiguities", [])) > 2:
                unfavorable.append({
                    "clause_id": clause["clause_id"],
                    "clause_type": clause["clause_type"],
                    "reasons": ["Multiple Ambiguous Terms"],
                    "text": clause.get("original_text", "")[:200] + "...",
                    "severity": "MEDIUM"
                })
        
        return unfavorable
    
    def suggest_alternatives(self, clause_text: str, clause_type: str, risks: List[Dict]) -> List[str]:
        """
        Suggest alternative clause language
        
        Returns:
            List of suggested alternatives
        """
        suggestions = []
        
        # Generic suggestions based on clause type
        if clause_type == "Termination":
            suggestions.append(
                "Consider adding specific termination conditions and notice periods "
                "(e.g., '30 days written notice with specific cause')"
            )
        
        if clause_type == "Liability":
            suggestions.append(
                "Consider capping liability to a reasonable amount "
                "(e.g., 'aggregate liability shall not exceed contract value')"
            )
        
        if clause_type == "Payment Terms":
            suggestions.append(
                "Consider milestone-based payments rather than full advance payment"
            )
        
        if clause_type == "Indemnity":
            suggestions.append(
                "Consider limiting indemnity to direct damages arising from specific breaches"
            )
        
        # Risk-specific suggestions
        for risk in risks:
            if risk["risk_type"] == "Unlimited Liability":
                suggestions.append(
                    "Replace 'unlimited' with a specific cap, such as '2x the contract value'"
                )
            
            if risk["risk_type"] == "Auto-Renewal":
                suggestions.append(
                    "Add requirement for written confirmation 60-90 days before renewal"
                )
            
            if risk["risk_type"] == "Non-Compete":
                suggestions.append(
                    "Limit non-compete to specific geography and reasonable time period (1-2 years)"
                )
        
        return suggestions if suggestions else ["No specific alternatives at this time"]
    
    def compare_with_standard(self, clause_text: str, clause_type: str) -> Dict:
        """
        Compare clause with standard templates
        
        Returns:
            Comparison result with similarity score
        """
        # This would compare with actual templates in production
        # For now, return a basic comparison structure
        
        return {
            "clause_type": clause_type,
            "similarity_score": 0.0,  # Would calculate actual similarity
            "deviations": [],
            "compliance_status": "To be reviewed"
        }
