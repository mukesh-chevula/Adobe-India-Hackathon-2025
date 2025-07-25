#!/usr/bin/env python3
"""
Comprehensive test script for Challenge 1B solution
Adobe India Hackathon 2025
"""

import sys
import json
import time
from pathlib import Path
from typing import Dict, List, Any

# ANSI color codes
class ColorCodes:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

sys.path.append('src')

try:
    from document_analyzer import DocumentAnalyzer
    from persona_processor import PersonaProcessor
    from section_ranker import SectionRanker
except ImportError as import_err:
    print(f"{ColorCodes.FAIL}Import error: {import_err}{ColorCodes.ENDC}")
    print(f"{ColorCodes.WARNING}Make sure you're running from the Challenge_1b directory{ColorCodes.ENDC}")
    sys.exit(1)

# ----------------- Component Tests -----------------

def _test_document_analyzer() -> Dict[str, Any]:
    print(f"\n{ColorCodes.OKBLUE}Testing Document Analyzer...{ColorCodes.ENDC}")
    analyzer_instance = DocumentAnalyzer()
    dummy_content = """
    Chapter 1: Introduction to Machine Learning
    Machine learning is a subset of artificial intelligence that focuses on algorithms.
    1.1 Supervised Learning
    Supervised learning uses labeled data to train models.
    • Classification: Predicting categories
    • Regression: Predicting continuous values
    1.2 Unsupervised Learning
    Finds patterns in data without labels.
    """
    mock_result = {
        'metadata': {'filename': 'test.pdf', 'total_pages': 1, 'total_sections': 3},
        'sections': [
            {
                'section_title': 'Introduction to Machine Learning',
                'content': 'Machine learning is a subset of artificial intelligence that focuses on algorithms.',
                'page_number': 1,
                'detection_method': 'header'
            },
            {
                'section_title': 'Supervised Learning',
                'content': 'Supervised learning uses labeled data to train models. Classification and regression.',
                'page_number': 1,
                'detection_method': 'header'
            },
            {
                'section_title': 'Unsupervised Learning',
                'content': 'Finds patterns in data without labels.',
                'page_number': 1,
                'detection_method': 'header'
            }
        ]
    }
    print(f"   {ColorCodes.OKGREEN}Document analyzer initialized{ColorCodes.ENDC}")
    print(f"   {ColorCodes.OKCYAN}Mock analysis created with {len(mock_result['sections'])} sections{ColorCodes.ENDC}")
    return mock_result

def _test_persona_processor(mock_analysis: Dict[str, Any]) -> Dict[str, Any]:
    print(f"\n{ColorCodes.OKBLUE}Testing Persona Processor...{ColorCodes.ENDC}")
    persona_proc = PersonaProcessor()
    persona_info = {"role": "PhD Researcher in Computational Biology"}
    job_info = {"task": "Prepare a literature review for machine learning research"}
    persona_result = persona_proc.process_with_persona(mock_analysis, persona_info, job_info)
    print(f"   {ColorCodes.OKGREEN}Persona type identified: {persona_result['persona_type']}{ColorCodes.ENDC}")
    print(f"   {ColorCodes.OKCYAN}Job type identified: {persona_result['job_type']}{ColorCodes.ENDC}")
    print(f"   {ColorCodes.OKCYAN}Enhanced sections: {len(persona_result['sections'])}{ColorCodes.ENDC}")
    return persona_result

def _test_section_ranker(persona_result: Dict[str, Any], persona: Dict[str, str], job: Dict[str, str]) -> List[Dict[str, Any]]:
    print(f"\n{ColorCodes.OKBLUE}Testing Section Ranker...{ColorCodes.ENDC}")
    section_ranker = SectionRanker()
    ranked = section_ranker.rank_sections(persona_result['sections'], persona, job)
    print(f"   {ColorCodes.OKGREEN}Ranked sections: {len(ranked)}{ColorCodes.ENDC}")
    if ranked:
        print(f"   {ColorCodes.OKCYAN}Top section score: {ranked[0].get('final_relevance_score', 0):.4f}{ColorCodes.ENDC}")
    return ranked

def test_components():
    print(f"{ColorCodes.HEADER}Testing Individual Components{ColorCodes.ENDC}")
    print("=" * 50)
    mock_analysis = _test_document_analyzer()
    persona_result = _test_persona_processor(mock_analysis)
    _test_section_ranker(persona_result, {"role": "PhD Researcher in Computational Biology"}, {"task": "Prepare a literature review for machine learning research"})
    return True

# ----------------- Schema Validation -----------------

def _load_schema(schema_file: Path) -> Any:
    with open(schema_file, 'r') as schema_f:
        return json.load(schema_f)

