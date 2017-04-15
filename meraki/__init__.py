import json

def mac_exists(mac):
    with open('clients.json') as client_list:
        for client in json.load(client_list):
            if client['info']['mac'] == mac:
                return True
    return False
