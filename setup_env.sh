#!/bin/bash

# Check if virtualenv is installed, if not, install it
if ! command -v virtualenv &> /dev/null
then
    echo "virtualenv could not be found, installing it..."
    pip install virtualenv
fi

# Create a virtual environment
echo "Creating virtual environment..."
virtualenv venv

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies from requirements.txt
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo "Environment setup complete."