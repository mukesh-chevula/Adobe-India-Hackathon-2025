"""
Adobe India Hackathon 2025 - Challenge 1A
Utility Classes - Font analysis and text processing utilities
"""

import re
from typing import Dict, List, Any, Set


class FontAnalyzer:
    """Analyzes font characteristics to identify document structure."""
    
    def __init__(self):
        """Initialize font analyzer."""
        self.font_cache = {}
    
    def analyze_font_distribution(self, text_dict: Dict) -> Dict[str, Any]:
        """
        Analyze the distribution of fonts in a document.
        
        Args:
            text_dict: PyMuPDF text dictionary
            
        Returns:
            Dictionary with font analysis results
        """
        font_sizes = []
        font_names = []
        font_flags = []
        
        if 'blocks' not in text_dict:
            return {'sizes': [], 'names': [], 'flags': []}
        
        for block in text_dict['blocks']:
            if 'lines' not in block:
                continue
                
            for line in block['lines']:
                if 'spans' not in line:
                    continue
                    
                for span in line['spans']:
                    font_sizes.append(span.get('size', 12))
                    font_names.append(span.get('font', 'default'))
                    font_flags.append(span.get('flags', 0))
        
        return {
            'sizes': font_sizes,
            'names': font_names,
            'flags': font_flags,
            'avg_size': sum(font_sizes) / len(font_sizes) if font_sizes else 12,
            'max_size': max(font_sizes) if font_sizes else 12,
            'min_size': min(font_sizes) if font_sizes else 12
        }
    
    def is_heading_font(self, font_size: float, font_flags: int, 
                       avg_size: float, threshold: float = 1.2) -> bool:
        """
        Determine if font characteristics suggest a heading.
        
        Args:
            font_size: Font size of the text
            font_flags: Font flags (bold, italic, etc.)
            avg_size: Average font size in the document
            threshold: Size threshold multiplier
            
        Returns:
            True if likely a heading font
        """
        # Size-based check
        size_ratio = font_size / avg_size if avg_size > 0 else 1
        is_large = size_ratio >= threshold
        
        # Bold text is often a heading
        is_bold = bool(font_flags & 2**4)
        
        return is_large or is_bold
    
    def get_font_hierarchy(self, font_sizes: List[float]) -> Dict[float, int]:
        """
        Create a hierarchy mapping from font sizes.
        
        Args:
            font_sizes: List of font sizes found in document
            
        Returns:
            Dictionary mapping font size to hierarchy level (1=largest, 2=second, etc.)
        """
        unique_sizes = sorted(set(font_sizes), reverse=True)
        hierarchy = {}
        
        for i, size in enumerate(unique_sizes[:3]):  # Only top 3 levels
            hierarchy[size] = i + 1
        
        return hierarchy


class TextProcessor:
    """Processes and analyzes text content for structure detection."""
    
    def __init__(self):
        """Initialize text processor."""
        self.stop_words = {
            'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 
            'with', 'by', 'from', 'about', 'into', 'through', 'during', 
            'before', 'after', 'above', 'below', 'up', 'down', 'out', 'off',
            'over', 'under', 'again', 'further', 'then', 'once'
        }
    
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text.
        
        Args:
            text: Raw text string
            
        Returns:
            Cleaned text string
        """
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove control characters
        text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
        
        # Normalize quotes and dashes
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace(''', "'").replace(''', "'")
        text = text.replace('–', '-').replace('—', '-')
        
        return text
    
    def is_likely_heading(self, text: str) -> bool:
        """
        Determine if text is likely a heading based on content analysis.
        
        Args:
            text: Text to analyze
            
        Returns:
            True if likely a heading
        """
        if not text or len(text.strip()) < 3:
            return False
        
        text = text.strip()
        
        # Check for heading patterns
        heading_patterns = [
            r'^\d+\.',                    # Numbered sections
            r'^[A-Z][A-Z\s]*$',          # ALL CAPS
            r'^[A-Z][a-z]+(\s[A-Z][a-z]+)*$',  # Title Case
            r'^(Chapter|Section|Part)\s+\d+',   # Chapter/Section markers
        ]
        
        for pattern in heading_patterns:
            if re.match(pattern, text):
                return True
        
        # Check text characteristics
        words = text.split()
        
        # Reasonable length for headings
        if not (2 <= len(words) <= 12):
            return False
        
        # Should not end with sentence punctuation
        if text.endswith(('.', '!', '?')):
            return False
        
        # Should not be mostly stop words
        non_stop_words = [w for w in words if w.lower() not in self.stop_words]
        if len(non_stop_words) < len(words) * 0.5:
            return False
        
        return True
    
    def extract_numbering(self, text: str) -> tuple:
        """
        Extract numbering information from heading text.
        
        Args:
            text: Heading text
            
        Returns:
            Tuple of (level, clean_text) where level is inferred hierarchy
        """
        # Pattern for multi-level numbering (1.2.3)
        match = re.match(r'^(\d+(?:\.\d+)*)\.\s*(.+)$', text)
        if match:
            numbering = match.group(1)
            clean_text = match.group(2)
            level = len(numbering.split('.'))
            return (level, clean_text)
        
        # Pattern for simple numbering (1.)
        match = re.match(r'^(\d+)\.\s*(.+)$', text)
        if match:
            clean_text = match.group(2)
            return (1, clean_text)
        
        # Pattern for letter numbering (A.)
        match = re.match(r'^([A-Z])\.\s*(.+)$', text)
        if match:
            clean_text = match.group(2)
            return (2, clean_text)
        
        # Pattern for roman numerals
        match = re.match(r'^([IVX]+)\.\s*(.+)$', text)
        if match:
            clean_text = match.group(2)
            return (1, clean_text)
        
        return (None, text)
    
    def calculate_text_complexity(self, text: str) -> float:
        """
        Calculate a complexity score for text.
        
        Args:
            text: Text to analyze
            
        Returns:
            Complexity score (higher = more complex)
        """
        if not text:
            return 0.0
        
        words = text.split()
        if not words:
            return 0.0
        
        # Average word length
        avg_word_length = sum(len(word) for word in words) / len(words)
        
        # Sentence count (rough estimate)
        sentences = len(re.split(r'[.!?]+', text))
        
        # Words per sentence
        words_per_sentence = len(words) / max(sentences, 1)
        
        # Complexity score
        complexity = (avg_word_length * 0.5) + (words_per_sentence * 0.3)
        
        return complexity
    
    def split_into_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences.
        
        Args:
            text: Input text
            
        Returns:
            List of sentences
        """
        if not text:
            return []
        
        # Simple sentence splitting
        sentences = re.split(r'[.!?]+', text)
        
        # Clean and filter sentences
        cleaned_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and len(sentence) > 3:
                cleaned_sentences.append(sentence)
        
        return cleaned_sentences
    
    def extract_keywords(self, text: str, top_k: int = 10) -> List[str]:
        """
        Extract keywords from text.
        
        Args:
            text: Input text
            top_k: Number of top keywords to return
            
        Returns:
            List of keywords
        """
        if not text:
            return []
        
        # Convert to lowercase and split into words
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        
        # Remove stop words
        words = [word for word in words if word not in self.stop_words]
        
        # Count word frequencies
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Sort by frequency and return top k
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        
        return [word for word, freq in sorted_words[:top_k]]
