import datetime
import os

import whois
from prettytable import PrettyTable

# Change the working directory to the script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Function to select and query the appropriate WHOIS server
def query_whois(domain):
    tld = domain.split('.')[-1]
    whois_servers = {
        'com': 'whois.verisign-grs.com',
        'net': 'whois.verisign-grs.com',
        'org': 'whois.pir.org',
        'gov': 'whois.nic.gov',
        'edu': 'whois.educause.edu',
        'pt': 'whois.dns.pt',
        'io': 'whois.nic.io'
    }
    whois_server = whois_servers.get(tld, f'whois.iana.org {tld}')
    print(f'Whois Server used: {whois_server}\n')
    return whois.whois(domain, whois_server)

if __name__ == "__main__":
    print("""\
     _    _ _   _ _____ _____ _____
    | |  | | | | |  _  |_   _/  ___|
    | |  | | |_| | | | | | | \ `--.  ___ ___  _ __   ___
    | |/\| |  _  | | | | | |  `--. \/ __/ _ \| '_ \ / _ \\
    \  /\  / | | \ \_/ /_| |_/\__/ / (_| (_) | |_) |  __/
     \/  \/\_| |_/\___/ \___/\____/ \___\___/| .__/ \___|
                                             | |
    by NotoriusNeo                           |_|         """)
    print("WHOIS Domain Lookup Tool")
    domain = input("Enter domain to check: ")

    table = PrettyTable(['Attribute', 'Value'])
    table.hrules = 0
    table.vertical_char = "|"
    table.junction_char = "|"
    table.sortby = "Attribute"
    table.align['Value'] = "l"

    for attr, value in query_whois(domain).items():
        if value is not None:
            if isinstance(value, list) and all(isinstance(x, datetime.datetime) for x in value):
                # if the value is a list of datetime objects, add each element to the table on a separate line
                for v in value:
                    table.add_row([attr, v])
            else:
                table.add_row([attr, value])

    # print the table to a file with the current timestamp in the filename
    filename = f"{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_whois_{domain}.txt"
    with open(filename, 'w') as f:
        f.write(str(table))
        print(f"Table saved to file: {filename}")
