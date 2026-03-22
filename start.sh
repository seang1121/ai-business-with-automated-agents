#!/bin/bash
echo "============================================================"
echo "  AI Business with Automated Agents — Starting..."
echo "============================================================"

# Create venv if missing
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt -q

# Seed demo data if DB doesn't exist
if [ ! -f "business.db" ]; then
    echo "Seeding demo data..."
    python backend/seed_demo.py
fi

# Start Flask
echo ""
echo "Starting server..."
python backend/app.py
