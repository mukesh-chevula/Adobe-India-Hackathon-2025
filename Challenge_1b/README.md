# Challenge 1B: Persona-Driven Document Intelligence

## Overview

Advanced PDF analysis solution that processes multiple document collections and extracts relevant content based on specific personas and job-to-be-done contexts. The system intelligently ranks and filters content based on persona relevance using keyword matching and context analysis.

## Features

- **Persona-Driven Analysis**: Tailors content extraction based on user roles (Travel Planner, HR Professional, Food Contractor)
- **Intelligent Ranking**: Scores and ranks document sections by relevance to persona and task
- **Smart Section Detection**: Automatically identifies document structure and extracts meaningful sections
- **Multi-Collection Processing**: Handles multiple document collections with different contexts
- **Efficient Processing**: CPU-only processing optimized for performance
- **Docker Ready**: Containerized solution for easy deployment

## Project Structure

```
Challenge_1b/
├── Collection 1/                    # Travel Planning Collection
│   ├── PDFs/                       # South of France travel guides (7 documents)
│   ├── challenge1b_input.json      # Input configuration with Travel Planner persona
│   └── challenge1b_output.json     # Extracted relevant travel content
├── Collection 2/                    # Adobe Acrobat Learning Collection
│   ├── PDFs/                       # Acrobat tutorials (15 documents)
│   ├── challenge1b_input.json      # Input configuration with HR Professional persona
│   └── challenge1b_output.json     # Extracted form creation and management content
├── Collection 3/                    # Recipe Collection
│   ├── PDFs/                       # Cooking guides (9 documents)
│   ├── challenge1b_input.json      # Input configuration with Food Contractor persona
│   └── challenge1b_output.json     # Extracted vegetarian menu content
├── utils/                           # Utility modules
│   └── parser.py                   # PDF text extraction utilities
├── process_pdfs.py                 # Main processing script
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Container configuration
└── README.md                       # This file
```

## Collections Details

### Collection 1: Travel Planning

- **Challenge ID**: `round_1b_002`
- **Persona**: Travel Planner
- **Job-to-be-Done**: Plan a 4-day trip for 10 college friends to South of France
- **Documents**: 7 comprehensive travel guides covering cities, cuisine, history, hotels, activities, tips, and culture
- **Focus Areas**: Itinerary planning, group accommodations, budget-friendly activities, local attractions

### Collection 2: Adobe Acrobat Learning

- **Challenge ID**: `round_1b_003`
- **Persona**: HR Professional
- **Job-to-be-Done**: Create and manage fillable forms for onboarding and compliance
- **Documents**: 15 Acrobat tutorials covering creation, conversion, editing, forms, and signatures
- **Focus Areas**: Form creation, digital workflows, document automation, compliance management

### Collection 3: Recipe Collection

- **Challenge ID**: `round_1b_001`
- **Persona**: Food Contractor
- **Job-to-be-Done**: Prepare vegetarian buffet-style dinner menu for corporate gathering
- **Documents**: 9 cooking guides with breakfast, lunch, dinner, and side dish recipes
- **Focus Areas**: Vegetarian options, buffet-style serving, corporate catering, menu planning

## Technical Architecture

### Persona Analysis Engine

The system uses a sophisticated persona analysis engine that:

- **Identifies Persona Types**: Automatically classifies personas into Travel Planner, HR Professional, Food Contractor, or General categories
- **Keyword Matching**: Uses domain-specific keyword dictionaries for each persona type
- **Relevance Scoring**: Calculates relevance scores based on both persona keywords and job-specific terms
- **Content Ranking**: Ranks document sections by relevance to provide the most useful content first

### PDF Processing Pipeline

1. **Text Extraction**: Uses PyMuPDF for robust PDF text extraction
2. **Section Detection**: Identifies document structure using header patterns and content analysis
3. **Content Analysis**: Analyzes each section for persona relevance
4. **Ranking & Filtering**: Sorts content by relevance score and selects top sections
5. **Output Generation**: Creates structured JSON output with metadata

## Input/Output Format

### Input JSON Structure

```json
{
  "challenge_info": {
    "challenge_id": "round_1b_XXX",
    "test_case_name": "specific_test_case",
    "description": "Brief description"
  },
  "documents": [
    {
      "filename": "document.pdf",
      "title": "Document Title"
    }
  ],
  "persona": {
    "role": "User Persona (e.g., Travel Planner)"
  },
  "job_to_be_done": {
    "task": "Specific task description"
  }
}
```

### Output JSON Structure

```json
{
  "challenge_info": {
    "challenge_id": "round_1b_XXX",
    "test_case_name": "specific_test_case",
    "description": "Brief description"
  },
  "metadata": {
    "processing_timestamp": 1721925600,
    "persona_type": "travel_planner",
    "job_context": "Plan a trip for college friends",
    "total_documents_processed": 7,
    "total_sections_analyzed": 45,
    "top_sections_selected": 15,
    "input_documents": ["doc1.pdf", "doc2.pdf"]
  },
  "extracted_sections": [
    {
      "document_filename": "source.pdf",
      "section_title": "Section Title",
      "content": "Relevant content extracted...",
      "page_number": 1,
      "relevance_score": 0.8456
    }
  ],
  "subsection_analysis": {
    "persona_insights": {
      "identified_persona": "travel_planner",
      "alignment_quality": "high",
      "persona_context": "Travel Planner",
      "task_context": "Plan a trip for college friends"
    },
    "content_distribution": {
      "high_relevance_sections": 8,
      "medium_relevance_sections": 12,
      "low_relevance_sections": 25
    },
    "top_sections_summary": [
      {
        "document": "source.pdf",
        "title": "Section Title",
        "score": 0.8456
      }
    ]
  }
}
```

## Usage

### Running the Solution

#### Option 1: Direct Python Execution

```bash
# Install dependencies
pip install -r requirements.txt

# Run the processor
python process_pdfs.py
```

#### Option 2: Docker Execution

```bash
# Build the Docker image
docker build -t challenge1b-processor .

# Run the container
docker run -v $(pwd):/app challenge1b-processor
```

### Expected Output

The script will process all three collections and generate:

- `Collection 1/challenge1b_output.json` - Travel planning results
- `Collection 2/challenge1b_output.json` - HR form creation results
- `Collection 3/challenge1b_output.json` - Food menu planning results

## Performance Characteristics

- **Processing Speed**: ~2-5 seconds per document collection
- **Memory Usage**: <500MB RAM during processing
- **CPU Requirements**: Standard CPU-only processing, no GPU needed
- **Output Size**: Structured JSON with top 15 most relevant sections per collection

## Key Features Implementation

- **Persona-Driven Content Extraction**: Tailored analysis for each user role
- **Intelligent Section Ranking**: Relevance-based content prioritization
- **Multi-Collection Support**: Processes all three collections automatically
- **Structured Output**: JSON format with comprehensive metadata
- **Docker Containerization**: Ready for deployment and scaling
- **Error Handling**: Robust processing with graceful failure handling
