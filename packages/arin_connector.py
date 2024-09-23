import requests
import json
import subprocess
import re
from datetime import datetime
from utils import parse_inetnum
from packages.connector import Connector
import xml.etree.ElementTree as ET  


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
            print("HTTP Error:", errh)
            return ""
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
            return ""
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
            return ""
        except requests.exceptions.RequestException as err:
            print("Something went wrong:", err)
            return ""

    def search_database(self, output_file):
        record_types = ['e']  # Record types for ARIN searches
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
                        discovered_at = str(datetime.now())
                        whois = json.loads(self.get_whois_arin(result["description"]))

                        entry = {
                            "object_type": "cidr",
                            'source': self.source,
                            "netname": whois["name"],
                            "first_ip": first_ip,
                            "last_ip": last_ip,
                            "cidr": cidr,
                            "inetnum": result['inetnum'],
                            "keyword": keyword,
                            "description": result["description"],
                            "discovered_at": [discovered_at],
                            "status": 'To verify',
                            "country": "",  # Country info may not be available in ARIN
                            "whois": whois
                        }
                        self.results.append(entry)
                        self.seen_inetnums.add(result['inetnum'])

        self.save()

    # Private method to parse ARIN whois output
    def _parse_arin_output(self, output):
        pattern = r'\(([^)]+)\)\s+(\d+\.\d+\.\d+\.\d+)\s+-\s+(\d+\.\d+\.\d+\.\d+)'
        matches = re.findall(pattern, output)
        return [{'description': match[0], 'inetnum': f'{match[1]} - {match[2]}'}
                for match in matches]