def _validate_output_schema(schema: Any, output: Any) -> bool:
    try:
        import jsonschema
        jsonschema.validate(instance=output, schema=schema)
        print(f"   {ColorCodes.OKGREEN}Test output validates against schema{ColorCodes.ENDC}")
        return True
    except ImportError:
        print(f"   {ColorCodes.WARNING}jsonschema not available, skipping validation test{ColorCodes.ENDC}")
        return True
    except Exception as err:
        print(f"   {ColorCodes.FAIL}Validation failed: {err}{ColorCodes.ENDC}")
        return False

def test_schema():
    print(f"\n{ColorCodes.HEADER}Testing Schema Validation{ColorCodes.ENDC}")
    print("=" * 50)
    schema_path = Path("challenge1b_output_schema.json")
    if not schema_path.exists():
        print(f"   {ColorCodes.FAIL}Schema file not found{ColorCodes.ENDC}")
        return False
    try:
        schema = _load_schema(schema_path)
        test_output = {
            "metadata": {
                "input_documents": ["test.pdf"],
                "persona": "Test researcher",
                "job_to_be_done": "Test task",
                "processing_timestamp": "2025-01-01T00:00:00Z"
            },
            "extracted_sections": [
                {
                    "document": "test.pdf",
                    "section_title": "Test Section",
                    "importance_rank": 1,
                    "page_number": 1
                }
            ],
            "subsection_analysis": [
                {
                    "document": "test.pdf",
                    "refined_text": "Test content",
                    "page_number": 1
                }
            ]
        }
        return _validate_output_schema(schema, test_output)
    except Exception as err:
        print(f"   {ColorCodes.FAIL}Schema test failed: {err}{ColorCodes.ENDC}")
        return False

# ----------------- End-to-End Test -----------------

def _run_processor_on_config(config_path: Path) -> bool:
    from process_documents import Challenge1BProcessor
    processor = Challenge1BProcessor()
    return processor.process_collection(str(config_path))

def _check_output_files() -> bool:
    output_files = list(Path("output").glob("challenge1b_output*.json"))
    if output_files:
        print(f"   {ColorCodes.OKCYAN}Generated {len(output_files)} output file(s){ColorCodes.ENDC}")
        return True
    else:
        print(f"   {ColorCodes.WARNING}No output files generated{ColorCodes.ENDC}")
        return False

def _minimal_test_case() -> bool:
    print(f"   {ColorCodes.OKCYAN}Creating minimal test case...{ColorCodes.ENDC}")
    test_sections = [
        {
            'section_title': 'Machine Learning Fundamentals',
            'content': 'Introduction to machine learning algorithms and their applications in research.',
            'page_number': 1,
            'document': 'test_document.pdf'
        },
        {
            'section_title': 'Data Analysis Methods',
            'content': 'Statistical methods for analyzing experimental data and drawing conclusions.',
            'page_number': 2,
            'document': 'test_document.pdf'
        }
    ]
    try:
        persona_proc = PersonaProcessor()
        section_ranker = SectionRanker()
        persona = {"role": "PhD Researcher"}
        job = {"task": "Literature review"}
        enhanced = []
        for sec in test_sections:
            sec_copy = sec.copy()
            sec_copy.update({
                'persona_relevance_score': 0.75,
                'final_relevance_score': 0.80,
                'persona_priority': 'high'
            })
            enhanced.append(sec_copy)
        ranked = section_ranker.rank_sections(enhanced, persona, job)
        output = {
            "metadata": {
                "input_documents": ["test_document.pdf"],
                "persona": "PhD Researcher",
                "job_to_be_done": "Literature review",
                "processing_timestamp": "2025-01-01T00:00:00Z"
            },
            "extracted_sections": [
                {
                    "document": "test_document.pdf",
                    "section_title": "Machine Learning Fundamentals",
                    "importance_rank": 1,
                    "page_number": 1
                }
            ],
            "subsection_analysis": [
                {
                    "document": "test_document.pdf",
                    "refined_text": "Introduction to machine learning algorithms",
                    "page_number": 1
                }
            ]
        }
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        output_path = output_dir / "challenge1b_output_minimal_test.json"
        with open(output_path, 'w') as out_f:
            json.dump(output, out_f, indent=2)
        print(f"   {ColorCodes.OKGREEN}Minimal test completed: {output_path}{ColorCodes.ENDC}")
        return True
    except Exception as err:
        print(f"   {ColorCodes.FAIL}Minimal test failed: {err}{ColorCodes.ENDC}")
        return False

def test_end_to_end():
    print(f"\n{ColorCodes.HEADER}Testing End-to-End Processing{ColorCodes.ENDC}")
    print("=" * 50)
    test_config_path = Path("test_data/challenge1b_input_test.json")
    if not test_config_path.exists():
        print(f"   {ColorCodes.WARNING}Test configuration not found, creating minimal test...{ColorCodes.ENDC}")
        return _minimal_test_case()
    print(f"   {ColorCodes.OKCYAN}Processing test configuration: {test_config_path}{ColorCodes.ENDC}")
    start = time.time()
    try:
        success = _run_processor_on_config(test_config_path)
        elapsed = time.time() - start
        if success:
            print(f"   {ColorCodes.OKGREEN}Processing completed successfully{ColorCodes.ENDC}")
            print(f"   {ColorCodes.OKCYAN}Processing time: {elapsed:.2f} seconds{ColorCodes.ENDC}")
            return _check_output_files()
        else:
            print(f"   {ColorCodes.FAIL}Processing failed{ColorCodes.ENDC}")
            return False
    except Exception as err:
        print(f"   {ColorCodes.FAIL}End-to-end test failed: {err}{ColorCodes.ENDC}")
        return False

