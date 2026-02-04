"""
Risk Assessor Module
Calculates risk scores for contracts
"""
from typing import Dict, List
from config import RISK_LEVELS, RISK_CATEGORIES


class RiskAssessor:
    """Assess and score contract risks"""
    
    def __init__(self):
        """Initialize risk assessor"""
        self.risk_weights = {
            "penalty_clauses": 1.2,
            "indemnity": 1.5,
            "unilateral_termination": 1.8,
            "arbitration": 1.0,
            "auto_renewal": 1.3,
            "non_compete": 1.4,
            "payment_terms": 1.2,
            "liability": 1.6,
            "confidentiality": 0.8
        }
    
    def assess_contract_risk(self, analyzed_clauses: List[Dict], llm_risks: List[Dict] = None) -> Dict:
        """
        Calculate comprehensive risk score for entire contract
        
        Args:
            analyzed_clauses: List of analyzed clauses from ClauseAnalyzer
            llm_risks: Optional list of risks from LLM analysis
            
        Returns:
            Dict with risk scores and breakdown
        """
        # Initialize risk tracking
        risk_breakdown = {category: [] for category in RISK_CATEGORIES.keys()}
        risk_breakdown["other"] = []
        
        total_risk_score = 0
        clause_count = len(analyzed_clauses)
        
        # Process NLP-detected risks
        for clause in analyzed_clauses:
            clause_risks = clause.get("risks", [])
            
            for risk in clause_risks:
                category = risk.get("category", "other")
                severity = risk.get("severity", "MEDIUM")
                
                # Calculate risk score
                severity_score = RISK_LEVELS[severity]["score"]
                weight = self.risk_weights.get(category, 1.0)
                risk_score = severity_score * weight
                
                total_risk_score += risk_score
                
                # Add to breakdown
                risk_breakdown[category].append({
                    "clause_id": clause.get("clause_id", "Unknown"),
                    "risk_type": risk.get("risk_type", "Unknown Risk"),
                    "severity": severity,
                    "score": risk_score,
                    "description": risk.get("description", "")
                })
        
        # Process LLM-detected risks
        if llm_risks:
            for risk in llm_risks:
                severity = risk.get("severity", "MEDIUM")
                risk_type = risk.get("type", "General Risk")
                
                # Try to categorize
                category = self._categorize_llm_risk(risk_type)
                
                severity_score = RISK_LEVELS.get(severity, RISK_LEVELS["MEDIUM"])["score"]
                weight = self.risk_weights.get(category, 1.0)
                risk_score = severity_score * weight
                
                total_risk_score += risk_score
                
                risk_breakdown[category].append({
                    "clause_id": "LLM Analysis",
                    "risk_type": risk_type,
                    "severity": severity,
                    "score": risk_score,
                    "description": risk.get("description", "")
                })
        
        # Calculate normalized score (0-100)
        if clause_count > 0:
            avg_risk_per_clause = total_risk_score / clause_count
            normalized_score = min(100, avg_risk_per_clause * 20)  # Scale to 0-100
        else:
            normalized_score = 0
        
        # Determine overall risk level
        overall_risk_level = self._determine_risk_level(normalized_score)
        
        # Generate risk summary
        risk_summary = self._generate_risk_summary(risk_breakdown, overall_risk_level)
        
        return {
            "overall_score": round(normalized_score, 2),
            "overall_level": overall_risk_level,
            "total_risks_found": sum(len(risks) for risks in risk_breakdown.values()),
            "risk_breakdown": risk_breakdown,
            "risk_summary": risk_summary,
            "high_priority_risks": self._get_high_priority_risks(risk_breakdown),
            "recommendation": self._get_recommendation(overall_risk_level, normalized_score)
        }
    
    def calculate_clause_risk_score(self, clause: Dict) -> Dict:
        """
        Calculate risk score for a single clause
        
        Returns:
            Dict with clause risk assessment
        """
        risks = clause.get("risks", [])
        
        if not risks:
            return {
                "clause_id": clause.get("clause_id", "Unknown"),
                "risk_score": 0,
                "risk_level": "LOW",
                "risk_count": 0
            }
        
        total_score = 0
        for risk in risks:
            severity = risk.get("severity", "MEDIUM")
            category = risk.get("category", "other")
            
            severity_score = RISK_LEVELS[severity]["score"]
            weight = self.risk_weights.get(category, 1.0)
            total_score += severity_score * weight
        
        # Normalize to 0-10 scale
        normalized_score = min(10, total_score)
        
        # Determine level
        if normalized_score >= 7:
            level = "HIGH"
        elif normalized_score >= 4:
            level = "MEDIUM"
        else:
            level = "LOW"
        
        return {
            "clause_id": clause.get("clause_id", "Unknown"),
            "risk_score": round(normalized_score, 2),
            "risk_level": level,
            "risk_count": len(risks),
            "risks": risks
        }
    
    def identify_critical_risks(self, risk_assessment: Dict) -> List[Dict]:
        """
        Identify the most critical risks that need immediate attention
        
        Returns:
            List of critical risk items
        """
        critical_risks = []
        
        risk_breakdown = risk_assessment.get("risk_breakdown", {})
        
        # Priority categories
        priority_categories = [
            "unilateral_termination",
            "indemnity",
            "liability",
            "non_compete",
            "penalty_clauses"
        ]
        
        for category in priority_categories:
            category_risks = risk_breakdown.get(category, [])
            
            # Get HIGH severity risks
            for risk in category_risks:
                if risk.get("severity") == "HIGH":
                    critical_risks.append({
                        "category": RISK_CATEGORIES.get(category, category),
                        "risk_type": risk.get("risk_type"),
                        "clause_id": risk.get("clause_id"),
                        "description": risk.get("description"),
                        "action_required": self._get_action_for_risk(category, risk)
                    })
        
        return critical_risks
    
    def generate_risk_mitigation_strategies(self, risk_assessment: Dict) -> List[Dict]:
        """
        Generate strategies to mitigate identified risks
        
        Returns:
            List of mitigation strategies
        """
        strategies = []
        
        risk_breakdown = risk_assessment.get("risk_breakdown", {})
        
        strategy_templates = {
            "unilateral_termination": {
                "strategy": "Negotiate for mutual termination rights or require specific cause",
                "actions": [
                    "Request 60-90 days notice period",
                    "Define specific termination causes",
                    "Add termination fee for early exit"
                ]
            },
            "indemnity": {
                "strategy": "Limit indemnification scope and cap liability",
                "actions": [
                    "Cap indemnity at contract value",
                    "Exclude indirect/consequential damages",
                    "Add mutual indemnification clause"
                ]
            },
            "liability": {
                "strategy": "Add liability caps and exclusions",
                "actions": [
                    "Cap total liability at 2x contract value",
                    "Exclude force majeure events",
                    "Define scope of liability clearly"
                ]
            },
            "penalty_clauses": {
                "strategy": "Negotiate reasonable penalty amounts",
                "actions": [
                    "Cap penalties at specific percentage",
                    "Allow cure period before penalties apply",
                    "Make penalties proportionate to breach"
                ]
            },
            "auto_renewal": {
                "strategy": "Add opt-in renewal or longer notice period",
                "actions": [
                    "Change to opt-in renewal",
                    "Require 90-day advance notice",
                    "Allow price renegotiation at renewal"
                ]
            },
            "non_compete": {
                "strategy": "Narrow scope and duration of restrictions",
                "actions": [
                    "Limit to specific geography",
                    "Reduce duration to 1 year",
                    "Define restricted activities specifically"
                ]
            }
        }
        
        for category, risks in risk_breakdown.items():
            if risks and category in strategy_templates:
                template = strategy_templates[category]
                strategies.append({
                    "risk_category": RISK_CATEGORIES.get(category, category),
                    "affected_clauses": len(risks),
                    "strategy": template["strategy"],
                    "actions": template["actions"],
                    "priority": "HIGH" if any(r.get("severity") == "HIGH" for r in risks) else "MEDIUM"
                })
        
        # Sort by priority
        strategies.sort(key=lambda x: 0 if x["priority"] == "HIGH" else 1)
        
        return strategies
    
    def _categorize_llm_risk(self, risk_type: str) -> str:
        """Categorize LLM-identified risk"""
        risk_type_lower = risk_type.lower()
        
        if "payment" in risk_type_lower or "fee" in risk_type_lower:
            return "payment_terms"
        elif "terminat" in risk_type_lower:
            return "unilateral_termination"
        elif "indemnity" in risk_type_lower or "indemnif" in risk_type_lower:
            return "indemnity"
        elif "liability" in risk_type_lower or "liable" in risk_type_lower:
            return "liability"
        elif "penalty" in risk_type_lower or "penalt" in risk_type_lower:
            return "penalty_clauses"
        elif "compete" in risk_type_lower or "non-compete" in risk_type_lower:
            return "non_compete"
        elif "renewal" in risk_type_lower or "renew" in risk_type_lower:
            return "auto_renewal"
        elif "arbitration" in risk_type_lower or "jurisdiction" in risk_type_lower:
            return "arbitration"
        elif "confidential" in risk_type_lower:
            return "confidentiality"
        else:
            return "other"
    
    def _determine_risk_level(self, score: float) -> str:
        """Determine overall risk level from score"""
        if score >= 70:
            return "HIGH"
        elif score >= 40:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _generate_risk_summary(self, risk_breakdown: Dict, overall_level: str) -> str:
        """Generate human-readable risk summary"""
        total_risks = sum(len(risks) for risks in risk_breakdown.values())
        
        if total_risks == 0:
            return "No significant risks identified in this contract."
        
        # Count by severity
        high_count = sum(1 for risks in risk_breakdown.values() for r in risks if r.get("severity") == "HIGH")
        medium_count = sum(1 for risks in risk_breakdown.values() for r in risks if r.get("severity") == "MEDIUM")
        low_count = sum(1 for risks in risk_breakdown.values() for r in risks if r.get("severity") == "LOW")
        
        # Find top risk categories
        top_categories = sorted(
            [(cat, len(risks)) for cat, risks in risk_breakdown.items() if risks],
            key=lambda x: x[1],
            reverse=True
        )[:3]
        
        summary = f"Overall Risk Level: {overall_level}\n\n"
        summary += f"Total Risks Identified: {total_risks}\n"
        summary += f"- High Severity: {high_count}\n"
        summary += f"- Medium Severity: {medium_count}\n"
        summary += f"- Low Severity: {low_count}\n\n"
        
        if top_categories:
            summary += "Main Risk Areas:\n"
            for cat, count in top_categories:
                category_name = RISK_CATEGORIES.get(cat, cat.replace('_', ' ').title())
                summary += f"- {category_name}: {count} issue(s)\n"
        
        return summary
    
    def _get_high_priority_risks(self, risk_breakdown: Dict) -> List[Dict]:
        """Extract high-priority risks"""
        high_priority = []
        
        for category, risks in risk_breakdown.items():
            for risk in risks:
                if risk.get("severity") == "HIGH":
                    high_priority.append({
                        "category": RISK_CATEGORIES.get(category, category),
                        "risk_type": risk.get("risk_type"),
                        "clause_id": risk.get("clause_id"),
                        "description": risk.get("description")
                    })
        
        return high_priority
    
    def _get_recommendation(self, risk_level: str, score: float) -> str:
        """Get recommendation based on risk level"""
        if risk_level == "HIGH":
            return (
                "⚠️ HIGH RISK: This contract contains significant risks. "
                "We strongly recommend consulting with a legal professional before signing. "
                "Consider negotiating the high-risk clauses identified."
            )
        elif risk_level == "MEDIUM":
            return (
                "⚡ MEDIUM RISK: This contract has some concerning clauses. "
                "Review the identified risks carefully and consider negotiating terms. "
                "Legal consultation is recommended for complex issues."
            )
        else:
            return (
                "✅ LOW RISK: This contract appears relatively balanced. "
                "Review the summary and specific clauses, but major concerns are minimal. "
                "Standard business review should be sufficient."
            )
    
    def _get_action_for_risk(self, category: str, risk: Dict) -> str:
        """Get recommended action for specific risk"""
        actions = {
            "unilateral_termination": "Negotiate for mutual termination rights or require cause",
            "indemnity": "Request liability cap and scope limitation",
            "liability": "Add maximum liability cap",
            "penalty_clauses": "Negotiate lower penalty amounts",
            "non_compete": "Narrow geographic and time scope",
            "auto_renewal": "Request opt-in renewal or longer notice",
            "payment_terms": "Negotiate milestone-based payments"
        }
        
        return actions.get(category, "Review and negotiate this clause")
