#!/bin/bash

# Check if the virtual environment directory exists
if [ ! -d "env" ]; then
    echo "No virtual environment found. Creating one..."
    virtualenv env
    pip3 install -r requirements.txt
fi

# Activate the virtual environment
echo "Activating the virtual environment..."
source env/bin/activate

# Check if the main.py file exists
if [ -f "main.py" ]; then
    # Collect all arguments passed to the script
    arguments=$@
    echo "Running main.py with arguments: $arguments"
    python3 main.py $arguments
else
    echo "Error: main.py is not found in the current directory."
fi
