#!/usr/bin/env python3
"""
Adobe India Hackathon 2025 - Challenge 1A
PDF Outline Extraction - Main Entry Point

This script processes all PDFs in the input directory and generates
structured JSON outlines for each document.
"""

import os
import sys
import time
from pathlib import Path

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from pdf_processor import PDFProcessor


def main():
    """Main entry point for PDF processing."""
    print("Starting PDF outline extraction...")
    start_time = time.time()
    
    # Define input and output directories
    input_dir = Path("/app/input")
    output_dir = Path("/app/output")
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize PDF processor
    processor = PDFProcessor()
    
    # Get all PDF files from input directory
    pdf_files = list(input_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("No PDF files found in input directory.")
        return
    
    print(f"Found {len(pdf_files)} PDF file(s) to process:")
    for pdf_file in pdf_files:
        print(f"  - {pdf_file.name}")
    
    # Process each PDF file
    processed_count = 0
    for pdf_file in pdf_files:
        try:
            print(f"\nProcessing: {pdf_file.name}")
            
            # Extract outline from PDF
            result = processor.extract_outline(pdf_file)
            
            # Create output JSON file
            output_file = output_dir / f"{pdf_file.stem}.json"
            processor.save_result(result, output_file)
            
            print(f"✓ Generated: {output_file.name}")
            processed_count += 1
            
        except Exception as e:
            print(f"✗ Error processing {pdf_file.name}: {str(e)}")
            # Continue processing other files
            continue
    
    # Summary
    total_time = time.time() - start_time
    print(f"\n{'='*50}")
    print(f"Processing complete!")
    print(f"Files processed: {processed_count}/{len(pdf_files)}")
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Average time per file: {total_time/len(pdf_files):.2f} seconds")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
