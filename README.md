# Rangebuster

This tool allows you to search CIDRs based on some keywords. The tool is based on free access RIR (Regional Internet Registry) databases. 

## Prerequisites

Make sure you have the following installed on you machine:
- [ripgrep](https://github.com/BurntSushi/ripgrep)
- [virtualenv](https://virtualenv.pypa.io/en/latest)
- [whois](https://who.is)

You can install them very easily with your package manager:

```bash
# Ubuntu/Debian
sudo apt install ripgrep virtualenv whois
# MacOS with brew
brew install ripgrep virtualenv whois
```

## Quick run

A script `run.sh` is provided to run this tool as simply as possible. Simply: 

```bash
chmod +x run.sh
```
And :

```bash
./run.sh -h
```

#### Example

```bash
./run.sh canik -s

Activating the virtual environment...
Running main.py with arguments: canik -s
2024-09-24 23:05:46.663 | INFO     | Using strict mode.
2024-09-24 23:05:46.913 | INFO     | Using cached /var/tmp/rir/afrinic.db.gz.
2024-09-24 23:05:46.923 | INFO     | Using cached /var/tmp/rir/apnic.db.inetnum.gz.
2024-09-24 23:05:46.925 | INFO     | Using cached /var/tmp/rir/lacnic.db.txt.
2024-09-24 23:05:46.933 | INFO     | Using cached /var/tmp/rir/ripe.gz.
2024-09-24 23:05:47.406 | INFO     | No record found for afrinic.
2024-09-24 23:05:47.633 | INFO     | No record found for lacnic.
2024-09-24 23:05:47.751 | INFO     | No record found for apnic.
[RIPE] 95.0.89.224/29 - Medicana_Samsun_Ozel_Saglik_Hizmetleri_AS
[RIPE] 95.0.135.96/27 - metro_ethernet_alsat_coklu_IP
[RIPE] 185.19.203.0/24 - TR-CANIK-20220629
[RIPE] 88.255.105.72/29 - metro_ethernet_alsat_coklu_IP
2024-09-24 23:05:50.710 | SUCCESS  | Found 4 matches for [ripe].
2024-09-24 23:05:50.739 | SUCCESS  | Finished in 0min 4.08s
```

## Basic install

Create a virtual environment and install packages: 

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
2024-09-23 15:19:29.028 | SUCCESS  | Found 6 matches for [afrinic].
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
python3 main.py ubuntu -o output.json
```
This is the kind of output you can expect:

```js
[
    {
        "object_type": "cidr",
        "source": "ripe",
        "netname": "ubuntu",
        "first_ip": "87.79.26.32",
        "last_ip": "87.79.26.47",
        "cidr": [
            "87.79.26.32/28"
        ],
        "inetnum": "87.79.26.32 - 87.79.26.47",
        "keyword": "ubuntu",
        "description": "ubuntu Deutschland e. V., Geibelstr.45, 30173 Hannover",
        "discovered_at": [
            "2025-01-08 16:10:26.765346"
        ],
        "country": "DE",
        "whois": {
            "inetnum": "87.79.26.32 - 87.79.26.47",
            "netname": "ubuntu",
            "descr": "ubuntu Deutschland e. V., Geibelstr.45, 30173 Hannover",
            "country": "DE",
            "admin-c": "DUMY-RIPE",
            "tech-c": "DUMY-RIPE",
            "status": "ASSIGNED PA",
            "mnt-by": "NETCOLOGNE-MNT",
            "mnt-lower": "NETCOLOGNE-MNT",
            "created": "2010-08-05T15:10:46Z",
            "last-modified": "2010-08-05T15:10:46Z",
            "source": "RIPE",
            "remarks": "****************************, * THIS OBJECT IS MODIFIED, * Please note that all data that is generally regarded as personal, * data has been removed from this object., * To view the original object, please query the RIPE Database at:, * http://www.ripe.net/whois, ****************************"
        }
    },
    {
        "object_type": "cidr",
        "source": "ripe",
        "netname": "SNI682387166_000275",
        "first_ip": "77.61.100.144",
        "last_ip": "77.61.100.147",
        "cidr": [
            "77.61.100.144/30"
        ],
        "inetnum": "77.61.100.144 - 77.61.100.147",
        "keyword": "ubuntu",
        "description": "Ubuntu Beach CV, NOORDWIJK ZH",
        "discovered_at": [
            "2025-01-08 16:10:26.766486"
        ],
        "country": "NL",
        "whois": {
            "inetnum": "77.61.100.144 - 77.61.100.147",
            "netname": "SNI682387166_000275",
            "descr": "Ubuntu Beach CV, NOORDWIJK ZH",
            "country": "NL",
            "admin-c": "DUMY-RIPE",
            "tech-c": "DUMY-RIPE",
            "status": "ASSIGNED PA",
            "notify": "kpn-ip-office@kpn.com",
            "mnt-by": "AS286-MNT",
            "created": "2013-02-12T07:54:37Z",
            "last-modified": "2013-02-12T07:54:37Z",
            "source": "RIPE",
            "remarks": "****************************, * THIS OBJECT IS MODIFIED, * Please note that all data that is generally regarded as personal, * data has been removed from this object., * To view the original object, please query the RIPE Database at:, * http://www.ripe.net/whois, ****************************"
        }
    }
...
]
``` 
