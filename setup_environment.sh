#!/bin/bash
# APDS Environment Setup Script for macOS/Linux
# This script helps set up the Python environment for APDS

echo "========================================"
echo "APDS Environment Setup"
echo "========================================"
echo ""

# Check if Python 3 is installed
echo "[1/5] Checking Python 3 installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo ""
    echo "Please install Python 3:"
    echo "  macOS: brew install python3"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip python3-venv"
    echo "  CentOS/RHEL: sudo yum install python3 python3-pip"
    exit 1
fi

python3 --version
echo "Python 3 found!"
echo ""

# Check if pip3 is available
echo "[2/5] Checking pip installation..."
if ! python3 -m pip --version &> /dev/null; then
    echo "ERROR: pip is not available"
    echo "Attempting to install pip..."
    python3 -m ensurepip --upgrade
fi

python3 -m pip --version
echo "pip found!"
echo ""

# Create virtual environment
echo "[3/5] Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists. Skipping..."
else
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to create virtual environment"
        exit 1
    fi
    echo "Virtual environment created successfully!"
fi
echo ""

# Activate virtual environment
echo "[4/5] Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to activate virtual environment"
    exit 1
fi
echo "Virtual environment activated!"
echo ""

# Upgrade pip
echo "[5/5] Upgrading pip..."
python3 -m pip install --upgrade pip
echo ""

# Install requirements
echo "Installing project dependencies..."
python3 -m pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo ""
echo "========================================"
echo "Setup completed successfully!"
echo "========================================"
echo ""
echo "To run the application:"
echo "  1. Activate the virtual environment: source venv/bin/activate"
echo "  2. Run: python3 app.py"
echo ""

