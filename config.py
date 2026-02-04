"""
Configuration file for Legal Assistant
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Project Paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
AUDIT_DIR = DATA_DIR / "audit_logs"
TEMPLATES_DIR = BASE_DIR / "templates"
PROMPTS_DIR = BASE_DIR / "prompts"
UPLOADS_DIR = DATA_DIR / "uploads"

# Create directories if they don't exist
for directory in [DATA_DIR, AUDIT_DIR, TEMPLATES_DIR, PROMPTS_DIR, UPLOADS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# LLM Configuration
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "anthropic")  # "anthropic" or "openai"
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
CLAUDE_MODEL = "claude-3-5-sonnet-20241022"
GPT_MODEL = "gpt-4o"  # Using GPT-4o (faster and more capable)

# Contract Types
CONTRACT_TYPES = [
    "Employment Agreement",
    "Vendor Contract",
    "Lease Agreement",
    "Partnership Deed",
    "Service Contract",
    "Non-Disclosure Agreement",
    "General Contract"
]

# Risk Categories
RISK_CATEGORIES = {
    "penalty_clauses": "Penalty Clauses",
    "indemnity": "Indemnity Clauses",
    "unilateral_termination": "Unilateral Termination",
    "arbitration": "Arbitration & Jurisdiction",
    "auto_renewal": "Auto-Renewal & Lock-in",
    "non_compete": "Non-compete & IP Transfer",
    "payment_terms": "Payment Terms",
    "liability": "Liability Limitations",
    "confidentiality": "Confidentiality Obligations"
}

# Risk Levels
RISK_LEVELS = {
    "LOW": {"score": 1, "color": "green", "label": "Low Risk"},
    "MEDIUM": {"score": 2, "color": "orange", "label": "Medium Risk"},
    "HIGH": {"score": 3, "color": "red", "label": "High Risk"}
}

# Supported Languages
SUPPORTED_LANGUAGES = ["English", "Hindi", "Mixed"]

# Entity Types for NER
ENTITY_TYPES = [
    "PARTY_NAME",
    "DATE",
    "AMOUNT",
    "DURATION",
    "JURISDICTION",
    "LIABILITY",
    "DELIVERABLE",
    "OBLIGATION",
    "RIGHT",
    "PROHIBITION"
]

# Clause Types
CLAUSE_TYPES = [
    "Payment Terms",
    "Termination",
    "Indemnity",
    "Confidentiality",
    "Intellectual Property",
    "Liability",
    "Dispute Resolution",
    "Force Majeure",
    "Warranties",
    "General Provisions"
]

# Indian Laws for Compliance (Reference)
INDIAN_LAWS_REFERENCE = [
    "Indian Contract Act, 1872",
    "Companies Act, 2013",
    "Shops and Establishments Act",
    "Payment of Wages Act, 1936",
    "Consumer Protection Act, 2019",
    "Information Technology Act, 2000",
    "Transfer of Property Act, 1882",
    "Partnership Act, 1932"
]

# Streamlit Configuration
PAGE_TITLE = "Legal Assistant for Indian SMEs"
PAGE_ICON = "⚖️"
LAYOUT = "wide"

# File Upload Settings
MAX_FILE_SIZE_MB = 10
ALLOWED_EXTENSIONS = [".pdf", ".docx", ".doc", ".txt"]
