# Adobe India Hackathon 2025 - Connecting the Dots Challenge

## Project Overview

This repository contains the solution for the Adobe India Hackathon 2025 "Connecting the Dots" Challenge Round 1A - a PDF intelligence system that reimagines how we interact with documents.

## Challenge Description

**Theme**: Rethink Reading. Rediscover Knowledge

This solution focuses on building an intelligent PDF processing system that can:

- Extract structured outlines from PDFs (Round 1A)

## Project Structure

```
adobe-hackathon-2025/
├── Challenge_1a/              # PDF Outline Extraction
│   ├── src/
│   │   ├── pdf_processor.py   # Main PDF processing logic
│   │   ├── outline_extractor.py # Heading detection & hierarchy
│   │   ├── schema_validator.py # JSON schema validation
│   │   └── utils.py           # Utility functions
│   ├── input/                 # Input PDFs (mounted volume)
│   ├── output/                # Output JSON files
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile            # Docker configuration
│   ├── process_pdfs.py       # Entry point script
│   ├── validate_schema.py    # Schema validation tool
│   └── README.md             # Challenge 1A documentation
└── README.md                 # This file
```

## Key Features

### Round 1A: PDF Outline Extraction

- Fast PDF text extraction using PyMuPDF
- Intelligent heading detection with multiple strategies
- Hierarchical structure analysis (H1, H2, H3)
- JSON output conforming to challenge schema
- Real-time schema validation
- Performance optimized for ≤10 seconds on 50-page PDFs

## Technical Stack

- **Language**: Python 3.10
- **PDF Processing**: PyMuPDF (fitz)
- **Text Analysis**: regex
- **Schema Validation**: jsonschema
- **Containerization**: Docker (AMD64 compatible)
- **Architecture**: CPU-only, offline processing

## Getting Started

### Prerequisites

- Docker with AMD64 support
- Git

### Quick Start

1. Clone the repository:

```bash
git clone <your-repo-url>
cd adobe-hackathon-2025
```

2. Build and run Challenge 1A:

```bash
cd Challenge_1a
docker build --platform linux/amd64 -t pdf-processor:v1.1 .
docker run --rm -v $(pwd)/input:/app/input:ro -v $(pwd)/output:/app/output --network none pdf-processor:v1.1
```

3. Validate output schema (optional):

```bash
cd Challenge_1a
python validate_schema.py
```

## Performance Specifications

### Challenge 1A Constraints

- **Execution Time**: ≤ 10 seconds for 50-page PDF
- **Model Size**: ≤ 200MB
- **Runtime**: CPU only (8 cores, 16GB RAM)
- **Architecture**: AMD64 (linux/amd64)
- **Network**: No internet access

## Scoring Criteria

### Challenge 1A (45 points)

- Heading Detection Accuracy (25 points)
- Performance & Size Compliance (10 points)
- Multilingual Handling Bonus (10 points)

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
