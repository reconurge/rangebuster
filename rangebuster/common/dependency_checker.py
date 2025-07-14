import subprocess
import sys
from loguru import logger

def check_ripgrep():
    """Check if ripgrep is installed and available."""
    try:
        result = subprocess.run(['rg', '--version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        if result.returncode == 0:
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass
    
    logger.error("❌ ripgrep (rg) is not installed or not available in PATH")
    logger.error("Please install ripgrep using your package manager:")
    logger.error("  Ubuntu/Debian: sudo apt install ripgrep")
    logger.error("  macOS: brew install ripgrep")
    logger.error("  Windows: choco install ripgrep")
    logger.error("  Or download from: https://github.com/BurntSushi/ripgrep/releases")
    return False

def check_python_whois():
    """Check if python-whois is available."""
    try:
        import whois
        return True
    except ImportError:
        logger.error("❌ python-whois is not installed")
        logger.error("Please install it with: pip install python-whois")
        return False

def check_dependencies():
    """Check all required dependencies."""
    ripgrep_ok = check_ripgrep()
    whois_ok = check_python_whois()
    
    if not ripgrep_ok or not whois_ok:
        logger.error("❌ Missing required dependencies. Please install them and try again.")
        sys.exit(1)
    
    logger.success("✅ All dependencies are available")
    return True 