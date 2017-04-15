import time

import requests
import json

timespan = 300
headers = {
    'X-Cisco-Meraki-API-Key': 'bf2bd5915762b1f96f579788c77d6d7fc038678f',
    'Content-Type': 'application/json'
}

client_list = []

org_url = 'https://dashboard.meraki.com/api/v0/organizations'
orgs = requests.get(org_url, headers=headers).json()

for org in orgs:
    net_url = 'https://dashboard.meraki.com/api/v0/organizations/' + str(org['id']) + '/networks'
    networks = requests.get(net_url, headers=headers).json()

    for network in networks:
        device_url = 'https://dashboard.meraki.com/api/v0/networks/' + network['id'] + '/devices'
        devices = requests.get(device_url, headers=headers).json()

        for device in devices:
            client_url = 'https://dashboard.meraki.com/api/v0/devices/' + device['serial'] + '/clients?timespan=' + str(timespan)
            clients = requests.get(client_url, headers=headers).json()

            for client in clients:
                client_list.append({
                    'info': client,
                    'org': org,
                    'network': network,
                    'device': device,
                })

with open('clients.json', 'w') as outfile:
    outfile.write(json.dumps(client_list, indent=4))
