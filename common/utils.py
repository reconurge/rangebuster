from configparser import ConfigParser
import os
import ipaddress
from loguru import logger
logger.remove()
logger.add(lambda msg: print(msg, end=''), colorize=True, format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <level>{message}</level>", level="INFO", diagnose=False)


def use_config():
    config = ConfigParser()
    config_path = "config.ini"
    config.read(config_path)
    return config

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
                raise ValueError("Invalid input format")

            return str(first_ip), str(last_ip), cidr

        except Exception as e:
            return str(e), None, None
        
        