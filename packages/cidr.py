from datetime import datetime
import json
from colorama import init, Fore # type: ignore
from loguru import logger

class CIDRInfo:
    def __init__(self, result, first_ip, last_ip, cidr, keyword="None", matches=[], source="None"):
        self.object_type = "cidr"
        self.source = source or (result["source"].lower() if "source" in result else None)
        self.netname = result["netname"] if "netname" in result else "No netname"
        self.first_ip = first_ip
        self.last_ip = last_ip
        self.cidr = cidr
        self.inetnum = result["inetnum"] if "inetnum" in result else "No inetnum"
        self.keyword = keyword
        self.matches=matches
        self.description = result["descr"] if "descr" in result else "No description"
        self.discovered_at = [str(datetime.now())]
        self.country = result["country"] if "country" in result else "No country"
        self.whois = result

    def to_dict(self):
        return {
            "object_type": self.object_type,
            "source": self.source,
            "netname": self.netname,
            "first_ip": self.first_ip,
            "last_ip": self.last_ip,
            "cidr": self.cidr,
            "inetnum": self.inetnum,
            "keyword": self.keyword,
            "description": self.description,
            "discovered_at": self.discovered_at,
            "country": self.country,
            "whois": self.whois
        }

    def to_json(self):
        return json.dumps(self.to_dict(), indent=4)

    def log(self):
         logger.success(f"[{self.source.upper()}] {', '.join(self.cidr)} - {self.netname}")
         
    def to_string(self):
        logger.info("CIDR Information:")
        for key, value in self.to_dict().items():
            logger.info(f"{key}:" + f"{Fore.GREEN} {value}")