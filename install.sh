#!/bin/bash
# Installation script for Renaissance Stock Ranking System

# Exit on error
set -e

echo "Setting up Renaissance Stock Ranking System..."

# Create and activate virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
else
    echo "Virtual environment already exists."
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

# Install the package in development mode
echo "Installing Renaissance Stock Ranking package..."
pip install -e .

# Make scripts executable
echo "Making scripts executable..."
chmod +x scripts/*.py

echo "Installation complete!"
echo ""
echo "To use the system:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the ranking: python scripts/run_ranking.py"
echo "3. Generate visualizations: python scripts/visualize_results.py"
echo "4. Analyze sectors: python scripts/analyze_sectors.py"
echo ""
echo "Alternatively, you can use the command-line tools:"
echo "- renaissance-rank"
echo "- renaissance-visualize"
echo "- renaissance-analyze"
echo "- renaissance-extract" 