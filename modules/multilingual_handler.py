"""
Multilingual Handler Module
Handles Hindi and multilingual contract processing
"""
import re
from typing import Dict, List, Optional
from langdetect import detect, detect_langs
import warnings

warnings.filterwarnings('ignore')


class MultilingualHandler:
    """Handle multilingual contracts (English and Hindi)"""
    
    def __init__(self):
        """Initialize multilingual handler"""
        self.supported_languages = ['en', 'hi']
        
        # Hindi to English translation mappings for common contract terms
        self.hindi_terms = {
            # Contract terms
            "अनुबंध": "contract",
            "समझौता": "agreement",
            "पक्ष": "party",
            "पक्षकार": "parties",
            "खंड": "clause",
            "धारा": "section",
            
            # Legal terms
            "कानून": "law",
            "नियम": "rule",
            "दायित्व": "liability",
            "क्षतिपूर्ति": "indemnity",
            "गोपनीय": "confidential",
            "गोपनीयता": "confidentiality",
            
            # Financial terms
            "भुगतान": "payment",
            "राशि": "amount",
            "शुल्क": "fee",
            "रुपये": "rupees",
            "मूल्य": "price",
            
            # Time terms
            "दिनांक": "date",
            "अवधि": "duration",
            "समय": "time",
            "वर्ष": "year",
            "महीना": "month",
            
            # Action terms
            "समाप्ति": "termination",
            "नवीनीकरण": "renewal",
            "रद्द": "cancel",
            "निलंबन": "suspension",
            
            # Rights and obligations
            "अधिकार": "right",
            "कर्तव्य": "duty",
            "दायित्व": "obligation",
            "जिम्मेदारी": "responsibility"
        }
        
        # Devanagari number mapping
        self.devanagari_numbers = {
            '०': '0', '१': '1', '२': '2', '३': '3', '४': '4',
            '५': '5', '६': '6', '७': '7', '८': '8', '९': '9'
        }
    
    def detect_language(self, text: str) -> Dict:
        """
        Detect language(s) in the text
        
        Returns:
            Dict with detected languages and confidence
        """
        if not text or not text.strip():
            return {
                "primary_language": "unknown",
                "is_multilingual": False,
                "languages": []
            }
        
        try:
            # Detect primary language
            primary_lang = detect(text)
            
            # Detect all languages with probabilities
            lang_probs = detect_langs(text)
            
            languages = [
                {
                    "lang": str(lang_prob).split(':')[0],
                    "confidence": float(str(lang_prob).split(':')[1])
                }
                for lang_prob in lang_probs
            ]
            
            # Check if multilingual
            is_multilingual = len(languages) > 1 and languages[1]["confidence"] > 0.2
            
            # Check for Hindi specifically
            has_hindi = self._contains_devanagari(text)
            has_english = self._contains_latin(text)
            
            return {
                "primary_language": primary_lang,
                "is_multilingual": is_multilingual or (has_hindi and has_english),
                "has_hindi": has_hindi,
                "has_english": has_english,
                "languages": languages
            }
        
        except Exception as e:
            # Fallback to simple detection
            has_hindi = self._contains_devanagari(text)
            has_english = self._contains_latin(text)
            
            return {
                "primary_language": "hi" if has_hindi else "en",
                "is_multilingual": has_hindi and has_english,
                "has_hindi": has_hindi,
                "has_english": has_english,
                "languages": [],
                "error": str(e)
            }
    
    def normalize_text(self, text: str) -> str:
        """
        Normalize multilingual text for processing
        
        Returns:
            Normalized text
        """
        # Convert Devanagari numbers to Arabic
        normalized = self._convert_devanagari_numbers(text)
        
        # Normalize whitespace
        normalized = re.sub(r'\s+', ' ', normalized)
        
        # Remove special characters that might cause issues
        normalized = normalized.replace('\u200b', '')  # Zero-width space
        normalized = normalized.replace('\ufeff', '')  # BOM
        
        return normalized.strip()
    
    def translate_hindi_terms(self, text: str) -> Dict:
        """
        Identify and translate common Hindi legal terms to English
        
        Returns:
            Dict with translations and annotated text
        """
        translations = {}
        annotated_text = text
        
        for hindi_term, english_term in self.hindi_terms.items():
            if hindi_term in text:
                translations[hindi_term] = english_term
                # Add English translation in parentheses
                annotated_text = annotated_text.replace(
                    hindi_term,
                    f"{hindi_term} ({english_term})"
                )
        
        return {
            "original_text": text,
            "annotated_text": annotated_text,
            "translations": translations,
            "terms_found": len(translations)
        }
    
    def extract_bilingual_clauses(self, text: str) -> List[Dict]:
        """
        Extract clauses that may be in both languages
        
        Returns:
            List of clause dictionaries with language info
        """
        # Split into paragraphs
        paragraphs = text.split('\n\n')
        
        clauses = []
        
        for i, para in enumerate(paragraphs):
            if not para.strip():
                continue
            
            lang_info = self.detect_language(para)
            
            clauses.append({
                "clause_id": f"C{i+1}",
                "text": para.strip(),
                "primary_language": lang_info["primary_language"],
                "is_multilingual": lang_info["is_multilingual"],
                "has_hindi": lang_info.get("has_hindi", False),
                "has_english": lang_info.get("has_english", False)
            })
        
        return clauses
    
    def generate_bilingual_summary(self, summary_en: str) -> Dict:
        """
        Generate summary in both English and Hindi (English + key Hindi terms)
        
        Note: Full machine translation is not included to avoid external APIs.
        This provides English summary with Hindi term annotations.
        
        Returns:
            Dict with English summary and Hindi term highlights
        """
        # Identify if English summary contains any translatable terms
        hindi_annotated = summary_en
        
        # Reverse mapping: English to Hindi
        en_to_hi = {v: k for k, v in self.hindi_terms.items()}
        
        for en_term, hi_term in en_to_hi.items():
            # Add Hindi translation for key terms
            pattern = r'\b' + re.escape(en_term) + r'\b'
            if re.search(pattern, hindi_annotated, re.IGNORECASE):
                hindi_annotated = re.sub(
                    pattern,
                    f"{en_term} ({hi_term})",
                    hindi_annotated,
                    flags=re.IGNORECASE,
                    count=1  # Only annotate first occurrence
                )
        
        return {
            "english_summary": summary_en,
            "annotated_summary": hindi_annotated,
            "note": "Key legal terms are shown in Hindi (हिंदी) for reference"
        }
    
    def identify_mixed_content(self, text: str) -> Dict:
        """
        Identify sections with mixed language content
        
        Returns:
            Analysis of mixed content
        """
        # Split into sentences
        sentences = re.split(r'[।\.\n]', text)
        
        mixed_sentences = []
        hindi_sentences = []
        english_sentences = []
        
        for sentence in sentences:
            if not sentence.strip():
                continue
            
            has_hindi = self._contains_devanagari(sentence)
            has_english = self._contains_latin(sentence)
            
            if has_hindi and has_english:
                mixed_sentences.append(sentence.strip())
            elif has_hindi:
                hindi_sentences.append(sentence.strip())
            elif has_english:
                english_sentences.append(sentence.strip())
        
        return {
            "total_sentences": len(sentences),
            "mixed_language_sentences": len(mixed_sentences),
            "hindi_only_sentences": len(hindi_sentences),
            "english_only_sentences": len(english_sentences),
            "mixed_examples": mixed_sentences[:3],  # First 3 examples
            "primary_language": "Mixed" if mixed_sentences else (
                "Hindi" if len(hindi_sentences) > len(english_sentences) else "English"
            )
        }
    
    def _contains_devanagari(self, text: str) -> bool:
        """Check if text contains Devanagari (Hindi) script"""
        devanagari_pattern = r'[\u0900-\u097F]'
        return bool(re.search(devanagari_pattern, text))
    
    def _contains_latin(self, text: str) -> bool:
        """Check if text contains Latin (English) script"""
        latin_pattern = r'[a-zA-Z]'
        return bool(re.search(latin_pattern, text))
    
    def _convert_devanagari_numbers(self, text: str) -> str:
        """Convert Devanagari numerals to Arabic"""
        for devanagari, arabic in self.devanagari_numbers.items():
            text = text.replace(devanagari, arabic)
        return text
    
    def extract_hindi_legal_phrases(self, text: str) -> List[Dict]:
        """
        Extract common Hindi legal phrases
        
        Returns:
            List of identified phrases with translations
        """
        phrases = []
        
        # Common Hindi legal phrases
        legal_phrases = {
            "यह समझौता": "This agreement",
            "पक्षकारों के बीच": "Between the parties",
            "निम्नलिखित शर्तों": "Following terms",
            "कानूनी रूप से बाध्यकारी": "Legally binding",
            "पारस्परिक सहमति": "Mutual consent",
            "उल्लंघन की स्थिति में": "In case of breach",
            "न्यायालय का अधिकार क्षेत्र": "Court jurisdiction",
            "विवाद समाधान": "Dispute resolution"
        }
        
        for hindi_phrase, english_phrase in legal_phrases.items():
            if hindi_phrase in text:
                # Find position
                position = text.find(hindi_phrase)
                phrases.append({
                    "hindi": hindi_phrase,
                    "english": english_phrase,
                    "position": position,
                    "context": text[max(0, position-50):min(len(text), position+len(hindi_phrase)+50)]
                })
        
        return phrases
    
    def create_glossary(self, text: str) -> Dict:
        """
        Create a glossary of Hindi-English terms found in the document
        
        Returns:
            Glossary dictionary
        """
        glossary = {}
        
        for hindi_term, english_term in self.hindi_terms.items():
            if hindi_term in text:
                count = text.count(hindi_term)
                glossary[hindi_term] = {
                    "english": english_term,
                    "occurrences": count,
                    "category": self._categorize_term(english_term)
                }
        
        return {
            "total_terms": len(glossary),
            "terms": glossary,
            "note": "This glossary shows Hindi legal terms found in your document"
        }
    
    def _categorize_term(self, term: str) -> str:
        """Categorize legal term"""
        categories = {
            "contract": ["contract", "agreement", "clause", "section"],
            "financial": ["payment", "amount", "fee", "price", "rupees"],
            "legal": ["law", "rule", "liability", "indemnity"],
            "temporal": ["date", "duration", "time", "year", "month"],
            "action": ["termination", "renewal", "cancel", "suspension"],
            "rights": ["right", "duty", "obligation", "responsibility"]
        }
        
        for category, terms in categories.items():
            if term in terms:
                return category
        
        return "general"