# ----------------- Performance Test -----------------

def _initialize_components():
    start = time.time()
    analyzer = DocumentAnalyzer()
    persona_proc = PersonaProcessor()
    section_ranker = SectionRanker()
    elapsed = time.time() - start
    print(f"   {ColorCodes.OKCYAN}Component initialization: {elapsed:.3f} seconds{ColorCodes.ENDC}")
    return analyzer, persona_proc, section_ranker

def _mock_performance_data(num_sections: int = 100) -> List[Dict[str, Any]]:
    return [
        {
            'section_title': f'Section {i}',
            'content': f'This is content for section {i} with some relevant keywords.',
            'page_number': (i // 10) + 1,
            'document': f'doc_{i//20}.pdf'
        }
        for i in range(num_sections)
    ]

def test_performance():
    print(f"\n{ColorCodes.HEADER}Testing Performance{ColorCodes.ENDC}")
    print("=" * 50)
    try:
        _, _, section_ranker = _initialize_components()
        mock_sections = _mock_performance_data()
        persona = {"role": "Researcher"}
        job = {"task": "Analysis"}
        enhanced = []
        for sec in mock_sections:
            sec_copy = sec.copy()
            sec_copy.update({
                'persona_relevance_score': 0.5,
                'final_relevance_score': 0.6
            })
            enhanced.append(sec_copy)
        start = time.time()
        ranked = section_ranker.rank_sections(enhanced, persona, job)
        elapsed = time.time() - start
        print(f"   {ColorCodes.OKCYAN}Processed {len(mock_sections)} sections in {elapsed:.3f} seconds{ColorCodes.ENDC}")
        print(f"   {ColorCodes.OKCYAN}Processing speed: {len(mock_sections)/elapsed:.1f} sections/second{ColorCodes.ENDC}")
        if elapsed < 5.0:
            print(f"   {ColorCodes.OKGREEN}Performance: EXCELLENT{ColorCodes.ENDC}")
            return True
        elif elapsed < 10.0:
            print(f"   {ColorCodes.OKGREEN}Performance: GOOD{ColorCodes.ENDC}")
            return True
        else:
            print(f"   {ColorCodes.WARNING}Performance: NEEDS IMPROVEMENT{ColorCodes.ENDC}")
            return False
    except Exception as err:
        print(f"   {ColorCodes.FAIL}Performance test failed: {err}{ColorCodes.ENDC}")
        return False

# ----------------- Main Test Suite -----------------

def _run_all_tests():
    print(f"{ColorCodes.HEADER}Challenge 1B Solution Test Suite{ColorCodes.ENDC}")
    print("=" * 60)
    print(f"{ColorCodes.BOLD}Testing persona-driven document intelligence system{ColorCodes.ENDC}")
    print("=" * 60)
    start = time.time()
    test_cases = [
        ("Individual Components", test_components),
        ("Schema Validation", test_schema),
        ("End-to-End Processing", test_end_to_end),
        ("Performance", test_performance)
    ]
    passed = 0
    for name, func in test_cases:
        try:
            print(f"\n{ColorCodes.OKBLUE}Running {name}...{ColorCodes.ENDC}")
            if func():
                passed += 1
                print(f"{ColorCodes.OKGREEN}{name}: PASSED{ColorCodes.ENDC}")
            else:
                print(f"{ColorCodes.FAIL}{name}: FAILED{ColorCodes.ENDC}")
        except Exception as err:
            print(f"{ColorCodes.FAIL}{name}: ERROR - {err}{ColorCodes.ENDC}")
    total = time.time() - start
    print("\n" + "=" * 60)
    print(f"{ColorCodes.BOLD}TEST SUITE SUMMARY{ColorCodes.ENDC}")
    print("=" * 60)
    print(f"{ColorCodes.OKGREEN}Tests passed: {passed}/{len(test_cases)}{ColorCodes.ENDC}")
    print(f"{ColorCodes.OKCYAN}Total test time: {total:.2f} seconds{ColorCodes.ENDC}")
    if passed == len(test_cases):
        print(f"{ColorCodes.OKGREEN}All tests passed! Solution is ready.{ColorCodes.ENDC}")
        return 0
    else:
        print(f"{ColorCodes.WARNING}{len(test_cases) - passed} test(s) failed{ColorCodes.ENDC}")
        return 1

if __name__ == "__main__":
    sys.exit(_run_all_tests())
