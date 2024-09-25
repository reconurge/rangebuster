#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

check_ripgrep() {
    if ! command -v rg &> /dev/null; then
        echo -e "${RED}ripgrep is not installed. Please install it using your package manager.${NC}"
        echo -e "${YELLOW}For example, on Ubuntu/Debian you can run: sudo apt install ripgrep${NC}"
        echo -e "${YELLOW}On macOS, you can run: brew install ripgrep${NC}"
        exit 1
    fi
}

check_ripgrep

if [ ! -d "env" ]; then
    echo -e "${BLUE}No virtual environment found. Creating one...${NC}"
    virtualenv env
    source env/bin/activate
    echo -e "${BLUE}Installing requirements.txt...${NC}"
    pip3 install -r requirements.txt
fi

echo -e "${BLUE}Activating the virtual environment...${NC}"
source env/bin/activate

if [ -f "main.py" ]; then
    arguments=$@
    echo -e "${GREEN}Running main.py with arguments: $arguments${NC}"
    python3 main.py $arguments
else
    echo -e "${RED}Error: main.py is not found in the current directory.${NC}"
fi
