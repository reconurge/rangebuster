#!/usr/bin/env python3
"""
Rangebuster CLI - Command line interface for searching CIDRs.
"""

import argparse
import time
from loguru import logger
from rangebuster import search_cidrs, __version__
from rangebuster.common.utils import get_duration, configure_logging

def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        prog="rangebuster",
        description="Search RIR and ARIN databases for keywords to find CIDR ranges.",
        epilog="Example: rangebuster tesla,solarcity -s -o results.json"
    )
    parser.add_argument(
        "keywords", 
        help="Keywords to search for. Separate multiple keywords with commas or provide a file path ending with .txt"
    )
    parser.add_argument(
        "-s", "--strict", 
        action="store_true", 
        help="Perform strict keyword matching (exact word boundaries)"
    )
    parser.add_argument(
        "-nc", "--no_cache", 
        action="store_true", 
        help="Clear the cache folder (where databases are stored)"
    )
    parser.add_argument(
        '-o', '--output', 
        type=str, 
        default=None, 
        help='Output filename (should end with .json)'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging (DEBUG level)'
    )
    parser.add_argument(
        '--version',
        action='version',
        version=f'rangebuster {__version__}'
    )

    args = parser.parse_args()

    # Configure logging based on verbose argument
    configure_logging(verbose=args.verbose)

    # Perform the search
    start_time = time.time()
    
    try:
        results = search_cidrs(
            keywords=args.keywords,
            strict=args.strict,
            output_file=args.output,
            clear_cache=args.no_cache,
            verbose=args.verbose
        )
        
        end_time = time.time()
        finished = get_duration(start_time, end_time)
        logger.warning(f"Finished in {finished}")
        
        # Print summary
        if results:
            logger.warning(f"Found {len(results)} CIDR ranges")
        else:
            logger.warning("No CIDR ranges found")
            
    except KeyboardInterrupt:
        logger.warning("Search interrupted by user")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 