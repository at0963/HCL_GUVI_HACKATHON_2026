"""
Legal Assistant for Indian SMEs
Main Streamlit Application - Redesigned UI
"""
import streamlit as st
import os
from pathlib import Path
from datetime import datetime
import json

import config

st.set_page_config(
    page_title="Legal Assistant | Indian SMEs",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

@st.cache_resource
def load_spacy():
    import spacy
    return spacy.load("en_core_web_sm")

@st.cache_resource
def load_processors():
    from modules.document_processor import DocumentProcessor
    from modules.nlp_processor import NLPProcessor
    from modules.entity_extractor import EntityExtractor
    from modules.clause_analyzer import ClauseAnalyzer
    from modules.contract_analyzer import ContractAnalyzer
    from modules.risk_assessor import RiskAssessor
    from modules.multilingual_handler import MultilingualHandler
    from modules.template_generator import TemplateGenerator
    from modules.report_generator import ReportGenerator

    nlp = load_spacy()

    return {
        "doc": DocumentProcessor(),
        "nlp": NLPProcessor(nlp),
        "entity": EntityExtractor(nlp),
        "clause": ClauseAnalyzer(nlp),
        "contract": ContractAnalyzer(),
        "risk": RiskAssessor(),
        "lang": MultilingualHandler(),
        "template": TemplateGenerator(),
        "report": ReportGenerator(),
    }

processors = load_processors()

# Enhanced Custom CSS

# Build CSS with proper formatting
css_code = f"""
<style>
    /* Hide Streamlit Branding and Toolbar */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    .stDeployButton {{display: none;}}
    
    /* Remove all top spacing */
    .main > div:first-child {{
        padding-top: 0rem !important;
    }}
    
    div[data-testid="stVerticalBlock"] > div:first-child {{
        padding-top: 0rem !important;
    }}
    
    section.main > div {{
        padding-top: 0rem !important;
    }}
    
    section[data-testid="stAppViewContainer"] {{
        padding-top: 0rem !important;
    }}
    
    div[data-testid="stToolbar"] {{
        display: none !important;
    }}
    
    /* Global Styles */
    .main {{
        padding: 0rem !important;
        padding-top: 0rem !important;
        margin-top: 0rem !important;
        background: #ffffff;
    }}
    
    .block-container {{
        padding-top: 0rem !important;
        padding-bottom: 1rem !important;
        margin-top: 0rem !important;
    }}
    
    /* Navigation Menu - Clean Style */
    .nav-area {{
        padding: 1rem 2rem;
        margin: 0rem !important;
        margin-bottom: 2rem !important;
        border-bottom: 1px solid #e9ecef;
        position: relative;
        top: -3rem;
        background: #ffffff;
        z-index: 1000;
    }}
    
    /* Force light text on dark backgrounds */
    .stApp {{
        background-color: #ffffff;
        color: #212529;
        font-size: 1.3rem;
    }}
    
    /* Show scrollbars */
    ::-webkit-scrollbar {{
        width: 12px;
        height: 12px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: #f1f1f1;
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: #888;
        border-radius: 6px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: #555;
    }}
    
    * {{
        scrollbar-width: auto;
        scrollbar-color: #888 #f1f1f1;
    }}
    
    /* Ensure text is readable */
    p, span, div, label, h1, h2, h3, h4, h5, h6 {{
        color: #212529 !important;
    }}
    
    p, span, div, label {{
        font-size: 1.3rem !important;
    }}
    
    h1 {{
        font-size: 3rem !important;
    }}
    
    h2 {{
        font-size: 2.5rem !important;
    }}
    
    h3 {{
        font-size: 2rem !important;
    }}
    
    h4 {{
        font-size: 1.75rem !important;
    }}
    
    /* Header Styles */
    .app-header {{
        background: linear-gradient(135deg, #4a90e2 0%, #6ba3e8 100%);
        padding: 3rem 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        text-align: center;
    }}
    
    .app-title {{
        font-size: 3rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    }}
    
    .app-subtitle {{
        font-size: 1.2rem;
        color: #ffffff;
        font-weight: 400;
    }}
    
    /* Sidebar Header Styles */
    .sidebar-header {{
        text-align: center;
        padding: 1.5rem 1rem;
        margin-bottom: 1.5rem;
        background: linear-gradient(135deg, #4a90e2 0%, #6ba3e8 100%);
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(74, 144, 226, 0.2);
    }}
    
    .sidebar-title {{
        font-size: 1.5rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.3rem;
        line-height: 1.3;
    }}
    
    .sidebar-subtitle {{
        font-size: 0.85rem;
        color: #ffffff;
        font-weight: 400;
        line-height: 1.4;
    }}
    
    /* Card Styles */
    .info-card {{
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border-left: 4px solid #4CAF50;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        height: 100%;
        min-height: 450px;
        display: flex;
        flex-direction: column;
    }}
    
    .info-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.12);
    }}
    
    /* Ensure columns have equal height */
    div[data-testid="column"] {{
        display: flex;
        flex-direction: column;
    }}
    
    div[data-testid="column"] > div {{
        flex: 1;
        display: flex;
        flex-direction: column;
    }}
    
    .warning-card {{
        background: #fff3cd;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #ffc107;
        box-shadow: 0 4px 15px rgba(255,193,7,0.1);
    }}
    
    .danger-card {{
        background: #f8d7da;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #dc3545;
        box-shadow: 0 4px 15px rgba(220,53,69,0.1);
    }}
    
    .success-card {{
        background: #d4edda;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #28a745;
        box-shadow: 0 4px 15px rgba(40,167,69,0.1);
    }}
    
    /* Risk Level Badges */
    .risk-badge {{
        display: inline-block;
        padding: 0.5rem 1.5rem;
        border-radius: 25px;
        font-weight: 600;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    
    .risk-high {{
        background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
        color: white;
    }}
    
    .risk-medium {{
        background: linear-gradient(135deg, #ffc107 0%, #e0a800 100%);
        color: #212529;
    }}
    
    .risk-low {{
        background: linear-gradient(135deg, #28a745 0%, #218838 100%);
        color: white;
    }}
    
    /* Metric Cards */
    .metric-card {{
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border-top: 3px solid #1e3c72;
    }}
    
    .metric-value {{
        font-size: 2.5rem;
        font-weight: 700;
        color: #1e3c72;
        margin: 0.5rem 0;
    }}
    
    .metric-label {{
        font-size: 0.9rem;
        color: #6c757d;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    
    /* Section Headers */
    .section-header {{
        font-size: 2.5rem;
        font-weight: 700;
        color: #1e3c72 !important;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #e0e7ff;
    }}
    
    /* Make all Streamlit text visible */
    .stMarkdown, .stText {{
        color: #212529 !important;
    }}
    
    /* File uploader text */
    .uploadedFile {{
        background: white;
        border-radius: 12px;
        padding: 1rem;
        border: 2px dashed #1e3c72;
        color: #212529 !important;
    }}
    
    /* Info boxes */
    .stAlert {{
        color: #212529 !important;
    }}
    
    /* ALL BUTTONS - Light colors, bigger size */
    .stButton>button {{
        background: #4a90e2 !important;
        color: #ffffff !important;
        border: 2px solid #4a90e2 !important;
        border-radius: 10px !important;
        padding: 1rem 2.5rem !important;
        font-weight: 600 !important;
        font-size: 1.3rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1) !important;
    }}
    
    .stButton>button:hover {{
        background: #6ba3e8 !important;
        border-color: #6ba3e8 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.15) !important;
    }}
    
    .stButton>button[kind="primary"] {{
        background: #4a90e2 !important;
        color: #ffffff !important;
        border: 2px solid #4a90e2 !important;
        font-weight: 700 !important;
    }}
    
    /* Download Buttons - Light colors */
    .stDownloadButton>button {{
        background: #4a90e2 !important;
        color: #ffffff !important;
        border: 2px solid #4a90e2 !important;
        border-radius: 10px !important;
        padding: 1rem 2.5rem !important;
        font-weight: 600 !important;
        font-size: 1.3rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1) !important;
    }}
    
    .stDownloadButton>button:hover {{
        background: #6ba3e8 !important;
        border-color: #6ba3e8 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.15) !important;
    }}
    
    /* Navigation buttons - transparent with bottom border */
    div.nav-area .stButton > button,
    .nav-area .stButton > button {{
        background: transparent !important;
        background-color: transparent !important;
        background-image: none !important;
        color: #1e3c72 !important;
        border: none !important;
        border-radius: 0 !important;
        padding: 1.2rem 2.5rem !important;
        font-weight: 600 !important;
        font-size: 1.6rem !important;
        transition: color 0.3s ease !important;
        box-shadow: none !important;
    }}
    
    div.nav-area .stButton > button:hover,
    .nav-area .stButton > button:hover {{
        background: transparent !important;
        color: #4a90e2 !important;
        transform: none !important;
        box-shadow: none !important;
        border: none !important;
    }}
    
    div.nav-area .stButton > button[kind="primary"],
    .nav-area .stButton > button[kind="primary"] {{
        background: transparent !important;
        color: #1e3c72 !important;
        font-weight: 700 !important;
        border-bottom: 4px solid #1e3c72 !important;
        border-top: none !important;
        border-left: none !important;
        border-right: none !important;
        box-shadow: none !important;
    }}
    
    /* Tabs Styling */
    .stTabs {{
        margin-top: 1rem;
    }}
    
    .stTabs [data-baseweb="tab-list"] {{
        gap: 0.5rem;
        background: transparent;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        height: auto;
        padding: 0.75rem 1.5rem;
        background: #f8f9fa;
        border-radius: 8px 8px 0 0;
        font-size: 1.1rem;
        font-weight: 500;
        color: #495057;
        border: none;
    }}
    
    .stTabs [data-baseweb="tab"]:hover {{
        background: #e9ecef;
        color: #1e3c72;
    }}
    
    .stTabs [aria-selected="true"] {{
        background: #4a90e2 !important;
        color: white !important;
    }}
    
    /* Page Container */
    .page-container {{
        padding: 0rem;
        max-width: 100%;
        margin: 0 auto;
    }}
    
    /* All Input Fields - Light backgrounds */
    input, textarea, select {{
        background: #ffffff !important;
        color: #212529 !important;
        border: 1px solid #ced4da !important;
        caret-color: #212529 !important;
    }}
    
    /* Text Input Fields */
    [data-testid="stTextInput"] input {{
        background: #ffffff !important;
        color: #212529 !important;
        border: 2px solid #ced4da !important;
        border-radius: 8px !important;
        padding: 0.75rem !important;
        font-size: 1.1rem !important;
        caret-color: #212529 !important;
    }}
    
    [data-testid="stTextInput"] input:focus {{
        border-color: #4a90e2 !important;
        box-shadow: 0 0 0 0.2rem rgba(74, 144, 226, 0.25) !important;
    }}
    
    /* Text Area */
    [data-testid="stTextArea"] textarea {{
        background: #ffffff !important;
        color: #212529 !important;
        border: 2px solid #ced4da !important;
        border-radius: 8px !important;
        padding: 0.75rem !important;
        font-size: 1.1rem !important;
        caret-color: #212529 !important;
    }}
    
    [data-testid="stTextArea"] textarea:focus {{
        border-color: #4a90e2 !important;
        box-shadow: 0 0 0 0.2rem rgba(74, 144, 226, 0.25) !important;
    }}
    
    /* Selectbox / Dropdown */
    [data-testid="stSelectbox"] {{
        background: #ffffff !important;
    }}
    
    [data-testid="stSelectbox"] label {{
        background: transparent !important;
        border: none !important;
        color: #212529 !important;
        font-weight: 600 !important;
    }}
    
    [data-testid="stSelectbox"] > div {{
        background: #ffffff !important;
    }}
    
    [data-testid="stSelectbox"] > div > div {{
        background: #ffffff !important;
        color: #212529 !important;
        border: 2px solid #ced4da !important;
        border-radius: 8px !important;
        min-height: 3.5rem !important;
        padding: 0.75rem 1rem !important;
        display: flex !important;
        align-items: center !important;
    }}
    
    [data-testid="stSelectbox"] input {{
        background: #ffffff !important;
        color: #212529 !important;
        line-height: 1.8 !important;
        font-size: 1.1rem !important;
        padding: 0.25rem 0 !important;
    }}
    
    [data-testid="stSelectbox"] [data-baseweb="select"] {{
        background: #ffffff !important;
        min-height: 3rem !important;
    }}
    
    [data-testid="stSelectbox"] [data-baseweb="select"] > div {{
        background: #ffffff !important;
        color: #212529 !important;
        padding: 0.5rem 1rem !important;
        min-height: 2.5rem !important;
        display: flex !important;
        align-items: center !important;
    }}
    
    /* Dropdown menu options */
    [role="listbox"] {{
        background: #ffffff !important;
        border: 1px solid #ced4da !important;
        border-radius: 8px !important;
    }}
    
    [role="option"] {{
        background: #ffffff !important;
        color: #212529 !important;
        padding: 0.5rem 1rem !important;
    }}
    
    [role="option"]:hover {{
        background: #e9ecef !important;
        color: #1e3c72 !important;
    }}
    
    [aria-selected="true"][role="option"] {{
        background: #d6e4f7 !important;
        color: #1e3c72 !important;
    }}
    
    /* Multiselect */
    [data-testid="stMultiSelect"] {{
        background: #ffffff !important;
    }}
    
    [data-testid="stMultiSelect"] label {{
        background: transparent !important;
        border: none !important;
        color: #212529 !important;
        font-weight: 600 !important;
    }}
    
    [data-testid="stMultiSelect"] > div {{
        background: #ffffff !important;
        color: #212529 !important;
        border: 2px solid #ced4da !important;
        border-radius: 8px !important;
        min-height: 3rem !important;
        padding: 0.5rem 0.75rem !important;
    }}
    
    [data-testid="stMultiSelect"] > div > div {{
        background: #ffffff !important;
        color: #212529 !important;
        min-height: 2rem !important;
    }}
    
    [data-testid="stMultiSelect"] input {{
        background: #ffffff !important;
        color: #212529 !important;
        line-height: 1.5 !important;
    }}
    
    /* Multiselect dropdown/menu */
    [data-testid="stMultiSelect"] [role="listbox"] {{
        background: #ffffff !important;
        color: #212529 !important;
    }}
    
    [data-testid="stMultiSelect"] [role="presentation"] {{
        background: #ffffff !important;
        color: #212529 !important;
    }}
    
    [data-testid="stMultiSelect"] ul {{
        background: #ffffff !important;
        color: #212529 !important;
    }}
    
    /* Multiselect "No results" and empty state */
    [data-testid="stMultiSelect"] li {{
        background: #ffffff !important;
        color: #212529 !important;
    }}
    
    /* Multiselect selected items (tags/chips) - with overflow control */
    [data-testid="stMultiSelect"] span {{
        background: #e9ecef !important;
        color: #212529 !important;
        border: 1px solid #ced4da !important;
        max-width: 100% !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        white-space: nowrap !important;
    }}
    
    [data-testid="stMultiSelect"] span[data-baseweb="tag"] {{
        background: #d6e4f7 !important;
        color: #1e3c72 !important;
        border: 1px solid #4a90e2 !important;
        font-weight: 500 !important;
        max-width: 100% !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        display: inline-flex !important;
        align-items: center !important;
    }}
    
    /* Multiselect tag text */
    [data-testid="stMultiSelect"] span[data-baseweb="tag"] span {{
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        white-space: nowrap !important;
    }}
    
    /* Multiselect clear/remove buttons */
    [data-testid="stMultiSelect"] svg {{
        color: #495057 !important;
        fill: #495057 !important;
        flex-shrink: 0 !important;
    }}
    
    [data-testid="stMultiSelect"] button {{
        background: transparent !important;
        color: #495057 !important;
    }}
    
    /* Number Input */
    [data-testid="stNumberInput"] input {{
        background: #ffffff !important;
        color: #212529 !important;
        border: 2px solid #ced4da !important;
        border-radius: 8px !important;
    }}
    
    /* Date Input */
    [data-testid="stDateInput"] input {{
        background: #ffffff !important;
        color: #212529 !important;
        border: 2px solid #ced4da !important;
        border-radius: 8px !important;
    }}
    
    /* Time Input */
    [data-testid="stTimeInput"] input {{
        background: #ffffff !important;
        color: #212529 !important;
        border: 2px solid #ced4da !important;
        border-radius: 8px !important;
    }}
    
    /* Upload Area */
    [data-testid="stFileUploader"] {{
        color: #212529 !important;
        background: #f8f9fa !important;
        padding: 2rem;
        border-radius: 12px;
        border: 2px dashed #6c757d;
    }}
    
    [data-testid="stFileUploader"] label {{
        color: #212529 !important;
        font-weight: 600 !important;
    }}
    
    [data-testid="stFileUploader"] div {{
        color: #212529 !important;
    }}
    
    [data-testid="stFileUploader"] section {{
        background: #e9ecef !important;
        border: 2px dashed #adb5bd !important;
        border-radius: 8px;
    }}
    
    [data-testid="stFileUploader"] section:hover {{
        border-color: #1e3c72 !important;
        background: #d6e4f7 !important;
    }}
    
    /* File Uploader Browse Button */
    [data-testid="stFileUploader"] button {{
        background: #e9ecef !important;
        color: #212529 !important;
        border: 2px solid #adb5bd !important;
        border-radius: 8px !important;
        padding: 0.5rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }}
    
    [data-testid="stFileUploader"] button:hover {{
        background: #d6e4f7 !important;
        border-color: #1e3c72 !important;
        color: #1e3c72 !important;
    }}
    
    /* Help Icon (Question Mark) - All variations */
    [data-testid="stFileUploader"] [data-testid="stTooltipIcon"] {{
        color: #495057 !important;
    }}
    
    [data-testid="stFileUploader"] [data-testid="stTooltipIcon"]:hover {{
        color: #1e3c72 !important;
    }}
    
    [data-testid="stFileUploader"] svg {{
        color: #495057 !important;
        fill: #495057 !important;
    }}
    
    [data-testid="stFileUploader"] svg:hover {{
        color: #1e3c72 !important;
        fill: #1e3c72 !important;
    }}
    
    /* Tooltip container and content */
    [role="tooltip"] {{
        background: #f8f9fa !important;
        color: #212529 !important;
        border: 1px solid #dee2e6 !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
        font-size: 1rem !important;
        padding: 0.75rem !important;
    }}
    
    [role="tooltip"] * {{
        color: #212529 !important;
    }}
    
    .stTooltipContent {{
        background: #f8f9fa !important;
        color: #212529 !important;
    }}
    
    /* All help icons globally */
    [data-testid="stTooltipIcon"] svg {{
        color: #495057 !important;
        fill: #495057 !important;
    }}
    
    [data-testid="stTooltipIcon"]:hover svg {{
        color: #1e3c72 !important;
        fill: #1e3c72 !important;
    }}
    
    /* Sidebar Styling */
    .css-1d391kg, [data-testid="stSidebar"] {{
        background: #f8f9fa;
    }}
    
    [data-testid="stSidebar"] * {{
        color: #212529 !important;
        font-size: 1.4rem !important;
    }}
    
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {{
        font-size: 1.8rem !important;
    }}
    
    /* Progress Steps */
    .progress-step {{
        background: white;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #2a5298;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        font-weight: 500;
    }}
    
    /* Table Styling */
    .dataframe {{
        border-radius: 12px !important;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    }}
    
    /* DataFrame Headers - Light colors with dark text */
    .dataframe thead tr {{
        background: #4a90e2 !important;
    }}
    
    .dataframe thead th {{
        background: #4a90e2 !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        padding: 0.75rem !important;
        border: none !important;
        font-size: 1.1rem !important;
    }}
    
    /* DataFrame Body */
    .dataframe tbody tr {{
        background: #ffffff !important;
    }}
    
    .dataframe tbody tr:nth-child(even) {{
        background: #f8f9fa !important;
    }}
    
    .dataframe tbody td {{
        color: #212529 !important;
        padding: 0.75rem !important;
        border: 1px solid #dee2e6 !important;
        font-size: 1.1rem !important;
    }}
    
    /* Streamlit DataFrame Container */
    [data-testid="stDataFrame"] {{
        background: #ffffff !important;
    }}
    
    [data-testid="stDataFrame"] * {{
        color: #212529 !important;
    }}
    
    /* Expander Styling - Light colors with visible text */
    .streamlit-expanderHeader {{
        background: #f8f9fa !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        color: #212529 !important;
        border: 1px solid #dee2e6 !important;
    }}
    
    .streamlit-expanderHeader:hover {{
        background: #e9ecef !important;
        color: #1e3c72 !important;
    }}
    
    /* Target all expander elements */
    [data-testid="stExpander"] {{
        background: #ffffff !important;
        border: 1px solid #dee2e6 !important;
        border-radius: 8px !important;
    }}
    
    [data-testid="stExpander"] summary {{
        background: #f8f9fa !important;
        color: #212529 !important;
        font-weight: 600 !important;
        padding: 0.75rem 1rem !important;
    }}
    
    [data-testid="stExpander"] summary:hover {{
        background: #e9ecef !important;
        color: #1e3c72 !important;
    }}
    
    /* Expander content area */
    [data-testid="stExpander"] > div {{
        background: #ffffff !important;
        color: #212529 !important;
    }}
    
    /* Footer */
    .app-footer {{
        text-align: center;
        padding: 2rem;
        color: #6c757d;
        font-size: 0.9rem;
        border-top: 1px solid #dee2e6;
        margin-top: 3rem;
    }}}}
</style>
"""

st.markdown(css_code, unsafe_allow_html=True)

# Initialize session state
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'uploaded_file_name' not in st.session_state:
    st.session_state.uploaded_file_name = None


def analyze_contract(uploaded_file, modules):
    """Perform complete contract analysis"""
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Step 1: Process document
        status_text.markdown('<div class="progress-step">Step 1/7: Extracting text from document...</div>', unsafe_allow_html=True)
        progress_bar.progress(15)
        doc_result = modules['doc'].process_uploaded_file(uploaded_file)
        
        if not doc_result['success']:
            st.error(f"Error processing document: {doc_result.get('error', 'Unknown error')}")
            return None
        
        text = doc_result['text']
        
        if not text or len(text) < 100:
            st.error("Document appears to be empty or too short. Please upload a valid contract.")
            return None
        
        # Step 2: Detect language
        status_text.markdown('<div class="progress-step">Step 2/7: Detecting language...</div>', unsafe_allow_html=True)
        progress_bar.progress(25)
        lang_info = modules['lang'].detect_language(text)
        
        # Step 3: Extract entities
        status_text.markdown('<div class="progress-step">Step 3/7: Extracting contract entities...</div>', unsafe_allow_html=True)
        progress_bar.progress(40)
        entities = modules['entity'].extract_all_entities(text)
        
        # Step 4: Analyze clauses
        status_text.markdown('<div class="progress-step">Step 4/7: Analyzing contract clauses...</div>', unsafe_allow_html=True)
        progress_bar.progress(55)
        clause_analysis = modules['clause'].analyze_clauses(text)
        
        # Step 5: LLM Analysis (if API key is configured)
        status_text.markdown('<div class="progress-step">Step 5/7: Performing AI-powered analysis...</div>', unsafe_allow_html=True)
        progress_bar.progress(70)
        try:
            contract_analyzer = modules['contract']
            
            # Classify contract
            classification = contract_analyzer.classify_contract_type(text)
            
            # Generate summary
            summary = contract_analyzer.generate_summary(text, classification['contract_type'])
            
            # Identify risks
            llm_risks = contract_analyzer.identify_risks(text, classification['contract_type'])
            
            # Check compliance
            compliance = contract_analyzer.check_compliance(text, classification['contract_type'])
            
        except Exception as e:
            st.warning(f"LLM analysis unavailable: {str(e)}. Continuing with NLP-based analysis.")
            classification = {"contract_type": "General Contract", "confidence": "Low", "reasoning": "LLM unavailable"}
            summary = "AI-powered summary unavailable. Please check your API key configuration."
            llm_risks = []
            compliance = {"full_analysis": "Compliance check unavailable"}
        
        # Step 6: Risk assessment
        status_text.markdown('<div class="progress-step">Step 6/7: Calculating risk scores...</div>', unsafe_allow_html=True)
        progress_bar.progress(85)
        risk_assessment = modules['risk'].assess_contract_risk(clause_analysis, llm_risks)
        
        # Identify unfavorable clauses
        unfavorable_clauses = modules['clause'].identify_unfavorable_clauses(clause_analysis)
        
        # Generate mitigation strategies
        mitigation_strategies = modules['risk'].generate_risk_mitigation_strategies(risk_assessment)
        
        # Generate negotiation points
        if unfavorable_clauses:
            try:
                negotiation_points = contract_analyzer.generate_negotiation_points(unfavorable_clauses)
            except:
                negotiation_points = ["Negotiation points unavailable - LLM not configured"]
        else:
            negotiation_points = []
        
        # Step 7: Compile results
        status_text.markdown('<div class="progress-step">Step 7/7: Compiling analysis results...</div>', unsafe_allow_html=True)
        progress_bar.progress(100)
        
        results = {
            'document_info': doc_result,
            'language_info': lang_info,
            'contract_classification': classification,
            'llm_summary': summary,
            'entities': entities,
            'clause_analysis': clause_analysis,
            'risk_assessment': risk_assessment,
            'unfavorable_clauses': unfavorable_clauses,
            'mitigation_strategies': mitigation_strategies,
            'negotiation_points': negotiation_points,
            'compliance_check': compliance,
            'timestamp': datetime.now().isoformat()
        }
        
        status_text.empty()
        progress_bar.empty()
        st.success("Analysis complete!")
        return results
        
    except Exception as e:
        st.error(f"Error during analysis: {str(e)}")
        import traceback
        st.error(traceback.format_exc())
        return None


def display_analysis_results(results, modules):
    """Display comprehensive analysis results"""
    
    # Main tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Summary", "Risk Assessment", "Clause Analysis", 
        "Extracted Data", "Recommendations", "Export"
    ])
    
    # Tab 1: Summary
    with tab1:
        st.markdown('<div class="section-header">Contract Summary</div>', unsafe_allow_html=True)
        
        # Key Metrics Row
        classification = results.get('contract_classification', {})
        risk_assessment = results.get('risk_assessment', {})
        risk_level = risk_assessment.get('overall_level', 'Unknown')
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f'''
            <div class="metric-card">
                <div class="metric-label">Contract Type</div>
                <div class="metric-value" style="font-size: 1.5rem;">{classification.get('contract_type', 'Unknown')}</div>
            </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            risk_badge_class = f"risk-{risk_level.lower()}"
            st.markdown(f'''
            <div class="metric-card">
                <div class="metric-label">Risk Level</div>
                <div style="margin-top: 1rem;">
                    <span class="risk-badge {risk_badge_class}">{risk_level}</span>
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        with col3:
            total_risks = risk_assessment.get('total_risks_found', 0)
            st.markdown(f'''
            <div class="metric-card">
                <div class="metric-label">Total Risks</div>
                <div class="metric-value">{total_risks}</div>
            </div>
            ''', unsafe_allow_html=True)
        
        with col4:
            high_priority = len(risk_assessment.get('high_priority_risks', []))
            st.markdown(f'''
            <div class="metric-card">
                <div class="metric-label">High Priority</div>
                <div class="metric-value">{high_priority}</div>
            </div>
            ''', unsafe_allow_html=True)
        
        # Language info
        lang_info = results.get('language_info', {})
        if lang_info.get('is_multilingual'):
            st.markdown('<div class="info-card"><strong>Multilingual Content:</strong> This contract contains both English and Hindi text</div>', unsafe_allow_html=True)
        
        # AI Summary
        st.markdown('<div class="section-header">AI-Generated Summary</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="info-card">{results.get("llm_summary", "Summary not available")}</div>', unsafe_allow_html=True)
        
        # Document Statistics
        st.markdown('<div class="section-header">Document Statistics</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            doc_info = results.get('document_info', {})
            st.markdown(f'''
            <div class="info-card">
                <h4>Document Information</h4>
                <p><strong>File:</strong> {doc_info.get('file_name', 'Unknown')}</p>
                <p><strong>Type:</strong> {doc_info.get('file_type', 'Unknown')}</p>
                <p><strong>Word Count:</strong> ~{len(doc_info.get('text', '').split())}</p>
            </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'''
            <div class="info-card">
                <h4>Analysis Metrics</h4>
                <p><strong>Clauses Analyzed:</strong> {len(results.get('clause_analysis', []))}</p>
                <p><strong>Parties Identified:</strong> {len(results.get('entities', {}).get('parties', []))}</p>
                <p><strong>Unfavorable Clauses:</strong> {len(results.get('unfavorable_clauses', []))}</p>
            </div>
            ''', unsafe_allow_html=True)
    
    # Tab 2: Risk Assessment
    with tab2:
        st.markdown('<div class="section-header">Risk Assessment</div>', unsafe_allow_html=True)
        
        risk_assessment = results.get('risk_assessment', {})
        risk_level = risk_assessment.get('overall_level', 'UNKNOWN')
        risk_score = risk_assessment.get('overall_score', 0)
        
        # Overall Risk Display
        if risk_level == 'HIGH':
            st.markdown(f'<div class="danger-card"><h3>HIGH RISK (Score: {risk_score}/100)</h3><p>{risk_assessment.get("recommendation", "")}</p></div>', unsafe_allow_html=True)
        elif risk_level == 'MEDIUM':
            st.markdown(f'<div class="warning-card"><h3>MEDIUM RISK (Score: {risk_score}/100)</h3><p>{risk_assessment.get("recommendation", "")}</p></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="success-card"><h3>LOW RISK (Score: {risk_score}/100)</h3><p>{risk_assessment.get("recommendation", "")}</p></div>', unsafe_allow_html=True)
        
        # High priority risks
        high_priority = risk_assessment.get('high_priority_risks', [])
        if high_priority:
            st.markdown('<div class="section-header">High Priority Risks</div>', unsafe_allow_html=True)
            
            for i, risk in enumerate(high_priority, 1):
                with st.expander(f"{i}. {risk.get('risk_type', 'Unknown Risk')} - Clause {risk.get('clause_id', 'N/A')}"):
                    st.write(f"**Category:** {risk.get('category', 'Unknown')}")
                    st.write(f"**Description:** {risk.get('description', 'No description')}")
        
        # Risk breakdown by category
        st.markdown('<div class="section-header">Risk Breakdown by Category</div>', unsafe_allow_html=True)
        
        risk_breakdown = risk_assessment.get('risk_breakdown', {})
        category_data = []
        for category, risks in risk_breakdown.items():
            if risks:
                high = sum(1 for r in risks if r.get('severity') == 'HIGH')
                medium = sum(1 for r in risks if r.get('severity') == 'MEDIUM')
                low = sum(1 for r in risks if r.get('severity') == 'LOW')
                
                category_name = config.RISK_CATEGORIES.get(category, category.replace('_', ' ').title())
                category_data.append({
                    'Category': category_name,
                    'High': high,
                    'Medium': medium,
                    'Low': low,
                    'Total': len(risks)
                })
        
        if category_data:
            import pandas as pd
            df = pd.DataFrame(category_data)
            st.dataframe(df, width='stretch')
        else:
            st.info("No significant risks identified by category.")
        
        # Mitigation strategies
        st.markdown('<div class="section-header">Risk Mitigation Strategies</div>', unsafe_allow_html=True)
        
        strategies = results.get('mitigation_strategies', [])
        for strategy in strategies:
            with st.expander(f"{strategy.get('risk_category', 'Category')} - Priority: {strategy.get('priority', 'MEDIUM')}"):
                st.write(f"**Strategy:** {strategy.get('strategy', '')}")
                st.write("**Recommended Actions:**")
                for action in strategy.get('actions', []):
                    st.write(f"- {action}")
    
    # Tab 3: Clause Analysis
    with tab3:
        st.markdown('<div class="section-header">Clause-by-Clause Analysis</div>', unsafe_allow_html=True)
        
        clause_analysis = results.get('clause_analysis', [])
        
        # Filter options
        col1, col2 = st.columns(2)
        
        with col1:
            clause_types = list(set(c.get('clause_type', 'Unknown') for c in clause_analysis))
            selected_types = st.multiselect("Filter by clause type:", clause_types, default=clause_types)
        
        with col2:
            risk_filter = st.selectbox("Filter by risk:", ["All", "High Risk Only", "Medium Risk Only", "Low Risk Only", "No Risk"])
        
        # Filter clauses
        filtered_clauses = clause_analysis
        if selected_types:
            filtered_clauses = [c for c in filtered_clauses if c.get('clause_type') in selected_types]
        
        if risk_filter != "All":
            if risk_filter == "High Risk Only":
                filtered_clauses = [c for c in filtered_clauses if any(r.get('severity') == 'HIGH' for r in c.get('risks', []))]
            elif risk_filter == "Medium Risk Only":
                filtered_clauses = [c for c in filtered_clauses if any(r.get('severity') == 'MEDIUM' for r in c.get('risks', []))]
            elif risk_filter == "Low Risk Only":
                filtered_clauses = [c for c in filtered_clauses if any(r.get('severity') == 'LOW' for r in c.get('risks', []))]
            elif risk_filter == "No Risk":
                filtered_clauses = [c for c in filtered_clauses if not c.get('risks')]
        
        st.write(f"Showing {len(filtered_clauses)} of {len(clause_analysis)} clauses")
        
        # Display clauses
        for clause in filtered_clauses:
            clause_id = clause.get('clause_id', 'Unknown')
            clause_type = clause.get('clause_type', 'Unknown')
            risks = clause.get('risks', [])
            
            # Determine risk level for styling
            if any(r.get('severity') == 'HIGH' for r in risks):
                risk_level_text = "HIGH RISK"
            elif any(r.get('severity') == 'MEDIUM' for r in risks):
                risk_level_text = "MEDIUM RISK"
            elif risks:
                risk_level_text = "LOW RISK"
            else:
                risk_level_text = "NO RISK"
            
            with st.expander(f"Clause {clause_id}: {clause_type} [{risk_level_text}]"):
                st.write(f"**Type:** {clause_type}")
                st.write(f"**Text:** {clause.get('original_text', 'N/A')[:500]}{'...' if len(clause.get('original_text', '')) > 500 else ''}")
                
                if risks:
                    st.write("**Identified Risks:**")
                    for risk in risks:
                        severity = risk.get('severity', 'UNKNOWN')
                        st.write(f"- [{severity}] {risk.get('risk_type', 'Unknown')}: {risk.get('description', '')}")
                
                # Obligations
                obligations = clause.get('obligations', {})
                if any(obligations.values()):
                    st.write("**Obligations & Rights:**")
                    if obligations.get('obligations'):
                        st.write(f"- Obligations: {len(obligations['obligations'])}")
                    if obligations.get('rights'):
                        st.write(f"- Rights: {len(obligations['rights'])}")
                    if obligations.get('prohibitions'):
                        st.write(f"- Prohibitions: {len(obligations['prohibitions'])}")
    
    # Tab 4: Extracted Data
    with tab4:
        st.markdown('<div class="section-header">Extracted Contract Information</div>', unsafe_allow_html=True)
        
        entities = results.get('entities', {})
        
        col1, col2 = st.columns(2)
        
        # Parties
        with col1:
            st.markdown('<h3>Parties Involved</h3>', unsafe_allow_html=True)
            parties = entities.get('parties', [])
            if parties:
                party_list = "<br>".join([f"• <strong>{party.get('name', 'Unknown')}</strong> - {party.get('role', 'Role')}" for party in parties[:10]])
                st.markdown(f'<div class="info-card">{party_list}</div>', unsafe_allow_html=True)
            else:
                st.info("No parties identified")
        
        # Financial terms
        with col2:
            st.markdown('<h3>Financial Terms</h3>', unsafe_allow_html=True)
            amounts = entities.get('amounts', [])
            if amounts:
                amount_list = "<br>".join([f"• {amount.get('amount', 'Amount')} - {amount.get('currency', 'Currency')}" for amount in amounts[:10]])
                st.markdown(f'<div class="info-card">{amount_list}</div>', unsafe_allow_html=True)
            else:
                st.info("No financial terms identified")
        
        col3, col4 = st.columns(2)
        
        # Dates
        with col3:
            st.markdown('<h3>Important Dates</h3>', unsafe_allow_html=True)
            dates = entities.get('dates', [])
            if dates:
                date_list = "<br>".join([f"• {date.get('date', 'Date')}" for date in dates[:10]])
                st.markdown(f'<div class="info-card">{date_list}</div>', unsafe_allow_html=True)
            else:
                st.info("No dates identified")
        
        # Jurisdiction
        with col4:
            st.markdown('<h3>Jurisdiction</h3>', unsafe_allow_html=True)
            jurisdictions = entities.get('jurisdictions', [])
            if jurisdictions:
                jurisdiction_list = "<br>".join([f"• {jurisdiction.get('jurisdiction', 'Unknown')}" for jurisdiction in jurisdictions[:5]])
                st.markdown(f'<div class="info-card">{jurisdiction_list}</div>', unsafe_allow_html=True)
            else:
                st.info("No jurisdiction information identified")
    
    # Tab 5: Recommendations
    with tab5:
        st.markdown('<div class="section-header">Recommendations & Negotiation Points</div>', unsafe_allow_html=True)
        
        # Unfavorable clauses
        st.markdown('<h3>Unfavorable Clauses Identified</h3>', unsafe_allow_html=True)
        unfavorable = results.get('unfavorable_clauses', [])
        
        if unfavorable:
            for i, clause in enumerate(unfavorable, 1):
                with st.expander(f"{i}. Clause {clause.get('clause_id', 'Unknown')} - {clause.get('clause_type', 'Unknown')}"):
                    st.write(f"**Severity:** {clause.get('severity', 'Unknown')}")
                    st.write("**Issues:**")
                    for reason in clause.get('reasons', []):
                        st.write(f"- {reason}")
                    st.write(f"**Text Preview:** {clause.get('text', 'N/A')}")
        else:
            st.markdown('<div class="success-card">No significantly unfavorable clauses identified!</div>', unsafe_allow_html=True)
        
        # Negotiation points
        st.markdown('<h3>Negotiation Points</h3>', unsafe_allow_html=True)
        negotiation_points = results.get('negotiation_points', [])
        
        if negotiation_points:
            st.write("Use these points when discussing the contract:")
            for point in negotiation_points:
                st.markdown(f'<div class="info-card">{point}</div>', unsafe_allow_html=True)
        else:
            st.info("No specific negotiation points generated")
        
        # Compliance check
        st.markdown('<h3>Compliance Considerations</h3>', unsafe_allow_html=True)
        compliance = results.get('compliance_check', {})
        st.markdown(f'<div class="info-card">{compliance.get("full_analysis", "Compliance analysis not available")}</div>', unsafe_allow_html=True)
    
    # Tab 6: Export
    with tab6:
        st.markdown('<div class="section-header">Export Analysis Results</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Generate Full PDF Report", width='stretch', type="primary"):
                with st.spinner("Generating PDF report..."):
                    try:
                        pdf_path = modules['report'].generate_full_report(results)
                        st.success("Report generated successfully!")
                        
                        with open(pdf_path, 'rb') as f:
                            st.download_button(
                                label="Download PDF Report",
                                data=f,
                                file_name=f"contract_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                                mime="application/pdf",
                                width='stretch'
                            )
                    except Exception as e:
                        st.error(f"Error generating PDF: {str(e)}")
        
        with col2:
            if st.button("Generate Summary PDF", width='stretch'):
                with st.spinner("Generating summary..."):
                    try:
                        pdf_path = modules['report'].generate_summary_report(results)
                        st.success("Summary generated successfully!")
                        
                        with open(pdf_path, 'rb') as f:
                            st.download_button(
                                label="Download Summary PDF",
                                data=f,
                                file_name=f"contract_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                                mime="application/pdf",
                                width='stretch'
                            )
                    except Exception as e:
                        st.error(f"Error generating summary: {str(e)}")
        
        with col3:
            if st.button("Export as JSON", width='stretch'):
                try:
                    json_path = modules['report'].export_to_json(results)
                    
                    with open(json_path, 'r', encoding='utf-8') as f:
                        st.download_button(
                            label="Download JSON Data",
                            data=f.read(),
                            file_name=f"contract_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                            mime="application/json",
                            width='stretch'
                        )
                except Exception as e:
                    st.error(f"Error exporting JSON: {str(e)}")
        
        st.markdown('<div class="info-card" style="margin-top: 2rem;">All analyses are logged for audit purposes with timestamps and key metrics.</div>', unsafe_allow_html=True)


def main():
    """Main application"""
    
    # Initialize session state for navigation
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'Home'
    
    # Create clean navigation bar with logo
    st.markdown('<div class="nav-area">', unsafe_allow_html=True)
    
    # Navigation with logo on the left
    col_logo, spacer1, col1, col2, col3, col4, spacer2 = st.columns([1.5, 0.5, 1.2, 1.2, 1.2, 1.2, 2])
    
    with col_logo:
        try:
            st.image("Images/logo.jpg", width=200)
        except:
            pass  # If logo not found, continue without it
    
    with col1:
        if st.button("Home", use_container_width=True, type="primary" if st.session_state.current_page == 'Home' else "secondary", key="nav_home"):
            st.session_state.current_page = 'Home'
            st.rerun()
    
    with col2:
        if st.button("Analyze", use_container_width=True, type="primary" if st.session_state.current_page == 'Analyze Contract' else "secondary", key="nav_analyze"):
            st.session_state.current_page = 'Analyze Contract'
            st.rerun()
    
    with col3:
        if st.button("Generate", use_container_width=True, type="primary" if st.session_state.current_page == 'Generate Template' else "secondary", key="nav_generate"):
            st.session_state.current_page = 'Generate Template'
            st.rerun()
    
    with col4:
        if st.button("Help", use_container_width=True, type="primary" if st.session_state.current_page == 'Help & FAQ' else "secondary", key="nav_help"):
            st.session_state.current_page = 'Help & FAQ'
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        # Website title in sidebar
        st.markdown('''
        <div class="sidebar-header">
            <div class="sidebar-title">Legal Assistant</div>
            <div class="sidebar-subtitle">For Indian Small & Medium Enterprises</div>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown("### Quick Links")
        st.write("• Contract Analysis")
        st.write("• Template Generation")
        st.write("• Risk Assessment")
        st.write("• Help & Documentation")
    
    # Main content container
    st.markdown('<div class="page-container">', unsafe_allow_html=True)
    
    # Page 1: Home
    if st.session_state.current_page == 'Home':
        st.markdown('<div class="section-header">Welcome to Legal Assistant</div>', unsafe_allow_html=True)
        
        st.markdown('''
        <div class="info-card">
        <p style="font-size: 1.3rem;">This AI-powered legal assistant is designed specifically for Indian SME business owners to help them navigate complex legal contracts with confidence.</p>
        
        <h1>What We Do</h1>
        <ul style="font-size: 1.4rem;">
        <li><strong>Understand Complex Contracts:</strong> Break down legal jargon into plain language that business owners can understand</li>
        <li><strong>Identify Potential Risks:</strong> Automatically detect problematic clauses, unfavorable terms, and compliance issues</li>
        <li><strong>Get Plain-Language Explanations:</strong> Receive clear, actionable insights about what each clause means for your business</li>
        <li><strong>Receive Actionable Advice:</strong> Get specific recommendations on negotiation points and risk mitigation strategies</li>
        </ul>
        </div>
        ''', unsafe_allow_html=True)
        
        # Two columns for Supported Contract Types and Features
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="section-header">Supported Contract Types</div>', unsafe_allow_html=True)
            contract_list = ""
            for contract_type in config.CONTRACT_TYPES:
                contract_list += f"<p>✓ {contract_type}</p>\n"
            st.markdown(f'<div class="info-card">{contract_list}</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="section-header">Key Features</div>', unsafe_allow_html=True)
            st.markdown('''
            <div class="info-card">
            <p>✓ <strong>Multilingual Support</strong> - English and Hindi</p>
            <p>✓ <strong>AI-Powered Analysis</strong> - Advanced NLP and LLM</p>
            <p>✓ <strong>Risk Assessment</strong> - Identify potential issues</p>
            <p>✓ <strong>Clause Analysis</strong> - Detailed breakdown</p>
            <p>✓ <strong>Smart Recommendations</strong> - Actionable advice</p>
            <p>✓ <strong>PDF Reports</strong> - Export your analysis</p>
            <p>✓ <strong>Template Generation</strong> - Standard contracts</p>
            <p>✓ <strong>Compliance Check</strong> - Indian legal standards</p>
            </div>
            ''', unsafe_allow_html=True)
        
        st.markdown('<div class="section-header">Getting Started</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('''
            <div class="info-card" style="text-align: center;">
            <h3 style="color: #1e3c72;">📄 Step 1</h3>
            <p><strong>Upload Your Contract</strong></p>
            <p>Click "Analyze Contract" and upload your document (PDF, DOCX, or TXT)</p>
            </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            st.markdown('''
            <div class="info-card" style="text-align: center;">
            <h3 style="color: #1e3c72;">🔍 Step 2</h3>
            <p><strong>AI Analysis</strong></p>
            <p>Our AI analyzes your contract for risks, clauses, and compliance issues</p>
            </div>
            ''', unsafe_allow_html=True)
        
        with col3:
            st.markdown('''
            <div class="info-card" style="text-align: center;">
            <h3 style="color: #1e3c72;">📊 Step 3</h3>
            <p><strong>Review & Export</strong></p>
            <p>Get detailed insights and export professional PDF reports</p>
            </div>
            ''', unsafe_allow_html=True)
        
        st.markdown('<div class="section-header">Important Disclaimer</div>', unsafe_allow_html=True)
        
        st.markdown('''
        <div class="warning-card">
        <h3>⚠️ Legal Disclaimer</h3>
        <p><strong>This tool provides informational analysis only and does NOT constitute legal advice.</strong></p>
        
        <p>While we strive for accuracy and comprehensiveness in our analysis:</p>
        <ul>
        <li>This tool does NOT replace consultation with a qualified legal professional</li>
        <li>Should NOT be relied upon as the sole basis for legal decisions</li>
        <li>May not capture all nuances specific to your situation</li>
        <li>Cannot account for the latest changes in laws and regulations</li>
        </ul>
        
        <p><strong>Always consult with a licensed lawyer before signing any contract or making important legal decisions.</strong></p>
        </div>
        ''', unsafe_allow_html=True)
    
    # Page 2: Analyze Contract
    elif st.session_state.current_page == 'Analyze Contract':
        st.markdown('<div class="section-header">Upload and Analyze Your Contract</div>', unsafe_allow_html=True)
        
        # Use cached processors
        modules = processors
        
        # File upload
        uploaded_file = st.file_uploader(
            "Choose a contract file (PDF, DOCX, TXT)",
            type=['pdf', 'docx', 'doc', 'txt'],
            help="Upload your contract document for analysis"
        )
        
        if uploaded_file:
            st.markdown(f'<div class="success-card">File uploaded: {uploaded_file.name}</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns([1, 3])
            
            with col1:
                analyze_button = st.button("Analyze Contract", type="primary", width='stretch')
            
            with col2:
                st.info("Analysis may take 30-60 seconds depending on contract size")
            
            if analyze_button:
                # Perform analysis
                results = analyze_contract(uploaded_file, modules)
                
                if results:
                    # Store in session state
                    st.session_state.analysis_results = results
                    st.session_state.uploaded_file_name = uploaded_file.name
                    
                    # Create audit log
                    modules['report'].create_audit_log(results)
        
        # Display results if available
        if st.session_state.analysis_results:
            st.markdown("---")
            st.markdown(f'<div class="section-header">Analysis Results for: {st.session_state.uploaded_file_name}</div>', unsafe_allow_html=True)
            display_analysis_results(st.session_state.analysis_results, modules)
    
    # Page 2: Generate Template
    elif st.session_state.current_page == 'Generate Template':
        st.markdown('<div class="section-header">Generate Standard Contract Template</div>', unsafe_allow_html=True)
        
        # Use cached processors
        modules = processors
        
        template_gen = modules['template']
        
        st.write("Generate SME-friendly contract templates compliant with Indian laws")
        
        # List available templates
        templates = template_gen.list_available_templates()
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            selected_template = st.selectbox(
                "Select Template Type:",
                options=[t['id'] for t in templates],
                format_func=lambda x: next(t['name'] for t in templates if t['id'] == x)
            )
        
        with col2:
            template_info = next(t for t in templates if t['id'] == selected_template)
            # Replace newlines with <br> for proper HTML rendering
            description_html = template_info["description"].replace('\n', '<br>')
            st.markdown(f'<div class="info-card"><strong>{template_info["name"]}</strong><br>{description_html}</div>', unsafe_allow_html=True)
        
        # Get required fields
        required_fields = template_gen.get_template_fields(selected_template)
        
        if required_fields:
            st.subheader("Customize Template")
            
            custom_fields = {}
            for field in required_fields:
                field_label = field.replace('_', ' ').title()
                custom_fields[field] = st.text_input(field_label, key=f"field_{field}")
        else:
            custom_fields = None
        
        if st.button("Generate Template", type="primary"):
            template_text = template_gen.generate_template(selected_template, custom_fields)
            
            st.success("Template generated successfully!")
            
            st.text_area("Generated Template:", template_text, height=400)
            
            # Download button
            st.download_button(
                label="Download Template",
                data=template_text,
                file_name=f"{selected_template}_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )
    
    # Page 3: Help & FAQ
    elif st.session_state.current_page == 'Help & FAQ':
        st.markdown('<div class="section-header">How to Use Legal Assistant</div>', unsafe_allow_html=True)
        
        st.markdown("""
        ### Getting Started
        
        1. **Upload Your Contract**: Click on "Analyze Contract" tab and upload your contract file (PDF, DOCX, or TXT)
        2. **Wait for Analysis**: The AI will analyze your contract (30-60 seconds)
        3. **Review Results**: Explore risk assessment, clause analysis, and recommendations
        4. **Export Reports**: Generate PDF reports for your records or legal consultation
        
        ### Understanding Risk Levels
        
        - **HIGH RISK**: Requires immediate attention and likely legal review
        - **MEDIUM RISK**: Should be reviewed carefully, may need negotiation  
        - **LOW RISK**: Standard terms, minimal concerns
        
        ### What Gets Analyzed
        
        - Contract type classification
        - Parties and key entities
        - Financial terms and amounts
        - Important dates and deadlines
        - Clause-by-clause risk assessment
        - Unfavorable terms identification
        - Compliance considerations
        
        ### Multilingual Support
        
        The system can process contracts in:
        - English
        - Hindi (हिंदी)
        - Mixed English-Hindi documents
        
        ### Privacy & Security
        
        - Your contracts are processed securely
        - No data is stored permanently without your consent
        - Audit logs track analysis for your records
        - Export and delete data at any time
        
        ### Limitations
        
        **Important:** This tool provides informational analysis only. It does NOT constitute legal advice.
        Always consult with a qualified legal professional before signing any contract.
        
        ### Support
        
        For questions or issues, please refer to the README documentation.
        """)
        
        st.markdown('<div class="section-header">Frequently Asked Questions</div>', unsafe_allow_html=True)
        
        with st.expander("What types of contracts can I analyze?"):
            st.write("""
            The system supports:
            - Employment Agreements
            - Vendor/Supplier Contracts
            - Service Agreements
            - Lease Agreements
            - Partnership Deeds
            - Non-Disclosure Agreements (NDAs)
            - General Contracts
            """)
        
        with st.expander("How accurate is the risk assessment?"):
            st.write("""
            The risk assessment combines:
            - Rule-based NLP analysis
            - AI/LLM-powered legal reasoning
            - Pattern matching against common risks
            
            While comprehensive, it should not replace professional legal review for important contracts.
            """)
        
        with st.expander("Can I use this for legal advice?"):
            st.write("""
            **NO**. This tool provides informational analysis and educational content only.
            It is NOT a substitute for professional legal advice. Always consult with a
            qualified lawyer for legal decisions.
            """)
        
        with st.expander("Is my contract data secure?"):
            st.write("""
            Yes. The application:
            - Processes documents securely
            - Uses secure API connections for AI analysis
            - Does not permanently store contract content without consent
            - Creates audit logs with metadata only (not full contract text)
            """)
    
    # Close page container
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown('''
    <div class="app-footer">
        <p>Your Legal Partner Across India.</p>
        <p>© 2026 Adithya. All Rights Reserved.</p>
        <p>Email: tsadithya24@gmail.com | Phone: +91-8300658690</p>
    </div>
    ''', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
