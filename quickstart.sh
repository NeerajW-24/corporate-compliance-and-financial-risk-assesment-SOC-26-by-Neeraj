#!/bin/bash
# Quick Start Script for Corporate Compliance Project

echo "========================================="
echo "Corporate Compliance & Risk Assessment"
echo "Season of Code | WnCC, IIT Bombay"
echo "=========================================="
echo ""

# Check Python
echo "✓ Checking Python installation..."
python3 --version

# Create virtual environment
echo "✓ Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "✓ Installing dependencies..."
pip install -r requirements.txt > /dev/null 2>&1

# Create necessary directories
echo "✓ Setting up directories..."
mkdir -p data reports logs

echo ""
echo "=========================================="
echo "✓ PROJECT SETUP COMPLETE!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Configure database in config/config.yaml"
echo "2. Run: python main.py --stage all"
echo "3. View dashboard: Power BI configuration ready"
echo ""
echo "Project includes:"
echo "  • 3 Integrated datasets (200+ economies)"
echo "  • 3 Anomaly detection methods"
echo "  • 6 TBML typologies"
echo "  • 12+ Compliance KPIs"
echo ""
