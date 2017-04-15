import json

def macExists(mac):
	with open('clients.json' as client_list):

		for client in json.loads(client_list):
			if client['info']['mac'] == mac:
				return True
	return False
