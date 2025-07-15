# Rangebuster

A powerful tool to search CIDRs based on keywords using Regional Internet Registry (RIR) databases. This tool allows you to discover IP ranges associated with specific keywords across multiple RIR databases.

## Features

- Search across multiple RIR databases (AFRINIC, APNIC, LACNIC, RIPE, ARIN)
- Support for multiple keywords and keyword files
- Strict and fuzzy keyword matching modes
- JSON output with detailed results
- Fast search using ripgrep
- Pure Python implementation with CLI interface
- Installable as a Python package
- Usable as a Python module
- Verbose logging option for debugging

## Prerequisites

### System dependencies

Make sure you have the following installed on your machine:

- [ripgrep](https://github.com/BurntSushi/ripgrep) - Fast text search tool

You can install ripgrep with your package manager:

```bash
# Ubuntu/Debian
sudo apt install ripgrep

# macOS with Homebrew
brew install ripgrep

# Windows with Chocolatey
choco install ripgrep

# Or download from: https://github.com/BurntSushi/ripgrep/releases
```

## Installation

### Option 1: Install as a python package (recommended)

```bash
# Install from PyPI (when available)
pip install git+https://github.com/reconurge/rangebuster

# Or install from source
git clone https://github.com/reconurge/rangebuster.git
cd rangebuster
pip install -e .
```

### Option 2: manual installation

```bash
# Clone the repository
git clone https://github.com/reconurge/rangebuster.git
cd rangebuster

# Create virtual environment
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### As a python package (CLI)

```bash
# Basic usage
rangebuster tesla,solarcity

# With strict matching
rangebuster tesla -s

# Save results to file
rangebuster tesla -o results.json

# Clear cache and search
rangebuster tesla -nc -o results.json

# Use keyword file
echo "tesla\nsolarcity" > keywords.txt
rangebuster keywords.txt -s -o results.json

# Enable verbose logging
rangebuster tesla -v

# Combine options
rangebuster tesla -s -v -o results.json
```

### As a python module

```bash
# add to requirements.txt
https://github.com/reconurge/rangebuster
# or install in your venv
pip install https://github.com/reconurge/rangebuster
````

Then you can use it as a module.

```python
from rangebuster import search_cidrs

# Basic search
results = search_cidrs("tesla,solarcity")
for result in results:
    print(f"{result['cidr']} - {result['netname']}")

# With options
results = search_cidrs(
    keywords="tesla",
    strict=True,
    output_file="results.json",
    clear_cache=False,
    verbose=True
)

# Using the RangeBuster class
from rangebuster import RangeBuster

rb = RangeBuster(
    keywords="tesla,solarcity",
    strict=True,
    output_file="results.json",
    verbose=True
)
results = rb.search()
```

### As a script

```bash
# Basic usage
python cli.py tesla,solarcity

# With strict matching
python cli.py tesla -s

# Save results to file
python cli.py tesla -o results.json

# Clear cache and search
python cli.py tesla -nc -o results.json

# Enable verbose logging
python cli.py tesla -v
```

## Command line options

```
usage: rangebuster [-h] [-s] [-nc] [-o OUTPUT] [-v] [--version] keywords

Search RIR and ARIN databases for keywords to find CIDR ranges.

positional arguments:
  keywords              Keywords to search for. Separate multiple keywords with commas or provide a file path ending with .txt

options:
  -h, --help            show this help message and exit
  -s, --strict          Perform strict keyword matching (exact word boundaries)
  -nc, --no_cache       Clear the cache folder (where databases are stored)
  -o OUTPUT, --output OUTPUT
                        Output filename (should end with .json)
  -v, --verbose         Enable verbose logging (DEBUG level)
  --version             show program's version number and exit
```

## Examples

### Basic search

```bash
rangebuster tesla

# Output (with verbose mode):
# [INFO] All dependencies are available
# [INFO] Downloading RIR databases...
# [INFO] Searching RIR databases...
# [INFO] Searching ARIN database...
# [RIPE] 87.79.26.32/28 - ubuntu
# [RIPE] 77.61.100.144/30 - SNI682387166_000275
# [INFO] Search completed!
# [INFO] Finished in 0min 4.08s
```

### Strict matching

```bash
rangebuster tesla -s

# This will only match exact word boundaries, not partial matches
```

### Save Results to JSON

```bash
rangebuster tesla -o tesla_results.json
```

### Multiple keywords

```bash
rangebuster tesla,solarcity,spacex -o results.json
```

### Using keyword file

```bash
# Create keywords file
echo -e "tesla\nsolarcity\nspacex" > keywords.txt

# Search with file
rangebuster keywords.txt -s -o results.json
```

### Verbose logging

```bash
# Enable verbose logging for debugging
rangebuster tesla -v

# This will show detailed DEBUG level logs including:
# - Database download progress
# - Search operations
# - File operations
# - Timing information
```

### Python module usage

```python
from rangebuster import search_cidrs

# Simple search
results = search_cidrs("tesla")
for result in results:
    print(f"{result['cidr']} - {result['netname']}")

# Advanced usage
results = search_cidrs(
    keywords="tesla,solarcity",
    strict=True,
    output_file="results.json",
    clear_cache=True,
    verbose=True
)

# Process results
for result in results:
    print(f"Source: {result['source']}")
    print(f"CIDR: {result['cidr']}")
    print(f"Netname: {result['netname']}")
    print(f"Description: {result['description']}")
    print("---")
```

## Output format

The tool outputs results in JSON format with the following structure:

```json
[
    {
        "object_type": "cidr",
        "source": "ripe",
        "netname": "ubuntu",
        "first_ip": "87.79.26.32",
        "last_ip": "87.79.26.47",
        "cidr": ["87.79.26.32/28"],
        "inetnum": "87.79.26.32 - 87.79.26.47",
        "keyword": "tesla",
        "description": "Tesla Motors, Inc.",
        "discovered_at": ["2025-01-08 16:10:26.765346"],
        "country": "US",
        "whois": {
            "inetnum": "87.79.26.32 - 87.79.26.47",
            "netname": "ubuntu",
            "descr": "Tesla Motors, Inc.",
            "country": "US",
            "status": "ASSIGNED PA",
            "source": "RIPE"
        }
    }
]
```

## Supported RIR databases

- **AFRINIC** - African Network Information Centre
- **APNIC** - Asia Pacific Network Information Centre  
- **LACNIC** - Latin America and Caribbean Network Information Centre
- **RIPE** - Réseaux IP Européens Network Coordination Centre
- **ARIN** - American Registry for Internet Numbers

## Cache management

The tool caches downloaded RIR databases in `/var/tmp/rir/` by default. You can:

- Clear cache: `rangebuster keyword -nc`
- Change cache location: Set `RIR_OUTPUT_PATH` environment variable

## Logging

The tool supports two logging modes:

- **Normal mode** (default): Shows only ERROR, WARNING messages and final results
- **Verbose mode** (`-v` or `--verbose`): Shows detailed DEBUG level logs including:
  - Database download progress
  - Search operations
  - File operations
  - Timing information
  - Function calls and line numbers

## Troubleshooting

### Missing `ripgrep`

If you get an error about ripgrep not being found:

```bash
# Ubuntu/Debian
sudo apt install ripgrep

# macOS
brew install ripgrep

# Windows
choco install ripgrep
```

### Permission issues

If you encounter permission issues with cache:

```bash
# Run with sudo (Linux/macOS)
sudo rangebuster <keyword>

# Or change cache location
export RIR_OUTPUT_PATH=/tmp/rangebuster_cache
rangebuster <keyword>
```

### Debugging issues

If you need to debug issues:

```bash
# Enable verbose logging
rangebuster keyword -v

# This will show detailed logs to help identify problems
```

## Development

### Setup development environment

```bash
git clone https://github.com/reconurge/rangebuster.git
cd rangebuster
python -m venv env
source env/bin/activate
pip install -r requirements.txt
pip install -e .
```

### Package structure

```
rangebuster/
├── rangebuster/          # Main package
│   ├── __init__.py      # Package initialization
│   ├── rangebuster.py   # Core API functionality
│   ├── common/          # Common utilities
│   │   ├── config.py
│   │   ├── utils.py
│   │   └── dependency_checker.py
│   └── packages/        # RIR connectors
│       ├── rir_connector.py
│       ├── arin_connector.py
│       ├── cidr.py
│       └── cidr_parser.py
├── cli.py               # Command line interface
├── setup.py             # Package setup
├── requirements.txt     # Dependencies
└── README.md           # Documentation
```

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/reconurge/rangebuster/blob/main/LICENCE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Acknowledgments

- Built with [ripgrep](https://github.com/BurntSushi/ripgrep) for fast text search
- Uses [python-whois](https://github.com/richardpenman/python-whois) for WHOIS lookups
- Inspired by the need for efficient CIDR discovery in security research 
