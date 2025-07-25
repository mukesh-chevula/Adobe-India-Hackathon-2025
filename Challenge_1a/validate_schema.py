#!/usr/bin/env python3
"""
Adobe India Hackathon 2025 - Challenge 1A
Standalone Schema Validation Tool

This script validates Challenge 1A output files against the official schema.
"""

import json
import sys
from pathlib import Path

def colored_text(text: str, color_code: str) -> str:
    """Return colored text for terminal output."""
    return f"\033[{color_code}m{text}\033[0m"

# Add src to Python path
sys.path.insert(0, 'src')

try:
    from schema_validator import SchemaValidator, validate_output_directory
except ImportError:
    print(f"{colored_text('Error: Could not import schema_validator module', '31')}")
    print("Make sure you're running this from the Challenge_1a directory")
    sys.exit(1)


def main():
    """Main validation function."""
    print(f"{colored_text('Challenge 1A Schema Validation Tool', '36')}")
    print("=" * 50)
    
    output_dir = Path("output")
    
    if not output_dir.exists():
        print(f"{colored_text('Output directory not found!', '31')}")
        print("Please ensure you have an 'output' directory with JSON files.")
        sys.exit(1)
    
    # Validate all files in output directory
    validate_output_directory(output_dir)


if __name__ == "__main__":
    main()
