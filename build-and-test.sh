#!/bin/bash

# Adobe India Hackathon 2025 - Build and Test Script
# This script helps build and test Challenge 1A solution

set -e

echo "🚀 Adobe India Hackathon 2025 - Build and Test Script"
echo "====================================================="

# Function to build Challenge 1A
build_challenge_1a() {
    echo ""
    echo "📄 Building Challenge 1A - PDF Outline Extraction"
    echo "-------------------------------------------------"
    
    cd Challenge_1a
    
    echo "Building Docker image..."
    docker build --platform linux/amd64 -t pdf-processor:v1.1 .
    
    echo "✅ Challenge 1A build complete!"
    cd ..
}

# Function to test Challenge 1A
test_challenge_1a() {
    echo ""
    echo "🧪 Testing Challenge 1A"
    echo "----------------------"
    
    cd Challenge_1a
    
    # Create test directories if they don't exist
    mkdir -p input output
    
    echo "Running Challenge 1A container..."
    docker run --rm \
        -v $(pwd)/input:/app/input:ro \
        -v $(pwd)/output:/app/output \
        --network none \
        pdf-processor:v1.1
    
    echo "✅ Challenge 1A test complete!"
    echo "Output files generated in Challenge_1a/output/"
    cd ..
}

# Function to validate schema
validate_schema() {
    echo ""
    echo "📋 Validating Schema Compliance"
    echo "------------------------------"
    
    cd Challenge_1a
    
    if [ -f "validate_schema.py" ]; then
        python validate_schema.py
    else
        echo "⚠️  Schema validation script not found"
    fi
    
    cd ..
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  build       Build Challenge 1A Docker image"
    echo "  test        Test Challenge 1A (builds if needed)"
    echo "  validate    Validate output schema compliance"
    echo "  full        Build, test, and validate"
    echo "  clean       Clean up Docker images"
    echo "  help        Show this help message"
}

# Function to clean up
clean_images() {
    echo ""
    echo "🧹 Cleaning up Docker images"
    echo "---------------------------"
    
    echo "Removing Docker images..."
    docker rmi pdf-processor:v1.1 2>/dev/null || echo "pdf-processor:v1.1 not found"
    docker rmi pdf-processor:v1.0 2>/dev/null || echo "pdf-processor:v1.0 not found"
    
    echo "✅ Cleanup complete!"
}

# Main execution
case "${1:-help}" in
    "build")
        build_challenge_1a
        ;;
    "test")
        build_challenge_1a
        test_challenge_1a
        ;;
    "validate")
        validate_schema
        ;;
    "full")
        build_challenge_1a
        test_challenge_1a
        validate_schema
        ;;
    "clean")
        clean_images
        ;;
    "help"|*)
        show_usage
        ;;
esac

echo ""
echo "🎯 Ready for the Adobe India Hackathon 2025!"
echo "============================================="
