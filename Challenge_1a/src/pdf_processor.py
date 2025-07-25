"""
Adobe India Hackathon 2025 - Challenge 1A
PDF Processor - Main PDF processing and coordination module
"""

import json
import fitz  # PyMuPDF
from pathlib import Path
from typing import Dict, List, Any
from outline_extractor import OutlineExtractor

def colored_text(text: str, color_code: str) -> str:
    """Return colored text for terminal output."""
    return f"\033[{color_code}m{text}\033[0m"


class PDFProcessor:
    """Main PDF processing class that coordinates outline extraction."""
    
    def __init__(self):
        """Initialize the PDF processor."""
        self.outline_extractor = OutlineExtractor()
    
    def extract_outline(self, pdf_path: Path) -> Dict[str, Any]:
        """
        Extract structured outline from a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dictionary containing title and outline structure
        """
        try:
            # Open PDF document
            doc = fitz.open(pdf_path)
            
            # Extract document metadata and content
            metadata = doc.metadata
            page_count = len(doc)
            
            print(f"  Document info: {page_count} pages")
            
            # Extract text content from all pages
            pages_content = []
            for page_num in range(page_count):
                page = doc[page_num]
                
                # Extract text with font information
                text_dict = page.get_text("dict")
                pages_content.append({
                    'page_num': page_num + 1,
                    'text_dict': text_dict,
                    'plain_text': page.get_text()
                })
            
            # Close document
            doc.close()
            
            # Extract title and outline using the specialized extractor
            title = self.outline_extractor.extract_title(metadata, pages_content)
            outline = self.outline_extractor.extract_headings(pages_content)
            
            return {
                "title": title,
                "outline": outline
            }
            
        except Exception as e:
            print(f"Error processing PDF {pdf_path}: {str(e)}")
            # Return default structure on error
            return {
                "title": pdf_path.stem.replace('_', ' ').title(),
                "outline": []
            }
    
    def save_result(self, result: Dict[str, Any], output_path: Path) -> None:
        """
        Save the extraction result to a JSON file with validation.
        
        Args:
            result: The extraction result dictionary
            output_path: Path where to save the JSON file
        """
        try:
            # Validate the result against schema before saving
            is_valid, errors = self._validate_result(result)
            
            if not is_valid:
                print(f"  {colored_text('Schema validation warnings', '33')} for {output_path.name}:")
                for error in errors[:3]:  # Show first 3 errors
                    print(f"     - {error}")
                if len(errors) > 3:
                    print(f"     ... and {len(errors) - 3} more warning(s)")
            
            # Save the JSON file
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
                
            if is_valid:
                print(f"  {colored_text('Schema validation passed', '32')}")
            
        except Exception as e:
            print(f"Error saving result to {output_path}: {str(e)}")
            raise
    
    def _validate_result(self, result: Dict[str, Any]) -> tuple:
        """
        Validate result against Challenge 1A schema.
        
        Args:
            result: The result dictionary to validate
            
        Returns:
            Tuple of (is_valid, error_list)
        """
        errors = []
        
        # Check title
        title = result.get('title', '')
        if not title or not isinstance(title, str) or len(title.strip()) < 3:
            errors.append("Title must be a non-empty string with at least 3 characters")
        
        # Check outline
        outline = result.get('outline', [])
        if not isinstance(outline, list):
            errors.append("Outline must be an array")
        else:
            for i, item in enumerate(outline):
                if not isinstance(item, dict):
                    errors.append(f"Outline item {i} must be an object")
                    continue
                
                # Check required fields
                level = item.get('level', '')
                text = item.get('text', '')
                page = item.get('page')
                
                if level not in ['H1', 'H2', 'H3']:
                    errors.append(f"Item {i}: level must be H1, H2, or H3")
                
                if not text or not isinstance(text, str):
                    errors.append(f"Item {i}: text must be a non-empty string")
                
                if not isinstance(page, int) or page < 1:
                    errors.append(f"Item {i}: page must be a positive integer")
        
        return len(errors) == 0, errors
