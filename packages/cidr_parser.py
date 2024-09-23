import json
from multiprocessing import Lock
import re
from packages.cidr import CIDRInfo
from utils import parse_inetnum

class CIDRParser:
    def __init__(self, entry, keyword, output_file, source='No source'):
        self.output_file = output_file
        self.source = source
        self.file_lock = Lock()
        self.entry = entry
        self.keyword = keyword
        self.results = []
        self._process_entries()

    def _save_results(self):
        with self.file_lock:
            with open(self.output_file, 'w') as json_file:
                json.dump(self.results, json_file, indent=4, default=str)

    def _find_keyword_occurrences(self, entry):
        pattern = re.compile(r'\b\w*' + re.escape(self.keyword) + r'\w*\b', re.IGNORECASE)
        return pattern.findall(entry)

    def _process_entries(self):
        current_entry = {}
        
        for line in self.entry:
            line = line.strip()
            matches = self._find_keyword_occurrences(line)

            if line:
                if ":" in line:
                    key, value = map(str.strip, line.split(":", 1))
                    if key in current_entry:
                        current_entry[key] = current_entry[key] if isinstance(current_entry[key], list) else [current_entry[key]]
                        current_entry[key].append(value)
                    else:
                        current_entry[key] = value
            else:
                if current_entry:
                    cidr_result = self._finalize_entry(current_entry, matches)
                    if cidr_result:
                        self.results.append(cidr_result)
                    current_entry = {}

        if current_entry:
            cidr_result = self._finalize_entry(current_entry, matches)
            if cidr_result:
                self.results.append(cidr_result)

        return self.results


    def _finalize_entry(self, current_entry, matches):
        for key, value in current_entry.items():
            if isinstance(value, list):
                current_entry[key] = ", ".join(value)

        inetnum = current_entry.get("inetnum")
        if not inetnum:
            inetnum = "No inetnum found."

        first_ip, last_ip, cidr = parse_inetnum(inetnum)
        if not first_ip or not last_ip or not cidr:
            return

        return CIDRInfo(
            result=current_entry,
            first_ip=first_ip,
            last_ip=last_ip,
            cidr=cidr, 
            keyword=self.keyword, 
            matches=matches, 
            source=self.source
        )
