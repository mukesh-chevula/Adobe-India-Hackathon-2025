#!/usr/bin/env python3
"""
Schema validation script for Challenge 1B output
Adobe India Hackathon 2025
"""

import json
import sys
from pathlib import Path
import jsonschema
from typing import List

def color_text(text, color):
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "reset": "\033[0m"
    }
    return f"{colors.get(color, '')}{text}{colors['reset']}"

def get_schema_path() -> Path:
    return Path(__file__).parent / "challenge1b_output_schema.json"

def read_json_file(file_path: Path) -> dict:
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def print_schema_load_error(e, schema_path):
    print(color_text(f"Schema file error: {e} ({schema_path})", "red"))
    sys.exit(1)

def load_schema() -> dict:
    schema_path = get_schema_path()
    try:
        return read_json_file(schema_path)
    except FileNotFoundError as e:
        print_schema_load_error("not found", schema_path)
    except json.JSONDecodeError as e:
        print_schema_load_error(f"invalid JSON: {e}", schema_path)

def check_sections_and_subsections(output_data: dict):
    sections = output_data.get('extracted_sections', [])
    subsections = output_data.get('subsection_analysis', [])
    if not sections and not subsections:
        print(color_text("  Warning: No sections or subsections found", "yellow"))

def check_importance_ranks(sections):
    ranks = [s.get('importance_rank', 0) for s in sections]
    if ranks and ranks != sorted(ranks):
        print(color_text("  Warning: Importance ranks are not sequential", "yellow"))

def semantic_checks(output_data: dict):
    check_sections_and_subsections(output_data)
    sections = output_data.get('extracted_sections', [])
    if sections:
        check_importance_ranks(sections)

def validate_json_schema(output_data: dict, schema: dict):
    try:
        jsonschema.validate(instance=output_data, schema=schema)
        return True, ""
    except jsonschema.ValidationError as e:
        return False, f"{e.message}\n      Path: {' -> '.join(str(p) for p in e.path)}"

def validate_output_file(file_path: Path, schema: dict) -> bool:
    try:
        output_data = read_json_file(file_path)
    except FileNotFoundError:
        print(color_text(f"  File not found: {file_path}", "red"))
        return False
    except json.JSONDecodeError as e:
        print(color_text(f"  Invalid JSON: {e}", "red"))
        return False

    valid, error_msg = validate_json_schema(output_data, schema)
    if not valid:
        print(color_text(f"  Schema validation error: {error_msg}", "red"))
        return False

    semantic_checks(output_data)
    print(color_text("  Valid JSON structure", "green"))
    print(color_text("  Perfect compliance!", "blue"))
    return True

def get_output_patterns() -> List[str]:
    return [
        "challenge1b_output*.json",
        "*output*.json",
        "round_1b*.json"
    ]

def find_output_files(directory: Path) -> List[Path]:
    files = []
    for pattern in get_output_patterns():
        files.extend(directory.glob(pattern))
    return sorted(set(files))

def print_summary(valid_files, total_files):
    print("\n" + "=" * 40)
    print(color_text("Validation Summary:", "blue"))
    print(f"   Valid files: {color_text(f'{valid_files}/{total_files}', 'green' if valid_files == total_files else 'yellow')}")
    if valid_files == total_files:
        print(color_text("   All files passed validation!", "green"))
    else:
        print(color_text(f"   {total_files - valid_files} file(s) failed validation", "yellow"))

def get_files_to_validate(argv, output_dir: Path) -> List[Path]:
    if len(argv) > 1:
        return [Path(arg) for arg in argv[1:]]
    return find_output_files(output_dir)

def main():
    print(color_text("Challenge 1B Output Validator", "blue"))
    print("=" * 40)
    schema = load_schema()
    print(color_text("Schema loaded successfully", "green"))

    output_dir = Path(__file__).parent / "output"
    files_to_validate = get_files_to_validate(sys.argv, output_dir)

    if not files_to_validate:
        print(color_text("No output files found to validate", "red"))
        return 1

    print(color_text(f"Found {len(files_to_validate)} output file(s)", "blue"))
    valid_files = 0
    total_files = len(files_to_validate)

    for file_path in files_to_validate:
        print(f"\n{color_text('Validating:', 'blue')} {file_path.name}")
        if validate_output_file(file_path, schema):
            valid_files += 1

    print_summary(valid_files, total_files)
    return 0 if valid_files == total_files else 1

if __name__ == "__main__":
    sys.exit(main())
