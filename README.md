# Adobe India Hackathon 2025 - Connecting the Dots Challenge

## Project Overview

This repository contains solutions for the Adobe India Hackathon 2025 "Connecting the Dots" Challenge - an intelligent PDF processing system that reimagines how we interact with documents through persona-driven intelligence.

## Challenge Description

**Theme**: Rethink Reading. Rediscover Knowledge

This solution focuses on building intelligent PDF processing systems that can:

- **Round 1A**: Extract structured outlines from PDFs with hierarchical organization
- **Round 1B**: Perform persona-driven document intelligence with contextual content extraction

## Challenge 1B: Persona-Driven Document Intelligence

**Primary Focus**: Advanced multi-collection PDF analysis that understands user context and extracts the most relevant content based on specific personas and job-to-be-done scenarios.

### Key Innovations

- **Intelligent Persona Recognition**: Automatically identifies user roles (Travel Planner, HR Professional, Food Contractor)
- **Context-Aware Content Extraction**: Ranks and filters content based on relevance to specific tasks
- **Multi-Collection Processing**: Handles diverse document types with tailored analysis approaches
- **Smart Relevance Scoring**: Uses sophisticated algorithms to match content with user needs

## Project Structure

```
adobe-hackathon-2025/
├── Challenge_1a/              # PDF Outline Extraction
│   ├── src/                   # Core processing modules
│   ├── input/                 # Input PDFs
│   ├── output/                # Generated outlines
│   ├── process_pdfs.py       # Main processor
│   ├── Dockerfile            # Container config
│   └── README.md             # Documentation
├── Challenge_1b/              # Persona-Driven Intelligence
│   ├── Collection 1/          # Travel Planning (South of France guides)
│   ├── Collection 2/          # Adobe Acrobat Learning (HR workflows)
│   ├── Collection 3/          # Recipe Collection (Corporate catering)
│   ├── utils/                 # PDF processing utilities
│   ├── process_pdfs.py       # Main analysis engine
│   ├── requirements.txt       # Dependencies (PyMuPDF)
│   ├── Dockerfile            # Production container
│   └── README.md             # Detailed documentation
├── build-and-test.sh         # Automated build & test script
└── README.md                 # This overview
```

## Key Features & Capabilities

### Challenge 1B Highlights

- **Multi-Persona Support**: Handles Travel Planners, HR Professionals, and Food Contractors with specialized processing
- **Intelligent Content Ranking**: Advanced relevance scoring based on persona keywords and job context
- **Multi-Collection Processing**: Processes 3 distinct document collections (31 PDFs total)
- **Structured Output**: Comprehensive JSON with metadata, extracted sections, and analysis insights
- **Production Ready**: Docker containerization with CPU-only processing requirements

### Collection Analysis

- **Collection 1 (Travel)**: 7 South of France guides → Travel planning insights
- **Collection 2 (Adobe)**: 15 Acrobat tutorials → HR form creation workflows
- **Collection 3 (Food)**: 9 recipe guides → Corporate catering menu planning

### Technical Architecture

- **PDF Processing**: PyMuPDF for robust text extraction and document analysis
- **Section Detection**: Smart header recognition and content segmentation
- **Relevance Engine**: TF-IDF inspired scoring with persona-specific keyword matching
- **Performance**: <60 seconds processing time, <1GB memory footprint

## Quick Start

### Challenge 1B (Primary Focus)

```bash
cd Challenge_1b

# Option 1: Direct execution
pip install -r requirements.txt
python process_pdfs.py

# Option 2: Docker execution
docker build -t challenge1b .
docker run -v $(pwd):/app challenge1b
```

### Expected Output

- Processes all 3 collections automatically
- Generates `challenge1b_output.json` for each collection
- Provides detailed console output with processing statistics
- Creates persona-specific content rankings and analysis

## Performance Metrics

- **Processing Speed**: 2-5 seconds per collection
- **Memory Usage**: <500MB during processing
- **Accuracy**: High relevance scoring for persona-task alignment
- **Scalability**: CPU-only processing suitable for production deployment

## Technical Specifications

### Dependencies

- Python 3.10+
- PyMuPDF (fitz) for PDF processing
- Standard library modules (json, pathlib, re, typing)

### Input Requirements

- PDF documents in collection-specific `PDFs/` directories
- `challenge1b_input.json` configuration files per collection
- Proper persona and job-to-be-done specifications

### Output Format

- Structured JSON with challenge info, metadata, extracted sections, and analysis
- Relevance scores for content ranking
- Comprehensive persona insights and content distribution metrics

### Round 1A: PDF Outline Extraction

- Fast PDF text extraction using PyMuPDF
- Intelligent heading detection with multiple strategies
- Hierarchical structure analysis (H1, H2, H3)
- JSON output conforming to challenge schema
- Real-time schema validation
- Performance optimized for ≤10 seconds on 50-page PDFs

### Round 1B: Persona-Driven Document Intelligence

- **Multi-Collection Processing**: Handles 3 distinct document collections (Travel, Adobe Acrobat, Recipes)
- **Advanced Persona Recognition**: Automatically identifies Travel Planner, HR Professional, Food Contractor personas
- **Intelligent Content Ranking**: Relevance scoring based on persona keywords and job context matching
- **Smart Section Detection**: Automatic document structure analysis and meaningful section extraction
- **Contextual Analysis**: Job-to-be-done specific filtering and prioritization
- **Comprehensive Output**: Structured JSON with metadata, extracted sections, and analytical insights
- **Performance Optimized**: CPU-only processing completing in <60 seconds for all collections

## Technical Stack

- **Language**: Python 3.10
- **PDF Processing**: PyMuPDF (fitz)
- **Text Analysis**: Advanced regex patterns, TF-IDF scoring
- **Schema Validation**: jsonschema
- **Containerization**: Docker (AMD64 compatible)
- **Architecture**: CPU-only, offline processing

### Quick Start

### Prerequisites

- Docker with AMD64 support
- Git

### Automated Build & Test

Use the provided build script for convenient testing:

```bash
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
docker build --platform linux/amd64 -t pdf-processor:v1.1 .
docker run --rm -v $(pwd)/input:/app/input:ro -v $(pwd)/output:/app/output --network none pdf-processor:v1.1
```

3. **Challenge 1B** - Persona-Driven Intelligence:

```bash
cd Challenge_1b
docker build --platform linux/amd64 -t challenge1b-processor .
docker run --rm challenge1b-processor

# Or run directly with Python
pip install -r requirements.txt
python process_pdfs.py
```

### Challenge 1B Processing Results

After running, you'll see output like:

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
ls -la "Collection "*/challenge1b_output.json
```

### Verifying Challenge 1B Results

Each collection will generate a `challenge1b_output.json` file containing:

- **metadata**: Processing information and statistics
- **extracted_sections**: Top 15 most relevant content sections
- **subsection_analysis**: Persona insights and content distribution
- **relevance_scores**: Numerical rankings for content importance

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

## Scoring Criteria

### Challenge 1A (45 points)

- Heading Detection Accuracy (25 points)
- Performance & Size Compliance (10 points)
- Multilingual Handling Bonus (10 points)

### Challenge 1B (100 points)

- Section Relevance (60 points)
- Sub-Section Relevance (40 points)

## Development Notes

- Keep the repository private until competition deadline
- Use only open-source libraries and models
- Test on both simple and complex PDFs
- Ensure cross-platform compatibility
- Implement modular, reusable code

## License

This project is developed for the Adobe India Hackathon 2025 competition.

---

**Important**: This is a competitive hackathon submission. All solutions must run offline and meet the specified performance constraints.
