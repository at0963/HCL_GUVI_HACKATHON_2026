"""
Entity Extractor Module
Extracts named entities specific to legal contracts
"""
import re
from typing import List, Dict
from datetime import datetime
import spacy


class EntityExtractor:
    """Extract contract-specific entities using pattern matching and NER"""

    def __init__(self, nlp):
        self.nlp = nlp
    
    def extract_all_entities(self, text: str) -> Dict[str, List]:
        """
        Extract all contract entities
        
        Returns:
            Dict with entity types and extracted values
        """
        entities = {
            "parties": self.extract_parties(text),
            "dates": self.extract_dates(text),
            "amounts": self.extract_amounts(text),
            "durations": self.extract_durations(text),
            "jurisdictions": self.extract_jurisdictions(text),
            "emails": self.extract_emails(text),
            "phone_numbers": self.extract_phone_numbers(text),
            "addresses": self.extract_addresses(text)
        }
        
        return entities
    
    def extract_parties(self, text: str) -> List[Dict]:
        """Extract party names from contract"""
        parties = []
        
        # Pattern 1: "between X and Y"
        pattern1 = r'(?:between|by and between)\s+([A-Z][^,\n]+?)\s+(?:and|&)\s+([A-Z][^,\n]+?)(?:,|\.|;|\n)'
        matches = re.finditer(pattern1, text, re.IGNORECASE)
        for match in matches:
            parties.append({
                "name": match.group(1).strip(),
                "role": "Party 1",
                "type": "organization/individual"
            })
            parties.append({
                "name": match.group(2).strip(),
                "role": "Party 2",
                "type": "organization/individual"
            })
        
        # Pattern 2: "Party 1" or "First Party"
        party_pattern = r'(?:Party\s+(?:1|One|First)|First Party)[:\s]+([A-Z][^\n,;]+)'
        matches = re.finditer(party_pattern, text, re.IGNORECASE)
        for match in matches:
            parties.append({
                "name": match.group(1).strip(),
                "role": "First Party",
                "type": "organization/individual"
            })
        
        # Pattern 3: "hereinafter referred to as"
        referred_pattern = r'([A-Z][^,\(\n]+?)\s+\(hereinafter referred to as[^)]+\)'
        matches = re.finditer(referred_pattern, text)
        for match in matches:
            parties.append({
                "name": match.group(1).strip(),
                "role": "Contracting Party",
                "type": "organization/individual"
            })
        
        # Use spaCy NER for organizations and persons
        doc = self.nlp(text[:5000])  # Process first 5000 chars
        for ent in doc.ents:
            if ent.label_ in ["ORG", "PERSON"]:
                parties.append({
                    "name": ent.text,
                    "role": "Identified Entity",
                    "type": ent.label_
                })
        
        # Deduplicate
        seen = set()
        unique_parties = []
        for party in parties:
            name_normalized = party["name"].lower().strip()
            if name_normalized not in seen and len(name_normalized) > 3:
                seen.add(name_normalized)
                unique_parties.append(party)
        
        return unique_parties
    
    def extract_dates(self, text: str) -> List[Dict]:
        """Extract dates from contract"""
        dates = []
        
        # Pattern 1: DD/MM/YYYY or MM/DD/YYYY
        pattern1 = r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b'
        matches = re.finditer(pattern1, text)
        for match in matches:
            dates.append({
                "date": match.group(1),
                "format": "numeric",
                "context": self._get_context(text, match.start(), match.end())
            })
        
        # Pattern 2: Month DD, YYYY
        pattern2 = r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b'
        matches = re.finditer(pattern2, text, re.IGNORECASE)
        for match in matches:
            dates.append({
                "date": match.group(0),
                "format": "text",
                "context": self._get_context(text, match.start(), match.end())
            })
        
        # Pattern 3: DD Month YYYY (Indian format)
        pattern3 = r'\b\d{1,2}(?:st|nd|rd|th)?\s+(January|February|March|April|May|June|July|August|September|October|November|December),?\s+\d{4}\b'
        matches = re.finditer(pattern3, text, re.IGNORECASE)
        for match in matches:
            dates.append({
                "date": match.group(0),
                "format": "text_indian",
                "context": self._get_context(text, match.start(), match.end())
            })
        
        # Use spaCy for date entities
        doc = self.nlp(text[:5000])
        for ent in doc.ents:
            if ent.label_ == "DATE":
                dates.append({
                    "date": ent.text,
                    "format": "ner",
                    "context": self._get_context(text, ent.start_char, ent.end_char)
                })
        
        return dates
    
    def extract_amounts(self, text: str) -> List[Dict]:
        """Extract monetary amounts from contract"""
        amounts = []
        
        # Indian Rupee patterns
        inr_patterns = [
            r'(?:Rs\.?|INR|₹)\s*(\d+(?:,\d+)*(?:\.\d+)?)\s*(?:Lakhs?|Crores?|Thousands?)?',
            r'(\d+(?:,\d+)*(?:\.\d+)?)\s*(?:Rupees|INR|Rs\.?)',
        ]
        
        for pattern in inr_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                amounts.append({
                    "amount": match.group(0),
                    "currency": "INR",
                    "value": match.group(1),
                    "context": self._get_context(text, match.start(), match.end())
                })
        
        # USD and other currencies
        currency_pattern = r'(?:USD|US\$|\$|EUR|€|GBP|£)\s*(\d+(?:,\d+)*(?:\.\d+)?)'
        matches = re.finditer(currency_pattern, text)
        for match in matches:
            amounts.append({
                "amount": match.group(0),
                "currency": "USD/Other",
                "value": match.group(1),
                "context": self._get_context(text, match.start(), match.end())
            })
        
        # Use spaCy for money entities
        doc = self.nlp(text[:5000])
        for ent in doc.ents:
            if ent.label_ == "MONEY":
                amounts.append({
                    "amount": ent.text,
                    "currency": "detected",
                    "value": ent.text,
                    "context": self._get_context(text, ent.start_char, ent.end_char)
                })
        
        return amounts
    
    def extract_durations(self, text: str) -> List[Dict]:
        """Extract time durations and periods"""
        durations = []
        
        # Pattern: X years/months/days/weeks
        duration_pattern = r'\b(\d+)\s+(year|month|week|day|hour)s?\b'
        matches = re.finditer(duration_pattern, text, re.IGNORECASE)
        for match in matches:
            durations.append({
                "duration": match.group(0),
                "value": match.group(1),
                "unit": match.group(2),
                "context": self._get_context(text, match.start(), match.end())
            })
        
        # Pattern: Term of X
        term_pattern = r'(?:term|period|duration)\s+of\s+(\d+\s+(?:year|month|week|day)s?)'
        matches = re.finditer(term_pattern, text, re.IGNORECASE)
        for match in matches:
            durations.append({
                "duration": match.group(1),
                "value": match.group(1).split()[0],
                "unit": match.group(1).split()[1],
                "context": self._get_context(text, match.start(), match.end())
            })
        
        return durations
    
    def extract_jurisdictions(self, text: str) -> List[Dict]:
        """Extract jurisdiction and governing law information"""
        jurisdictions = []
        
        # Indian states and cities
        indian_locations = [
            "Mumbai", "Delhi", "Bangalore", "Bengaluru", "Chennai", "Kolkata",
            "Hyderabad", "Pune", "Ahmedabad", "Jaipur", "Maharashtra", "Karnataka",
            "Tamil Nadu", "Gujarat", "Rajasthan", "West Bengal", "Telangana",
            "India", "Indian"
        ]
        
        # Jurisdiction patterns
        jurisdiction_pattern = r'(?:jurisdiction|courts? of|governed by (?:the )?laws? of)\s+([A-Z][^,\.\n]+)'
        matches = re.finditer(jurisdiction_pattern, text, re.IGNORECASE)
        for match in matches:
            jurisdictions.append({
                "jurisdiction": match.group(1).strip(),
                "type": "specified",
                "context": self._get_context(text, match.start(), match.end())
            })
        
        # Look for Indian locations
        for location in indian_locations:
            pattern = r'\b' + location + r'\b'
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                jurisdictions.append({
                    "jurisdiction": location,
                    "type": "location",
                    "context": self._get_context(text, match.start(), match.end())
                })
        
        # Use spaCy for GPE (Geopolitical Entity)
        doc = self.nlp(text[:5000])
        for ent in doc.ents:
            if ent.label_ == "GPE":
                jurisdictions.append({
                    "jurisdiction": ent.text,
                    "type": "ner",
                    "context": self._get_context(text, ent.start_char, ent.end_char)
                })
        
        # Deduplicate
        seen = set()
        unique_jurisdictions = []
        for jur in jurisdictions:
            jur_normalized = jur["jurisdiction"].lower().strip()
            if jur_normalized not in seen:
                seen.add(jur_normalized)
                unique_jurisdictions.append(jur)
        
        return unique_jurisdictions
    
    def extract_emails(self, text: str) -> List[str]:
        """Extract email addresses"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        return list(set(emails))
    
    def extract_phone_numbers(self, text: str) -> List[str]:
        """Extract phone numbers (Indian and international)"""
        phone_patterns = [
            r'\+91[\s-]?\d{10}',  # Indian international format
            r'\d{10}',  # Indian 10-digit
            r'\+\d{1,3}[\s-]?\(?\d{1,4}\)?[\s-]?\d{1,4}[\s-]?\d{1,9}',  # International
        ]
        
        phones = []
        for pattern in phone_patterns:
            matches = re.findall(pattern, text)
            phones.extend(matches)
        
        return list(set(phones))
    
    def extract_addresses(self, text: str) -> List[str]:
        """Extract addresses using NER"""
        doc = self.nlp(text[:5000])
        addresses = []
        
        for ent in doc.ents:
            if ent.label_ in ["GPE", "LOC", "FAC"]:
                # Get surrounding context to capture full address
                start = max(0, ent.start_char - 100)
                end = min(len(text), ent.end_char + 100)
                context = text[start:end]
                
                # Look for address patterns in context
                address_pattern = r'[^.]+(?:Street|Road|Avenue|Lane|Nagar|Colony|Block|Floor)[^.]*'
                addr_matches = re.findall(address_pattern, context, re.IGNORECASE)
                addresses.extend(addr_matches)
        
        return list(set(addresses))
    
    def _get_context(self, text: str, start: int, end: int, window: int = 50) -> str:
        """Get context around extracted entity"""
        context_start = max(0, start - window)
        context_end = min(len(text), end + window)
        return text[context_start:context_end].strip()
