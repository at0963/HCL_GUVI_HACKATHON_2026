"""
Contract Analyzer Module
Uses LLM (GPT-4) for deep contract analysis
"""
import os
from typing import Dict, List, Optional
import openai
from config import LLM_PROVIDER, OPENAI_API_KEY, GPT_MODEL


class ContractAnalyzer:
    """Analyze contracts using LLM"""
    
    def __init__(self):
        """Initialize LLM client"""
        self.provider = LLM_PROVIDER
        
        if self.provider == "openai":
            if not OPENAI_API_KEY or OPENAI_API_KEY == "your_openai_api_key_here":
                raise ValueError("Please set OPENAI_API_KEY in .env file")
            openai.api_key = OPENAI_API_KEY
            self.model = GPT_MODEL
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}. Please use 'openai'.")
    
    def classify_contract_type(self, text: str) -> Dict:
        """
        Classify the type of contract
        
        Returns:
            Dict with contract type and confidence
        """
        prompt = f"""Analyze the following contract text and classify it into one of these types:
- Employment Agreement
- Vendor Contract
- Lease Agreement
- Partnership Deed
- Service Contract
- Non-Disclosure Agreement
- General Contract

Provide your answer in this format:
Contract Type: [Type]
Confidence: [High/Medium/Low]
Reasoning: [Brief explanation]

Contract text (first 2000 characters):
{text[:2000]}
"""
        
        response = self._call_llm(prompt)
        
        # Parse response
        lines = response.split('\n')
        contract_type = "General Contract"
        confidence = "Medium"
        reasoning = ""
        
        for line in lines:
            if line.startswith("Contract Type:"):
                contract_type = line.split(":", 1)[1].strip()
            elif line.startswith("Confidence:"):
                confidence = line.split(":", 1)[1].strip()
            elif line.startswith("Reasoning:"):
                reasoning = line.split(":", 1)[1].strip()
        
        return {
            "contract_type": contract_type,
            "confidence": confidence,
            "reasoning": reasoning
        }
    
    def generate_summary(self, text: str, contract_type: str) -> str:
        """
        Generate plain-language summary of contract
        
        Returns:
            Summary text
        """
        prompt = f"""You are a legal assistant helping Indian SME business owners understand contracts.

Analyze this {contract_type} and provide a simple, plain-language summary that a non-lawyer can understand. Focus on:
1. What this contract is about (2-3 sentences)
2. Who are the parties involved
3. Key obligations and rights
4. Important dates and deadlines
5. Payment terms (if any)
6. Termination conditions

Use simple business language. Avoid legal jargon. Be concise and clear.

Contract text:
{text[:4000]}
"""
        
        return self._call_llm(prompt)
    
    def explain_clause(self, clause_text: str, clause_type: str) -> Dict:
        """
        Explain a specific clause in plain language
        
        Returns:
            Dict with explanation and implications
        """
        prompt = f"""You are explaining a legal contract clause to an Indian SME business owner.

Clause Type: {clause_type}
Clause Text: {clause_text}

Provide:
1. Simple Explanation: What does this clause mean in plain English?
2. What It Means For You: Practical implications for the business
3. Key Points to Note: Important things to be aware of

Use simple language. Be practical and helpful.
"""
        
        response = self._call_llm(prompt)
        
        # Parse into sections
        sections = {}
        current_section = None
        current_content = []
        
        for line in response.split('\n'):
            if line.startswith("1. Simple Explanation:"):
                if current_section:
                    sections[current_section] = '\n'.join(current_content)
                current_section = "explanation"
                current_content = []
            elif line.startswith("2. What It Means For You:"):
                if current_section:
                    sections[current_section] = '\n'.join(current_content)
                current_section = "implications"
                current_content = []
            elif line.startswith("3. Key Points to Note:"):
                if current_section:
                    sections[current_section] = '\n'.join(current_content)
                current_section = "key_points"
                current_content = []
            else:
                current_content.append(line)
        
        if current_section:
            sections[current_section] = '\n'.join(current_content)
        
        return sections if sections else {"explanation": response}
    
    def identify_risks(self, text: str, contract_type: str) -> List[Dict]:
        """
        Identify potential legal risks using LLM
        
        Returns:
            List of identified risks
        """
        prompt = f"""You are a legal risk advisor for Indian SMEs.

Analyze this {contract_type} and identify potential legal risks. For each risk, provide:
- Risk Type (e.g., Payment Risk, Liability Risk, Termination Risk)
- Severity (HIGH/MEDIUM/LOW)
- Description (What is the risk?)
- Why It Matters (Impact on business)

Format each risk as:
RISK: [Type]
SEVERITY: [Level]
DESCRIPTION: [Brief description]
IMPACT: [Why it matters]
---

Contract text:
{text[:4000]}
"""
        
        response = self._call_llm(prompt)
        
        # Parse risks
        risks = []
        risk_blocks = response.split('---')
        
        for block in risk_blocks:
            if not block.strip():
                continue
            
            risk = {}
            for line in block.split('\n'):
                if line.startswith("RISK:"):
                    risk["type"] = line.split(":", 1)[1].strip()
                elif line.startswith("SEVERITY:"):
                    risk["severity"] = line.split(":", 1)[1].strip()
                elif line.startswith("DESCRIPTION:"):
                    risk["description"] = line.split(":", 1)[1].strip()
                elif line.startswith("IMPACT:"):
                    risk["impact"] = line.split(":", 1)[1].strip()
            
            if risk:
                risks.append(risk)
        
        return risks
    
    def suggest_alternatives(self, clause_text: str, identified_issues: List[str]) -> List[str]:
        """
        Suggest alternative clause language
        
        Returns:
            List of suggested alternatives
        """
        issues_text = "\n".join([f"- {issue}" for issue in identified_issues])
        
        prompt = f"""You are helping an Indian SME business owner negotiate better contract terms.

Original Clause:
{clause_text}

Identified Issues:
{issues_text}

Suggest 2-3 alternative ways to phrase this clause that would be more favorable to the business owner. 
Each suggestion should:
1. Address the identified issues
2. Be reasonable and fair to both parties
3. Use clear, simple language
4. Be specific and actionable

Format as:
ALTERNATIVE 1:
[Suggested text]

ALTERNATIVE 2:
[Suggested text]
"""
        
        response = self._call_llm(prompt)
        
        # Parse alternatives
        alternatives = []
        current_alt = []
        
        for line in response.split('\n'):
            if line.startswith("ALTERNATIVE"):
                if current_alt:
                    alternatives.append('\n'.join(current_alt))
                current_alt = []
            else:
                current_alt.append(line)
        
        if current_alt:
            alternatives.append('\n'.join(current_alt))
        
        return [alt.strip() for alt in alternatives if alt.strip()]
    
    def check_compliance(self, text: str, contract_type: str) -> Dict:
        """
        Check compliance with Indian laws
        
        Returns:
            Dict with compliance analysis
        """
        prompt = f"""You are a legal compliance advisor for Indian businesses.

Analyze this {contract_type} for compliance with relevant Indian laws. Consider:
- Indian Contract Act, 1872
- Companies Act, 2013 (if applicable)
- Payment of Wages Act, 1936 (for employment)
- Consumer Protection Act, 2019 (if applicable)
- Information Technology Act, 2000 (if applicable)
- Transfer of Property Act, 1882 (for leases)

Provide:
1. Compliance Status: [Compliant/Needs Review/Non-Compliant]
2. Relevant Laws: List applicable Indian laws
3. Compliance Issues: Any potential compliance problems
4. Recommendations: What should be added or changed

Contract text (excerpt):
{text[:3000]}
"""
        
        response = self._call_llm(prompt)
        
        # Parse response
        return {
            "full_analysis": response,
            "timestamp": self._get_timestamp()
        }
    
    def generate_negotiation_points(self, unfavorable_clauses: List[Dict]) -> List[str]:
        """
        Generate negotiation talking points
        
        Returns:
            List of negotiation points
        """
        clauses_text = "\n\n".join([
            f"Clause {i+1}: {clause.get('text', '')[:200]}"
            for i, clause in enumerate(unfavorable_clauses)
        ])
        
        prompt = f"""You are a business negotiation advisor for Indian SMEs.

The following clauses have been identified as potentially unfavorable:

{clauses_text}

Provide 5-7 specific negotiation points that a business owner can use when discussing these clauses. 
Each point should:
1. Be clear and specific
2. Explain what to ask for
3. Include a brief rationale
4. Be reasonable and professional

Format as numbered list.
"""
        
        response = self._call_llm(prompt)
        
        # Extract numbered points
        points = []
        for line in response.split('\n'):
            if line.strip() and (line[0].isdigit() or line.startswith('-')):
                points.append(line.strip())
        
        return points
    
    def _call_llm(self, prompt: str, max_tokens: int = 2000) -> str:
        """
        Call the configured LLM
        
        Returns:
            Response text
        """
        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a legal assistant helping Indian SME business owners understand contracts."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        
        except Exception as e:
            return f"Error calling LLM: {str(e)}"
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
