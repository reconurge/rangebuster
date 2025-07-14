from configparser import ConfigParser
import os
import ipaddress
from loguru import logger

def configure_logging(verbose=False):
    """Configure logging based on verbose mode. If not verbose, suppress all logging output."""
    logger.remove()  # Remove existing handlers
    
    if verbose:
        # Verbose mode: show DEBUG level and more detailed format
        logger.add(
            lambda msg: print(msg, end=''), 
            colorize=True, 
            format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | <level>{message}</level>", 
            level="DEBUG", 
            diagnose=False
        )
    # else: do not add any handler, so no logs are shown

# Initialize with default (non-verbose) logging (no output)
configure_logging(verbose=False)

def get_duration(start, end):
    duration_seconds = end - start
    duration_minutes = int(duration_seconds // 60)
    duration_seconds %= 60
    duration_string = f"{duration_minutes}min {duration_seconds:.2f}s"
    return duration_string

def get_keywords_from_string_or_file(keywords_arg):

    if ',' in keywords_arg:
        return [kw.strip() for kw in keywords_arg.split(',')]
    else:
        try:
            with open(keywords_arg, 'r') as file:
                return [kw.strip() for kw in file.readlines()]
        except Exception:
            return [keywords_arg]
        
def parse_inetnum(value):
    try:
        if '-' in value:
            ip1, ip2 = map(str.strip, value.split('-'))
            first_ip = ipaddress.IPv4Address(ip1)
            last_ip = ipaddress.IPv4Address(ip2)
            network = ipaddress.summarize_address_range(first_ip, last_ip)
            cidr = [str(cidr) for cidr in network]

        elif '/' in value:
            network = ipaddress.IPv4Network(value, strict=False)
            first_ip = network.network_address
            last_ip = network.broadcast_address
            cidr = [str(network)]
        else:
            return None, None, None

        return str(first_ip), str(last_ip), cidr

    except Exception as e:
        return None, None, None
        
        