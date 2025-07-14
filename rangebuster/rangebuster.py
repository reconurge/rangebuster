"""
Rangebuster API - Core functionality for searching CIDRs.
"""

import os
from loguru import logger
from .common.utils import get_keywords_from_string_or_file, configure_logging
from .common.config import CACHE_PATH, sources
from .common.dependency_checker import check_dependencies
from .packages.rir_connector import RiRConnector
from .packages.arin_connector import ArinConnector



class RangeBuster:
    """Main class for searching CIDRs across RIR databases."""
    
    def __init__(self, keywords, strict=False, output_file=None, clear_cache=False, verbose=False):
        """
        Initialize RangeBuster.
        
        Args:
            keywords (str): Keywords to search for (comma-separated or file path)
            strict (bool): Perform strict keyword matching
            output_file (str): Output JSON file path
            clear_cache (bool): Clear cache before searching
            verbose (bool): Enable verbose logging
        """
        self.keywords = keywords
        self.strict = strict
        self.output_file = output_file
        self.clear_cache = clear_cache
        self.verbose = verbose
        self.results = []
        
        # Configure logging based on verbose mode
        configure_logging(verbose=self.verbose)
        
        # Check dependencies
        check_dependencies()
        
        # Create cache directory
        os.makedirs(CACHE_PATH, exist_ok=True)
        
        # Clear cache if requested
        if self.clear_cache:
            self._clear_cache()
    
    def _clear_cache(self):
        """Clear the cache directory."""
        try:
            import shutil
            if os.path.exists(CACHE_PATH):
                shutil.rmtree(CACHE_PATH)
                logger.info(f"✅ Cache cleared: {CACHE_PATH}")
            else:
                logger.warning(f"Cache path {CACHE_PATH} does not exist.")
        except PermissionError:
            logger.warning(f"Permission denied: Unable to remove '{CACHE_PATH}'.")
            logger.warning("If you want to clear the cache, please run with elevated permissions.")
        except Exception as e:
            logger.warning(f"An error occurred while trying to remove the cache: {e}")
    
    def search(self):
        """Perform the search across all RIR databases."""
        if self.strict:
            logger.info("Using strict mode.")
        
        # Download databases
        logger.info("Downloading RIR databases...")
        self._download_databases()
        
        # Search RIR databases
        logger.info("Searching RIR databases...")
        self._search_rir_databases()
        
        # Search ARIN database
        logger.info("Searching ARIN database...")
        self._search_arin_database()
        
        logger.success("✅ Search completed!")
        return self.results
    
    def _download_databases(self):
        """Download RIR databases."""
        # Use sequential processing instead of multiprocessing to avoid bootstrapping issues
        for section in sources:
            name = section['name']
            url = section['url']
            db_file = section['db_file']
            logger.debug(f"Downloading {name} database from {url}")
            rir_connector = RiRConnector(
                output_file=self.output_file, 
                keywords=self.keywords, 
                strict=self.strict, 
                source=name, 
                db_file=db_file
            )
            rir_connector.download_database(url, os.path.join(CACHE_PATH, db_file))
    
    def _search_rir_databases(self):
        """Search RIR databases."""
        # Use sequential processing instead of multiprocessing to avoid bootstrapping issues
        for section in sources:
            name = section['name']
            db_file = section['db_file']
            logger.debug(f"Searching {name} database")
            rir_connector = RiRConnector(
                output_file=self.output_file, 
                keywords=self.keywords, 
                strict=self.strict, 
                source=name, 
                db_file=db_file
            )
            rir_connector.run()
            self.results.extend(rir_connector.get_results())
    
    def _search_arin_database(self):
        """Search ARIN database."""
        logger.debug("Searching ARIN database")
        arin_connector = ArinConnector(
            keywords=get_keywords_from_string_or_file(self.keywords), 
            strict=self.strict, 
            output_file=self.output_file
        )
        arin_connector.search_database(self.output_file)
        
        # Collect ARIN results
        self.results.extend(arin_connector.get_results())
    
    def get_results(self):
        """Get the search results."""
        return self.results

def search_cidrs(keywords, strict=False, output_file=None, clear_cache=False, verbose=False):
    """
    Search CIDRs for given keywords across RIR databases.
    
    Args:
        keywords (str): Keywords to search for (comma-separated or file path)
        strict (bool): Perform strict keyword matching
        output_file (str): Output JSON file path
        clear_cache (bool): Clear cache before searching
        verbose (bool): Enable verbose logging
    
    Returns:
        list: List of CIDR results as dictionaries
    """
    range_buster = RangeBuster(
        keywords=keywords,
        strict=strict,
        output_file=output_file,
        clear_cache=clear_cache,
        verbose=verbose
    )
    return range_buster.search() 