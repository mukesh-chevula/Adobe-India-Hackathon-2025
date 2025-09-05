# Adobe India Hackathon 2025 - Connecting the Dots Challenge

## Project Overview

This repository contains comprehensive solutions for the Adobe India Hackathon 2025 "Connecting the Dots" Challenge - an intelligent PDF processing system that reimagines how we interact with documents through advanced text extraction and persona-driven intelligence.

## Challenge Description

**Theme**: Rethink Reading. Rediscover Knowledge

This solution focuses on building intelligent PDF processing systems that can:

- **Round 1A**: Extract structured outlines from PDFs with hierarchical organization and real-time schema validation
- **Round 1B**: Perform persona-driven document intelligence with contextual content extraction and relevance ranking

## Challenge Solutions

### Challenge 1A: PDF Outline Extraction

**Objective**: Extract structured hierarchical outlines from PDF documents

**Key Features**:

- Advanced PDF text extraction using PyMuPDF
- Multi-strategy heading detection (font-based, formatting-based, regex patterns)
- Hierarchical structure analysis (H1, H2, H3 levels)
- Real-time JSON schema validation
- Performance optimized for ≤10 seconds on 50-page PDFs
- Handles complex document layouts and multilingual content

**Technical Implementation**:

- **PDF Processing**: PyMuPDF for robust text extraction
- **Heading Detection**: Font size analysis, bold text detection, numbering patterns
- **Structure Building**: Hierarchical outline construction with page references
- **Validation**: jsonschema compliance checking
- **Output**: Clean JSON format matching official schema

### Challenge 1B: Persona-Driven Document Intelligence

**Objective**: Analyze multiple document collections through persona-specific lenses

**Key Features**:

- **Multi-Collection Processing**: Handles 3 distinct document collections (31 PDFs total)
- **Advanced Persona Recognition**: Travel Planner, HR Professional, Food Contractor personas
- **Intelligent Content Ranking**: TF-IDF inspired relevance scoring with persona keywords
- **Contextual Analysis**: Job-to-be-done specific filtering and prioritization
- **Smart Section Detection**: Automatic document structure analysis
- **Comprehensive Output**: Structured JSON with metadata, extracted sections, and insights

**Technical Implementation**:

- **Document Analysis**: Advanced text segmentation and section identification
- **Persona Processing**: Role-specific keyword matching and context understanding
- **Section Ranking**: Sophisticated relevance algorithms for content prioritization
- **Multi-Collection Support**: Unified processing pipeline for diverse document types

## Project Structure

```
adobe-hackathon-2025/
├── Challenge_1a/              # PDF Outline Extraction Solution
│   ├── src/                   # Core processing modules
│   │   ├── pdf_processor.py   # Main PDF processing coordinator
│   │   ├── outline_extractor.py # Advanced heading detection engine
│   │   ├── schema_validator.py # Real-time JSON validation
│   │   └── utils.py           # Utility functions and helpers
│   ├── input/                 # Input PDFs directory (6 test files)
│   ├── output/                # Generated JSON outlines
│   ├── requirements.txt       # PyMuPDF, jsonschema dependencies
│   ├── Dockerfile            # Production container config
│   ├── process_pdfs.py       # Main entry point
│   ├── validate_schema.py    # Standalone validation tool
│   └── README.md             # Detailed Challenge 1A documentation
├── Challenge_1b/              # Persona-Driven Intelligence Solution
│   ├── Collection 1/          # Travel Planning Documents (7 PDFs)
│   │   ├── PDFs/             # South of France travel guides
│   │   ├── challenge1b_input.json  # Travel Planner persona config
│   │   └── challenge1b_output.json # Generated analysis results
│   ├── Collection 2/          # Adobe Acrobat Learning (15 PDFs)
│   │   ├── PDFs/             # HR workflow tutorials
│   │   ├── challenge1b_input.json  # HR Professional persona config
│   │   └── challenge1b_output.json # Generated analysis results
│   ├── Collection 3/          # Recipe Collection (9 PDFs)
│   │   ├── PDFs/             # Corporate catering guides
│   │   ├── challenge1b_input.json  # Food Contractor persona config
│   │   └── challenge1b_output.json # Generated analysis results
│   ├── src/                   # Advanced processing modules
│   │   ├── document_analyzer.py # Document structure analysis
│   │   ├── persona_processor.py # Role-specific content processing
│   │   └── section_ranker.py    # Advanced relevance algorithms
│   ├── utils/                 # PDF processing utilities
│   │   └── parser.py         # Text extraction and parsing
│   ├── test_data/            # Testing configurations
│   ├── requirements.txt       # PyMuPDF dependencies
│   ├── Dockerfile            # Production container config
│   ├── process_pdfs.py       # Main processing engine
│   ├── validate_schema.py    # Schema compliance validator
│   ├── test_solution.py      # Comprehensive test suite
│   ├── approach_explanation.md # Technical methodology
│   └── README.md             # Detailed Challenge 1B documentation
├── build-and-test.sh         # Automated build & test script
└── README.md                 # This comprehensive overview
```

