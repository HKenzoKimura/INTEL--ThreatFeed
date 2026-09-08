import sys
import requests
import pandas as pd
import re
import json
import urllib3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTextEdit

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_ips_from_feeds(feeds):
    default_headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    all_ips = []

    for feed in feeds:
        headers = feed.get('headers', default_headers)
        response = requests.get(feed['url'], headers=headers, params=feed.get('params', {}), verify=False)
        if response.status_code == 200:
            if feed['type'] == 'json':
                data = json.loads(response.text)
                ip_addresses = [entry['ipAddress'] for entry in data['data']]
            else:
                content = response.text
                ip_addresses = content.splitlines()
            
            df = pd.DataFrame(ip_addresses, columns=['IP Address'])
            
            # Extrair endereços IP do dataframe
            for entry in df['IP Address']:
                match = re.search(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', entry)
                if match:
                    all_ips.append(match.group())
        else:
            print(f"Error fetching {feed['name']}: {response.status_code} - {response.text}")

    return all_ips

# Lista de feeds com suas respectivas URLs e tipos
feeds = [
    {'name': 'Cybercrime Tracking C2', 'url': 'https://raw.githubusercontent.com/firehol/blocklist-ipsets/refs/heads/master/cybercrime.ipset', 'type': 'text'},
    {'name': 'DM Tor', 'url': 'https://raw.githubusercontent.com/firehol/blocklist-ipsets/refs/heads/master/dm_tor.ipset', 'type': 'text'},
    {'name': 'Botvrij.eu', 'url': 'https://www.botvrij.eu/data/ioclist.ip-dst', 'type': 'text'},
    {'name': 'Binary Defense', 'url': 'https://www.binarydefense.com/banlist.txt', 'type': 'text'},
    {'name': 'Brute Force Blocker', 'url': 'https://danger.rulez.sk/projects/bruteforceblocker/blist.php', 'type': 'text'},
    {'name': 'Cinsscore', 'url': 'https://cinsscore.com/list/ci-badguys.txt', 'type': 'text'}
    {'name': 'GreenSnow', 'url': 'https://blocklist.greensnow.co/greensnow.txt', 'type': 'text'},
    {'name': 'OpenPhish', 'url': 'https://openphish.com/feed.txt', 'type': 'text'},
    {'name': 'Firehol Blocklist Net UA', 'url': 'https://raw.githubusercontent.com/firehol/blocklist-ipsets/refs/heads/master/blocklist_net_ua.ipset', 'type': 'text'},
    {'name': 'Firehol Abusers 1D', 'url': 'https://raw.githubusercontent.com/firehol/blocklist-ipsets/refs/heads/master/firehol_abusers_1d.netset', 'type': 'text'},
    {'name': 'BotScout', 'url': 'https://raw.githubusercontent.com/firehol/blocklist-ipsets/refs/heads/master/botscout.ipset', 'type': 'text'},
    {'name': 'BotScout 1D', 'url': 'https://raw.githubusercontent.com/firehol/blocklist-ipsets/refs/heads/master/botscout_1d.ipset', 'type': 'text'},
    {'name': 'IP Abuse DB', 'url': 'https://api.abuseipdb.com/api/v2/blacklist', 'type': 'json', 'params': {'confidenceMinimum': '75'}, 'headers': {'Accept': 'application/json', 'Key': 'TOKEN'}},
    {'name': 'Myip', 'url': 'https://raw.githubusercontent.com/firehol/blocklist-ipsets/refs/heads/master/myip.ipset', 'type': 'text'},
    {'name': 'ipsum', 'url': 'https://raw.githubusercontent.com/stamparm/ipsum/master/ipsum.txt', 'type': 'text'},
    {'name': 'Emerging Threats', 'url': 'https://rules.emergingthreats.net/blockrules/compromised-ips.txt', 'type': 'text'},
    {'name': 'Clean Talk', 'url': 'https://raw.githubusercontent.com/firehol/blocklist-ipsets/refs/heads/master/cleantalk.ipset', 'type': 'text'},
    {'name': 'Clean Talk Top20', 'url': 'https://raw.githubusercontent.com/firehol/blocklist-ipsets/refs/heads/master/cleantalk_top20.ipset', 'type': 'text'},
    {'name': 'Socks Proxy', 'url': 'https://raw.githubusercontent.com/firehol/blocklist-ipsets/refs/heads/master/socks_proxy.ipset', 'type': 'text'},
    {'name': 'BlackList de', 'url': 'https://raw.githubusercontent.com/firehol/blocklist-ipsets/refs/heads/master/blocklist_de_bots.ipset', 'type': 'text'},
    {'name': 'BlackList de StrongIP', 'url': 'https://raw.githubusercontent.com/firehol/blocklist-ipsets/refs/heads/master/blocklist_de_strongips.ipset', 'type': 'text'},
    {'name': 'BlackList de SSH', 'url': 'https://raw.githubusercontent.com/firehol/blocklist-ipsets/refs/heads/master/blocklist_de_ssh.ipset', 'type': 'text'},
    {'name': 'BlackList de FTP', 'url': 'https://raw.githubusercontent.com/firehol/blocklist-ipsets/refs/heads/master/blocklist_de_ftp.ipset', 'type': 'text'},
    {'name': 'Pushing Inertia BlackList', 'url': 'https://raw.githubusercontent.com/firehol/blocklist-ipsets/refs/heads/master/pushing_inertia_blocklist.netset', 'type': 'text'}
]

extracted_ips = fetch_ips_from_feeds(feeds)
unique_ips = list(set(extracted_ips))
total_ips_before = len(extracted_ips)
total_ips_after = len(unique_ips)

df_feed = pd.DataFrame(unique_ips, columns=['IP Address'])
pickle_total_ips_after = df_feed.to_pickle('feedIntelligence.pkl')


