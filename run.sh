#!/bin/bash

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to check and install ripgrep
check_ripgrep() {
    if ! command -v rg &> /dev/null; then
        echo -e "${RED}ripgrep is not installed. Please install it using your package manager.${NC}"
        echo -e "${YELLOW}For example, on Ubuntu/Debian you can run: sudo apt install ripgrep${NC}"
        echo -e "${YELLOW}On macOS, you can run: brew install ripgrep${NC}"
        exit 1
    fi
}

# Check for ripgrep
check_ripgrep

# Check if the virtual environment directory exists
if [ ! -d "env" ]; then
    echo -e "${BLUE}No virtual environment found. Creating one...${NC}"
    virtualenv env
    echo -e "${BLUE}Installing requirements.txt...${NC}"
    pip3 install -r requirements.txt
fi

# Activate the virtual environment
echo -e "${BLUE}Activating the virtual environment...${NC}"
source env/bin/activate

# Check if the main.py file exists
if [ -f "main.py" ]; then
    # Collect all arguments passed to the script
    arguments=$@
    echo -e "${GREEN}Running main.py with arguments: $arguments${NC}"
    python3 main.py $arguments
else
    echo -e "${RED}Error: main.py is not found in the current directory.${NC}"
fi