## Key Features & Technical Highlights

### Challenge 1A: PDF Outline Extraction

**Core Capabilities**:

- **Fast PDF Processing**: PyMuPDF-based extraction completing in <10 seconds for 50-page documents
- **Multi-Strategy Heading Detection**:
  - Font size and style analysis for visual hierarchy detection
  - Text formatting recognition (bold, size changes, spacing)
  - Regex pattern matching for numbered sections and structured content
  - Intelligent fallback mechanisms for complex layouts
- **Hierarchical Structure Building**: Automatic H1/H2/H3 classification with proper nesting
- **Real-Time Validation**: jsonschema compliance checking with detailed error reporting
- **Robust Error Handling**: Graceful handling of malformed PDFs and edge cases

**Performance Metrics**:

- Processing Speed: 2-8 seconds per PDF (depending on complexity)
- Memory Usage: <200MB during processing
- Accuracy: High precision in heading detection across diverse document formats
- Compatibility: Handles multilingual content and complex formatting

### Challenge 1B: Persona-Driven Document Intelligence

**Advanced Features**:

- **Multi-Collection Architecture**: Processes 3 distinct document collections with 31 total PDFs
- **Intelligent Persona Recognition**:
  - Travel Planner: Optimized for trip planning and destination information
  - HR Professional: Focused on workflow creation and form processing
  - Food Contractor: Specialized in menu planning and recipe analysis
- **Contextual Content Extraction**:
  - Job-to-be-done alignment for relevant content identification
  - Advanced relevance scoring using TF-IDF inspired algorithms
  - Smart section ranking based on persona-specific keywords
- **Comprehensive Analysis Output**:
  - Top 15 most relevant sections per collection
  - Detailed subsection analysis with quality metrics
  - Processing metadata and performance statistics

**Performance Metrics**:

- Processing Speed: 15-25 seconds for all 3 collections
- Memory Usage: <500MB during processing
- Analysis Accuracy: High relevance matching for persona-task alignment
- Scalability: CPU-only processing suitable for production deployment

**Collection Details**:

- **Collection 1 (Travel)**: 7 South of France guides → 13.4KB output with travel planning insights
- **Collection 2 (Adobe)**: 15 Acrobat tutorials → 27.1KB output with HR workflow guidance
- **Collection 3 (Food)**: 9 recipe guides → 17.0KB output with catering menu insights

### Verifying Results

#### Challenge 1A Output Structure:

Each PDF generates a JSON file with:

- **title**: Extracted document title
- **outline**: Array of hierarchical headings with level (H1/H2/H3), text, and page number

#### Challenge 1B Output Structure:

Each collection generates a `challenge1b_output.json` file containing:

- **metadata**: Processing information and document list
- **extracted_sections**: Top 15 most relevant content sections with importance rankings
- **subsection_analysis**: Detailed persona insights and refined content analysis

## Technical Architecture

### Challenge 1A Technical Stack:

- **PDF Processing**: PyMuPDF (fitz) for robust text extraction
- **Text Analysis**: Advanced regex patterns for heading detection
- **Structure Building**: Hierarchical outline construction algorithms
- **Validation**: jsonschema for real-time compliance checking
- **Performance**: Optimized for CPU-only processing with <200MB memory usage

### Challenge 1B Technical Stack:

- **PDF Processing**: PyMuPDF for multi-document text extraction
- **Content Analysis**: TF-IDF inspired relevance scoring algorithms
- **Persona Engine**: Role-specific keyword matching and context understanding
- **Section Ranking**: Advanced importance calculation with persona weighting
- **Architecture**: Modular design with DocumentAnalyzer, PersonaProcessor, and SectionRanker components

## Getting Started

### Prerequisites

- Docker with AMD64 support
- Git
- Python 3.10+ (for local development)

### Automated Build & Test

Use the provided build script for convenient testing:

