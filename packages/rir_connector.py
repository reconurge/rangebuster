from datetime import datetime
import subprocess
from packages.cidr_parser import CIDRParser
from packages.connector import Connector
import os
import requests
import re
from colorama import Fore
from utils import get_keywords_from_string_or_file
from loguru import logger

logger.remove()  # Remove the default configuration (file handler)
logger.add(lambda msg: print(msg, end=''), colorize=True, format="<green>{HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <level>{message}</level>", level="INFO", diagnose=False)

INDEXES = {
    "afrinic": 1, 
    "lacnic": 2,
    "apnic": 3,
    "ripe": 4,
}

class RiRConnector(Connector):
    def __init__(self, output_file, keywords, strict, source, db_file):
        super().__init__(output_file = output_file, keywords = keywords, strict = strict, source = source)
        self.db_file = os.path.join("cache", db_file)
        
    def download_database(self, url, output_filename):
        download_message = f"Downloading {output_filename}..."
        if not os.path.exists(output_filename):
            try:
                response = requests.get(url, stream=True)
                block_size = 1024  # 1 Kibibyte

                with open(output_filename, 'wb') as file:
                    for data in response.iter_content(chunk_size=block_size):
                        file.write(data)
                download_message = f'Downloaded {output_filename} successfully.'
                logger.info(download_message)

            except ConnectionError:
                logger.error(f"An error occurred downloading {output_filename}.")

        else:
            logger.info(f'Using cached {output_filename}.')

    def search_database(self):
        output_grep_file = f'{self.db_file}.txt'
        keywords = get_keywords_from_string_or_file(self.keywords)

        if self.db_file.endswith("gz"):
            args = "-aizINw" if self.strict else "-aizIN"
            if self.keywords.endswith('.txt'):
                grep_command = f"rg {args} -f {os.path.join('.', self.keywords)} {self.db_file} -C 30 > {output_grep_file}"
            else:
                keyword_file_new = os.path.join(".", f"keywords_{str(datetime.now().strftime('%d%m%y%H%M%S'))}.txt")
                with open(keyword_file_new, "w") as file:
                    for keyword in keywords:
                        file.write(f"{keyword}\n")

                grep_command = f"rg {args} -f {os.path.join('.', keyword_file_new)} {self.db_file} -C 30 > {output_grep_file}"

        else:
            grep_command = f"grep -i -E -A 30 '\\b{'|'.join(map(re.escape, keywords))}\\b' {self.db_file} > {output_grep_file}"
        
        if self.strict:
            logger.info("STRICT")

        result = subprocess.run(grep_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if result.returncode == 0:
            self._process_grep_results(output_grep_file, keywords)
        else:
            logger.info(f"No record found for {self.source}.")

    def _process_grep_results(self, output_grep_file, keywords):
        try:
            with open(output_grep_file, 'r', encoding='utf-8', errors='ignore') as file:
                results = []
                entry = []
                in_entry = False
                file.seek(0)

                for _, line in enumerate(file, start=1):
                    if not in_entry and line.strip() == "":
                        continue
                    if in_entry:
                        entry.append(line)
                        if line.strip() == "":
                            in_entry = False
                            matched_keywords = [keyword for keyword in keywords if (re.search(r'\b{}\b'.format(re.escape(keyword)), ''.join(entry), re.IGNORECASE)
                                if self.strict else re.search(r'{}\b|\w*{}\w*'.format(re.escape(keyword), re.escape(keyword)), ''.join(entry), re.IGNORECASE))]
                            
                            if matched_keywords:
                                results.append(''.join(entry))
                                for matched_keyword in matched_keywords:
                                    cidr_parser = CIDRParser(entry, matched_keyword, self.output_file, self.source)
                                    cidrs = cidr_parser._process_entries()  # Now this returns a list of CIDRInfo objects
                                    for cidr in cidrs:
                                        if cidr.to_dict()['inetnum'] not in self.seen_inetnums:
                                            cidr.log()
                                            self.results.append(cidr.to_dict())
                                            self.seen_inetnums.add(cidr.to_dict()['inetnum'])

                            entry = []
                    else:
                        in_entry = True
                        entry.append(line)

                logger.success(f"Found {len(results)} matches for [{self.source}].")

                self.save()
        except OSError:
            logger.error(Fore.RED + f'Could not open {output_grep_file}.')

    def run(self):
        self.search_database()
