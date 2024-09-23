# CIDR recon

This tool allows you to search CIDRs based on some keywords. The tool is based on free access RIR (Regional Internet Registry) databases. 

## Prerequisites

Make sure you have [ripgrep](https://github.com/BurntSushi/ripgrep) installed on you machine. In a future version, this tool will use [ripgrepy](https://pypi.org/project/ripgrepy/), but it's not the case for now.

## Install

Copy config file:

```bash
cp config.ini.example config.ini
```
Then create a virtual environment and install packages: 

```bash
virtualenv env && source env/bin/activate
pip3 install -r requirements.txt
```

Then make sure the tool works fine:

```bash
python3 main.py -h

usage: cidr_recon [-h] [-s] [-nc] [-o OUTPUT] keywords

Search RR/RIR database for keywords.

positional arguments:
  keywords              Keywords to search for. Separate multiple keywords with commas.

options:
  -h, --help            show this help message and exit
  -s, --strict          Perform strict keyword matching.
  -nc, --no_cache       Clear the cache folder (where databases are stored).
  -o OUTPUT, --output OUTPUT
                        Output filename (should end with .json)
```

## Usage

Without saving to json file, simply printing the inetnums:

```bash
python3 main.py tesla,solarcity

2024-09-23 15:19:28.552 | INFO     | Using cached cache/afrinic.db.gz.
2024-09-23 15:19:28.552 | INFO     | Using cached cache/lacnic.db.txt.
2024-09-23 15:19:28.554 | INFO     | Using cached cache/apnic.db.inetnum.gz.
2024-09-23 15:19:28.564 | INFO     | Using cached cache/ripe.gz.
[AFRINIC] 41.218.104.148/30 - ITG
[AFRINIC] 41.218.104.156/30 - ITG
[AFRINIC] 41.78.100.144/29 - Michelin_Tyres
[AFRINIC] 102.244.192.40/30 - Michelin_Douala
[AFRINIC] 102.177.113.250/31 - CMC-CERBA-LANCET-RWANDA
[AFRINIC] 102.177.113.252/31 - CMC-CERBA-LANCET-Kenya
2024-09-23 15:19:29.028 | SUCCESS  | Found 7 matches for [afrinic].
[APNIC] 203.125.189.64/26 - MICHELIN-SG
[APNIC] 202.95.76.128/27 - MICHELIN-SG
[APNIC] 202.95.77.184/29 - MICHELIN-SG
[APNIC] 202.95.93.96/27 - MICHELIN-SG
[APNIC] 58.246.87.172/30 - Michelin
[APNIC] 124.83.35.155/32 - BIZONEZERO
...
[RIPE] 87.241.50.152/29 - NET-IT-Tesla-Italy-Srl
[RIPE] 217.111.255.184/29 - NET-BE-Tesla-Belgium
[RIPE] 212.161.79.192/29 - NET-BE-Tesla-Belgium
[RIPE] 213.215.131.112/29 - NET-IT-Tesla-Italy
[RIPE] 78.143.2.248/29 - NET-PL-Tesla-Poland
2024-09-23 15:25:35.804 | SUCCESS  | Found 693 matches for [ripe].
2024-09-23 15:25:35.834 | SUCCESS  | Finished in 0min 4.76s
```

Saving to output file:

```bash
python3 main.py tesla,solarcity -o output.json
```
