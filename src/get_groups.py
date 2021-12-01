# with a valid token this API CALL will get a json with all the defined
# groups in your console

import requests
import json

def get_groups(token):
	bearer_token="bearer "+str(token)
	payload = {'accept': 'application/json', 'authorization': bearer_token}
	groups = requests.get('https://api.crowdstrike.com/devices/combined/host-groups/v1?sort=name.asc', headers=payload)
	return groups.json()