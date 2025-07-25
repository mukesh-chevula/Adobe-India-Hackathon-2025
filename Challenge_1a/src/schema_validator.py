"""
Adobe India Hackathon 2025 - Challenge 1A
Schema Validator - Validates output JSON against the official schema
"""

import json
import jsonschema
from pathlib import Path
from typing import Dict, Any, List, Tuple

def colored_text(text: str, color_code: str) -> str:
    """Return colored text for terminal output."""
    return f"\033[{color_code}m{text}\033[0m"


class SchemaValidator:
    """Validates Challenge 1A output against the official schema."""
    
    def __init__(self):
        """Initialize the schema validator."""
        # Official schema from the hackathon
        self.official_schema = {
            "$schema": "http://json-schema.org/draft-04/schema#",
            "type": "object",
            "properties": {
                "title": {
                    "type": "string"
                },
                "outline": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "level": {
                                "type": "string"
                            },
                            "text": {
                                "type": "string"
                            },
                            "page": {
                                "type": "integer"
                            }
                        },
                        "required": [
                            "level",
                            "text",
                            "page"
                        ]
                    }
                }
            },
            "required": [
                "title",
                "outline"
            ]
        }
    
    def validate_json_file(self, json_path: Path) -> Tuple[bool, List[str]]:
        """
        Validate a JSON file against the official schema.
        
        Args:
            json_path: Path to the JSON file to validate
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return self.validate_data(data)
            
        except json.JSONDecodeError as e:
            return False, [f"Invalid JSON format: {str(e)}"]
        except Exception as e:
            return False, [f"Error reading file: {str(e)}"]
    
    def validate_data(self, data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate data against the official schema.
        
        Args:
            data: Dictionary containing the JSON data
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        try:
            # Basic schema validation
            jsonschema.validate(data, self.official_schema)
            
            # Additional custom validations
            custom_errors = self._custom_validations(data)
            errors.extend(custom_errors)
            
            if errors:
                return False, errors
            else:
                return True, []
                
        except jsonschema.ValidationError as e:
            errors.append(f"Schema validation error: {e.message}")
            return False, errors
        except Exception as e:
            errors.append(f"Validation error: {str(e)}")
            return False, errors
    
    def _custom_validations(self, data: Dict[str, Any]) -> List[str]:
        """Perform additional custom validations."""
        errors = []
        
        # Validate title
        title = data.get('title', '')
        if not title or not isinstance(title, str):
            errors.append("Title must be a non-empty string")
        elif len(title.strip()) < 3:
            errors.append("Title should be at least 3 characters long")
        
        # Validate outline
        outline = data.get('outline', [])
        if not isinstance(outline, list):
            errors.append("Outline must be an array")
        elif len(outline) == 0:
            errors.append("Outline should contain at least one heading")
        else:
            # Validate each outline item
            for i, item in enumerate(outline):
                item_errors = self._validate_outline_item(item, i)
                errors.extend(item_errors)
        
        return errors
    
    def _validate_outline_item(self, item: Dict[str, Any], index: int) -> List[str]:
        """Validate individual outline item."""
        errors = []
        
        # Check level
        level = item.get('level', '')
        valid_levels = ['H1', 'H2', 'H3']
        if level not in valid_levels:
            errors.append(f"Item {index}: level must be one of {valid_levels}, got '{level}'")
        
        # Check text
        text = item.get('text', '')
        if not text or not isinstance(text, str):
            errors.append(f"Item {index}: text must be a non-empty string")
        elif len(text.strip()) < 3:
            errors.append(f"Item {index}: text should be at least 3 characters long")
        
        # Check page
        page = item.get('page')
        if not isinstance(page, int):
            errors.append(f"Item {index}: page must be an integer")
        elif page < 1:
            errors.append(f"Item {index}: page must be a positive integer (got {page})")
        
        return errors
    
    def get_validation_report(self, json_path: Path) -> str:
        """
        Get a detailed validation report for a JSON file.
        
        Args:
            json_path: Path to the JSON file
            
        Returns:
            Formatted validation report string
        """
        is_valid, errors = self.validate_json_file(json_path)
        
        report = f"{colored_text('SCHEMA VALIDATION REPORT', '36')} for: {json_path.name}\n"
        report += "=" * 60 + "\n\n"
        
        if is_valid:
            report += f"{colored_text('VALIDATION PASSED', '32')}\n"
            report += "The JSON file conforms to the official Challenge 1A schema.\n"
            
            # Load and show basic stats
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                outline = data.get('outline', [])
                level_counts = {}
                for item in outline:
                    level = item.get('level', 'Unknown')
                    level_counts[level] = level_counts.get(level, 0) + 1
                
                report += f"\n{colored_text('Statistics:', '34')}\n"
                report += f"   Title: {data.get('title', 'N/A')}\n"
                report += f"   Total headings: {len(outline)}\n"
                
                for level in ['H1', 'H2', 'H3']:
                    count = level_counts.get(level, 0)
                    if count > 0:
                        report += f"   {level} headings: {count}\n"
                
                if outline:
                    pages = [item.get('page', 0) for item in outline]
                    report += f"   Page range: {min(pages)} - {max(pages)}\n"
                
            except Exception as e:
                report += f"Note: Could not load statistics - {str(e)}\n"
        
        else:
            report += f"{colored_text('VALIDATION FAILED', '31')}\n"
            report += f"Found {len(errors)} error(s):\n\n"
            
            for i, error in enumerate(errors, 1):
                report += f"   {i}. {error}\n"
            
            report += f"\n{colored_text('Tips:', '33')}\n"
            report += f"   - Ensure 'title' is a non-empty string\n"
            report += f"   - Ensure 'outline' is an array of heading objects\n"
            report += f"   - Each heading must have 'level' (H1/H2/H3), 'text' (string), and 'page' (integer)\n"
        
        report += "\n" + "=" * 60
        return report


def validate_output_directory(output_dir: Path) -> None:
    """Validate all JSON files in the output directory."""
    validator = SchemaValidator()
    
    json_files = list(output_dir.glob("*.json"))
    
    if not json_files:
        print("No JSON files found in output directory.")
        return
    
    print(f"{colored_text('Validating', '36')} {len(json_files)} JSON file(s)...")
    print("=" * 70)
    
    valid_count = 0
    
    for json_file in json_files:
        print(f"\n{colored_text('Checking:', '34')} {json_file.name}")
        is_valid, errors = validator.validate_json_file(json_file)
        
        if is_valid:
            print(f"   {colored_text('Valid', '32')}")
            valid_count += 1
        else:
            print(f"   {colored_text('Invalid', '31')}")
            for error in errors[:3]:  # Show first 3 errors
                print(f"      - {error}")
            if len(errors) > 3:
                print(f"      ... and {len(errors) - 3} more error(s)")
    
    print(f"\n{'='*70}")
    print(f"{colored_text('Summary:', '34')} {valid_count}/{len(json_files)} files passed validation")
    
    if valid_count == len(json_files):
        print(f"{colored_text('All files conform to the official schema!', '32')}")
    else:
        print(f"{colored_text(f'{len(json_files) - valid_count} file(s) need fixing', '33')}")


if __name__ == "__main__":
    # Validate output directory
    output_dir = Path("/app/output")
    if not output_dir.exists():
        output_dir = Path("output")
    
    if output_dir.exists():
        validate_output_directory(output_dir)
    else:
        print("Output directory not found.")
