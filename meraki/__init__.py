def macExists(mac):
	with open('clients.json' as client_list):
		for client in client_list:
			if client['info']['mac'] == mac:
				return True
	return False
