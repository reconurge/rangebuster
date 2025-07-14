import json

class Connector:
    def __init__(self, keywords, strict, source, output_file):
        self.keywords = keywords
        self.strict = strict
        self.source = source
        self.output_file = output_file
        self.results = []
        self.seen_inetnums = set()

        
    def search_database(self):
        pass
    
    def get_results(self):
        return self.results
    
    def save(self):
        if not self.output_file:
            return
        with open(self.output_file, 'w') as json_file:
            json.dump(self.results, json_file, indent=4, default=str)