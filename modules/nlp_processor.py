"""
NLP Processor Module
Handles text preprocessing, sentence segmentation, and basic NLP tasks
"""
import re
from typing import List, Dict, Tuple
import spacy
from spacy.lang.en import English
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import warnings

warnings.filterwarnings('ignore')


class NLPProcessor:
    """Process text using spaCy and NLTK"""
    
    def __init__(self):
        """Initialize NLP models"""
        # Download required NLTK data
        self._download_nltk_data()
        
        # Load spaCy model
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("Downloading spaCy model...")
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
            self.nlp = spacy.load("en_core_web_sm")
        
        # Configure spaCy
        self.nlp.max_length = 2000000  # Increase max length for large contracts
        
        # Initialize NLTK components
        self.stop_words = set(stopwords.words('english'))
    
    def _download_nltk_data(self):
        """Download required NLTK data"""
        required_data = ['punkt', 'stopwords', 'averaged_perceptron_tagger', 'maxent_ne_chunker', 'words']
        
        for data in required_data:
            try:
                nltk.data.find(f'tokenizers/{data}')
            except LookupError:
                nltk.download(data, quiet=True)
    
    def process_text(self, text: str) -> Dict:
        """
        Process text and extract linguistic features
        
        Args:
            text: Input text to process
            
        Returns:
            Dict containing sentences, tokens, and other features
        """
        if not text or not text.strip():
            return {
                "sentences": [],
                "tokens": [],
                "entities": [],
                "noun_phrases": []
            }
        
        # Process with spaCy
        doc = self.nlp(text)
        
        # Extract sentences
        sentences = [sent.text.strip() for sent in doc.sents if sent.text.strip()]
        
        # Extract tokens
        tokens = [token.text for token in doc if not token.is_space]
        
        # Extract named entities
        entities = [
            {
                "text": ent.text,
                "label": ent.label_,
                "start": ent.start_char,
                "end": ent.end_char
            }
            for ent in doc.ents
        ]
        
        # Extract noun phrases
        noun_phrases = [chunk.text for chunk in doc.noun_chunks]
        
        return {
            "sentences": sentences,
            "tokens": tokens,
            "entities": entities,
            "noun_phrases": noun_phrases,
            "doc": doc  # Store spaCy doc for further processing
        }
    
    def extract_clauses(self, text: str) -> List[Dict]:
        """
        Extract contract clauses from text
        
        Returns:
            List of clause dictionaries with text and metadata
        """
        clauses = []
        
        # Split by numbered sections
        numbered_pattern = r'(?:^|\n)(\d+\.(?:\d+\.?)*)\s+([A-Z][^\n]+?)(?=\n\d+\.|\n[A-Z]{3,}|\Z)'
        matches = re.finditer(numbered_pattern, text, re.MULTILINE | re.DOTALL)
        
        for match in matches:
            clause_num = match.group(1)
            clause_text = match.group(2).strip()
            
            clauses.append({
                "clause_id": clause_num,
                "text": clause_text,
                "type": "numbered"
            })
        
        # Split by lettered sections
        lettered_pattern = r'(?:^|\n)([a-z]\))\s+([^\n]+?)(?=\n[a-z]\)|\n\d+\.|\Z)'
        matches = re.finditer(lettered_pattern, text, re.MULTILINE | re.DOTALL)
        
        for match in matches:
            clause_id = match.group(1)
            clause_text = match.group(2).strip()
            
            clauses.append({
                "clause_id": clause_id,
                "text": clause_text,
                "type": "lettered"
            })
        
        # If no structured clauses found, split by paragraphs
        if not clauses:
            paragraphs = text.split('\n\n')
            for i, para in enumerate(paragraphs):
                if para.strip() and len(para.strip()) > 50:  # Minimum length for a clause
                    clauses.append({
                        "clause_id": f"P{i+1}",
                        "text": para.strip(),
                        "type": "paragraph"
                    })
        
        return clauses
    
    def identify_clause_type(self, clause_text: str) -> str:
        """
        Identify the type of clause based on keywords
        
        Returns:
            Clause type as string
        """
        clause_lower = clause_text.lower()
        
        # Define keyword patterns for each clause type
        clause_patterns = {
            "Payment Terms": r'\b(payment|fee|compensation|remuneration|salary|invoice|due|price|cost)\b',
            "Termination": r'\b(terminat|cancel|end|expire|cessation|dissolve)\b',
            "Indemnity": r'\b(indemnif|hold harmless|defend|protect|compensate for loss)\b',
            "Confidentiality": r'\b(confidential|secret|proprietary|non-disclosure|nda)\b',
            "Intellectual Property": r'\b(intellectual property|copyright|patent|trademark|ip rights|ownership)\b',
            "Liability": r'\b(liabilit|responsib|damages|liable|accountable)\b',
            "Dispute Resolution": r'\b(dispute|arbitration|mediation|litigation|court|jurisdiction)\b',
            "Force Majeure": r'\b(force majeure|act of god|unforeseeable|beyond control)\b',
            "Warranties": r'\b(warrant|guarantee|represent|assure|certif)\b',
            "Non-compete": r'\b(non-compete|non-competition|restrictive covenant|compete)\b',
            "Duration": r'\b(term|duration|period|commence|effective date)\b',
            "Renewal": r'\b(renew|extend|continuation|auto-renew)\b',
        }
        
        # Check each pattern
        for clause_type, pattern in clause_patterns.items():
            if re.search(pattern, clause_lower):
                return clause_type
        
        return "General Provisions"
    
    def extract_obligations(self, text: str) -> Dict[str, List[str]]:
        """
        Extract obligations, rights, and prohibitions from text
        
        Returns:
            Dict with categories and extracted items
        """
        doc = self.nlp(text)
        
        obligations = []
        rights = []
        prohibitions = []
        
        # Patterns for obligations
        obligation_keywords = ['shall', 'must', 'will', 'agrees to', 'required to', 'obligated to']
        rights_keywords = ['may', 'entitled to', 'has the right', 'permitted to', 'can']
        prohibition_keywords = ['shall not', 'must not', 'prohibited', 'forbidden', 'may not']
        
        for sent in doc.sents:
            sent_text = sent.text.strip()
            sent_lower = sent_text.lower()
            
            # Check for prohibitions first (more specific)
            if any(keyword in sent_lower for keyword in prohibition_keywords):
                prohibitions.append(sent_text)
            # Then check for obligations
            elif any(keyword in sent_lower for keyword in obligation_keywords):
                obligations.append(sent_text)
            # Finally check for rights
            elif any(keyword in sent_lower for keyword in rights_keywords):
                rights.append(sent_text)
        
        return {
            "obligations": obligations,
            "rights": rights,
            "prohibitions": prohibitions
        }
    
    def detect_ambiguities(self, text: str) -> List[Dict]:
        """
        Detect ambiguous or vague language in contracts
        
        Returns:
            List of ambiguous phrases with context
        """
        ambiguities = []
        
        # Patterns for ambiguous language
        ambiguous_patterns = [
            r'\b(reasonable|appropriate|suitable|adequate|sufficient|substantial)\b',
            r'\b(may|might|could|should|would)\b',
            r'\b(approximately|about|around|roughly|nearly)\b',
            r'\b(promptly|timely|soon|expeditiously)\b',
            r'\b(best efforts|reasonable efforts)\b',
            r'\b(material|significant|substantial)\b',
        ]
        
        for pattern in ambiguous_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                # Get context (50 chars before and after)
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 50)
                context = text[start:end]
                
                ambiguities.append({
                    "phrase": match.group(0),
                    "context": context,
                    "position": match.start(),
                    "reason": "Vague or subjective term"
                })
        
        return ambiguities
    
    def extract_key_terms(self, text: str, top_n: int = 20) -> List[Tuple[str, int]]:
        """
        Extract key terms from text using TF-IDF-like approach
        
        Returns:
            List of (term, frequency) tuples
        """
        doc = self.nlp(text.lower())
        
        # Extract meaningful terms (nouns, proper nouns, adjectives)
        terms = []
        for token in doc:
            if (token.pos_ in ['NOUN', 'PROPN', 'ADJ'] and 
                not token.is_stop and 
                len(token.text) > 2 and
                token.is_alpha):
                terms.append(token.lemma_)
        
        # Count frequencies
        from collections import Counter
        term_freq = Counter(terms)
        
        return term_freq.most_common(top_n)
    
    def segment_into_sections(self, text: str) -> Dict[str, str]:
        """
        Segment contract into logical sections
        
        Returns:
            Dict with section names and content
        """
        sections = {}
        
        # Common section headers in contracts
        section_headers = [
            "DEFINITIONS",
            "PARTIES",
            "RECITALS",
            "TERMS AND CONDITIONS",
            "PAYMENT",
            "TERMINATION",
            "CONFIDENTIALITY",
            "INTELLECTUAL PROPERTY",
            "LIABILITY",
            "INDEMNITY",
            "DISPUTE RESOLUTION",
            "GENERAL PROVISIONS",
            "SIGNATURES"
        ]
        
        # Try to split by section headers
        current_section = "Preamble"
        current_content = []
        
        lines = text.split('\n')
        
        for line in lines:
            line_upper = line.strip().upper()
            
            # Check if line is a section header
            is_header = False
            for header in section_headers:
                if header in line_upper and len(line.strip()) < 100:
                    # Save previous section
                    if current_content:
                        sections[current_section] = '\n'.join(current_content)
                    
                    # Start new section
                    current_section = line.strip()
                    current_content = []
                    is_header = True
                    break
            
            if not is_header:
                current_content.append(line)
        
        # Save last section
        if current_content:
            sections[current_section] = '\n'.join(current_content)
        
        return sections if len(sections) > 1 else {"Full Document": text}
