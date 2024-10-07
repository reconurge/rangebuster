import requests
import json
import subprocess
import re
from datetime import datetime
from common.utils import parse_inetnum
from packages.cidr import CIDRInfo
from packages.connector import Connector
import xml.etree.ElementTree as ET  
from common.utils import logger

class ArinConnector(Connector):
    def __init__(self, keywords, strict, output_file):
        super().__init__(keywords, strict, source="arin", output_file=output_file)
        
    def process_element(self, element):
        data = {}
        for child in element:
            tag = child.tag.split('}')[1] 
            if child.text and child.text.strip(): 
                data[tag] = child.text
        return data

    def get_whois_arin(self, net_id):
        try:
            url = f'https://whois.arin.net/rest/net/{net_id}'
            response = requests.get(url)
            # Raises an HTTPError if the HTTP request returns an error status code
            response.raise_for_status()
            root = ET.fromstring(response.content)
            data = self.process_element(root)
            json_data = json.dumps(data, indent=4, default=str)
            return json_data
        except requests.exceptions.HTTPError as errh:
            logger.error("HTTP Error:", errh)
            return ""
        except requests.exceptions.ConnectionError as errc:
            logger.error("Error Connecting:", errc)
            return ""
        except requests.exceptions.Timeout as errt:
            logger.error("Timeout Error:", errt)
            return ""
        except requests.exceptions.RequestException as err:
            logger.error("Something went wrong:", err)
            return ""

    def search_database(self, output_file):
        record_types = ['e']  # Record types for ARIN searches
        if output_file:
            try:
                with open(output_file, 'r') as json_file:
                    self.results = json.load(json_file)
            except FileNotFoundError:
                self.results = []

        for record_type in record_types:
            for keyword in self.keywords:
                cmd = f'whois -h whois.arin.net "{record_type} {keyword}"'
                output = subprocess.check_output(cmd, shell=True, universal_newlines=True)
                parsed_results = self._parse_arin_output(output)

                for result in parsed_results:
                    if result['inetnum'] not in self.seen_inetnums:
                        first_ip, last_ip, cidr = parse_inetnum(result['inetnum'])
                        whois = json.loads(self.get_whois_arin(result["description"]))
                        cidr = CIDRInfo(
                            result=whois,
                            first_ip=first_ip,
                            last_ip=last_ip,
                            cidr=cidr, 
                            keyword=keyword, 
                            source=self.source
                        )
                        cidr.log()
                        self.results.append(cidr.to_dict())
                        self.seen_inetnums.add(cidr.to_dict()['inetnum'])

        self.save()

    # Private method to parse ARIN whois output
    def _parse_arin_output(self, output):
        pattern = r'\(([^)]+)\)\s+(\d+\.\d+\.\d+\.\d+)\s+-\s+(\d+\.\d+\.\d+\.\d+)'
        matches = re.findall(pattern, output)
        return [{'description': match[0], 'inetnum': f'{match[1]} - {match[2]}'}
                for match in matches]
