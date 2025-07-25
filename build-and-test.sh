#!/bin/bash

# Adobe India Hackathon 2025 - Build and Test Script
# This script helps build and test both Challenge 1A and 1B solutions

set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}Adobe India Hackathon 2025 - Build and Test Script${NC}"
echo -e "${CYAN}====================================================${NC}"

# Function to build Challenge 1A
build_challenge_1a() {
    echo ""
    echo -e "${BLUE}Building Challenge 1A - PDF Outline Extraction${NC}"
    echo -e "${BLUE}-------------------------------------------------${NC}"
    
    cd Challenge_1a
    
    echo "Building Docker image..."
    docker build --platform linux/amd64 -t pdf-processor:v1.1 .
    
    echo -e "${GREEN}Challenge 1A build complete!${NC}"
    cd ..
}

# Function to test Challenge 1A
test_challenge_1a() {
    echo ""
    echo -e "${YELLOW}Testing Challenge 1A${NC}"
    echo -e "${YELLOW}----------------------${NC}"
    
    cd Challenge_1a
    
    # Create test directories if they don't exist
    mkdir -p input output
    
    echo "Running Challenge 1A container..."
    docker run --rm \
        -v $(pwd)/input:/app/input:ro \
        -v $(pwd)/output:/app/output \
        --network none \
        pdf-processor:v1.1
    
    echo -e "${GREEN}Challenge 1A test complete!${NC}"
    echo "Output files generated in Challenge_1a/output/"
    cd ..
}

# Function to build Challenge 1B
build_challenge_1b() {
    echo ""
    echo -e "${BLUE}Building Challenge 1B - Document Intelligence${NC}"
    echo -e "${BLUE}-----------------------------------------------${NC}"
    
    cd Challenge_1b
    
    echo "Building Docker image..."
    docker build --platform linux/amd64 -t challenge1b-processor .
    
    echo -e "${GREEN}Challenge 1B build complete!${NC}"
    cd ..
}

# Function to test Challenge 1B
test_challenge_1b() {
    echo ""
    echo -e "${YELLOW}Testing Challenge 1B${NC}"
    echo -e "${YELLOW}----------------------${NC}"
    
    cd Challenge_1b
    
    echo "Running Challenge 1B container..."
    docker run --rm challenge1b-processor
    
    echo -e "${GREEN}Challenge 1B test complete!${NC}"
    echo "Output files generated in Collection directories:"
    echo "  - Collection 1/challenge1b_output.json"
    echo "  - Collection 2/challenge1b_output.json" 
    echo "  - Collection 3/challenge1b_output.json"
    cd ..
}

# Function to validate schemas
validate_schemas() {
    echo ""
    echo -e "${CYAN}Validating Schema Compliance${NC}"
    echo -e "${CYAN}------------------------------${NC}"
    
    echo "Validating Challenge 1A..."
    cd Challenge_1a
    if [ -f "validate_schema.py" ]; then
        python validate_schema.py
    else
        echo -e "${YELLOW}Challenge 1A schema validation script not found${NC}"
    fi
    cd ..
    
    echo ""
    echo "Validating Challenge 1B..."
    cd Challenge_1b
    if [ -f "validate_schema.py" ]; then
        python validate_schema.py
    else
        echo -e "${YELLOW}Challenge 1B schema validation script not found${NC}"
    fi
    cd ..
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  1a-build    Build Challenge 1A Docker image"
    echo "  1a-test     Test Challenge 1A (builds if needed)"
    echo "  1b-build    Build Challenge 1B Docker image"
    echo "  1b-test     Test Challenge 1B (builds if needed)"
    echo "  build-all   Build both challenges"
    echo "  test-all    Test both challenges"
    echo "  validate    Validate output schemas"
    echo "  full        Build, test, and validate everything"
    echo "  clean       Clean up Docker images"
    echo "  help        Show this help message"
}

# Function to clean up
clean_images() {
    echo ""
    echo -e "${RED}Cleaning up Docker images${NC}"
    echo -e "${RED}---------------------------${NC}"
    
    echo "Removing Docker images..."
    docker rmi pdf-processor:v1.1 2>/dev/null || echo "pdf-processor:v1.1 not found"
    docker rmi pdf-processor:v1.0 2>/dev/null || echo "pdf-processor:v1.0 not found"
    docker rmi challenge1b-processor 2>/dev/null || echo "challenge1b-processor not found"
    
    echo -e "${GREEN}Cleanup complete!${NC}"
}

# Main execution
case "${1:-help}" in
    "1a-build")
        build_challenge_1a
        ;;
    "1a-test")
        build_challenge_1a
        test_challenge_1a
        ;;
    "1b-build")
        build_challenge_1b
        ;;
    "1b-test")
        build_challenge_1b
        test_challenge_1b
        ;;
    "build-all")
        build_challenge_1a
        build_challenge_1b
        ;;
    "test-all")
        build_challenge_1a
        test_challenge_1a
        build_challenge_1b
        test_challenge_1b
        ;;
    "validate")
        validate_schemas
        ;;
    "full")
        build_challenge_1a
        test_challenge_1a
        build_challenge_1b
        test_challenge_1b
        validate_schemas
        ;;
    "clean")
        clean_images
        ;;
    "help"|*)
        show_usage
        ;;
esac

echo ""
echo -e "${CYAN}Ready for the Adobe India Hackathon 2025!${NC}"
echo -e "${CYAN}=============================================${NC}"