```bash
# Test Challenge 1A only
./build-and-test.sh 1a-test

# Test Challenge 1B only
./build-and-test.sh 1b-test

# Test both challenges
./build-and-test.sh test-all

# Build and validate everything
./build-and-test.sh full

# Show all options
./build-and-test.sh help
```

### Manual Setup

1. Clone the repository:

```bash
git clone <your-repo-url>
cd adobe-hackathon-2025
```

2. **Challenge 1A** - PDF Outline Extraction:

```bash
cd Challenge_1a

# Docker execution (recommended)
docker build --platform linux/amd64 -t pdf-processor:v1.1 .
docker run --rm \
        -v $(pwd)/input:/app/input:ro \
        -v $(pwd)/output:/app/output \
        --network none \
        pdf-processor:v1.1

# Or local Python execution
pip install -r requirements.txt
python process_pdfs.py
```

3. **Challenge 1B** - Persona-Driven Intelligence:

```bash
cd Challenge_1b

# Docker execution (recommended)
docker build --platform linux/amd64 -t challenge1b-processor .
docker run --rm challenge1b-processor

# Or local Python execution
pip install -r requirements.txt
python process_pdfs.py
```

### Expected Output

#### Challenge 1A Results:

```
Checking: challenge_doc.pdf
Valid

Summary: 6/6 files passed validation
All files conform to the official schema!
```

#### Challenge 1B Results:

```
Processing Collection 1
Output written to Collection 1/challenge1b_output.json

Processing Collection 2
Output written to Collection 2/challenge1b_output.json

Processing Collection 3
Output written to Collection 3/challenge1b_output.json
```

4. **Validate outputs** (optional):

```bash
# For Challenge 1A
cd Challenge_1a && python validate_schema.py

# For Challenge 1B - Check generated outputs
cd Challenge_1b
python validate_schema.py "Collection 1/challenge1b_output.json"
ls -la "Collection "*/challenge1b_output.json
```

## Performance Specifications

### Challenge 1A Constraints

- **Execution Time**: ≤ 10 seconds for 50-page PDF
- **Model Size**: ≤ 200MB
- **Runtime**: CPU only (8 cores, 16GB RAM)
- **Architecture**: AMD64 (linux/amd64)
- **Network**: No internet access

### Challenge 1B Constraints

- **Execution Time**: ≤ 60 seconds for 3-5 documents
- **Model Size**: ≤ 1GB (CPU-only, no ML models required)
- **Runtime**: CPU only
- **Architecture**: AMD64 (linux/amd64)
- **Network**: No internet access

## Scoring Criteria & Competition Details

### Challenge 1A Scoring (45 points total)

- **Heading Detection Accuracy (25 points)**: Precision in identifying and classifying document headings
- **Performance & Size Compliance (10 points)**: Meeting execution time and model size constraints
- **Multilingual Handling Bonus (10 points)**: Effective processing of non-English content

### Challenge 1B Scoring (100 points total)

- **Section Relevance (60 points)**: Accuracy in identifying and ranking relevant content sections
- **Sub-Section Relevance (40 points)**: Quality of detailed subsection analysis and persona alignment

### Achievement Highlights

- Challenge 1A: All 6 test PDFs processed successfully with 100% schema compliance
- Challenge 1B: 31 PDFs across 3 collections processed with high relevance accuracy
- Performance: Both solutions meet strict timing and resource constraints
- Docker Ready: Full containerization for hackathon submission requirements

## Development Philosophy

This solution emphasizes:

- **Modularity**: Clean separation of concerns with reusable components
- **Performance**: CPU-only processing optimized for competition constraints
- **Reliability**: Robust error handling and graceful degradation
- **Maintainability**: Well-documented code with comprehensive testing
- **Scalability**: Architecture designed for production deployment

## Repository Features

- **Automated Testing**: Comprehensive build and test scripts
- **Schema Validation**: Real-time compliance checking for both challenges
- **Docker Support**: Production-ready containerization
- **Documentation**: Detailed README files for each challenge
- **Performance Monitoring**: Built-in timing and resource usage tracking

## Documentation

For detailed technical methodology, design decisions, and implementation notes, please refer to the full documentation:

[View Project Documentation](https://drive.google.com/file/d/1ifcxlEdJBkASJWbTVokS9b4GmzwQLerf/view?usp=share_link)


## License

This project is developed for the Adobe India Hackathon 2025 competition.

---

**Important**: This is a competitive hackathon submission. All solutions must run offline and meet the specified performance constraints.
