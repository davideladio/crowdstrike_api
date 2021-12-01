# I'm given a hostname but I need its hostId. Well, this funcion will do
# exactly that. Although is more intended to be used within a loop
# to help you het hundreds or thousand of hostids from their hostnames
#
# i'm using logging levels in my code so thats why you'll see those lines
# commented. You can implement code on your own way including logging
# obvoously
#
# This funcion will require a previously retrieven token (get_token.py)
# and the hostname you want to adquire its hostid

import requests
import json
import logging

def get_hostid(token, hostname):
    url="https://api.crowdstrike.com/devices/queries/devices/v1?filter=hostname%3A"
    url=url+"'"+hostname+"'"
    bearer_token="Bearer "+str(token)
    payload = {'accept': 'application/json', 'authorization': bearer_token}
    
    data_hostname = requests.get(url, headers=payload)
    
    if data_hostname.status_code==200:
        # get the hostid from the json
        hostid=str(data_hostname.json()['resources'])
        # I clear here the brackets and quotes from the result
        hostid=hostid[2:len(hostid)-2]
        # log a success message
        logging.info("get_hostid SUCCESS %s --> %s", hostname, hostid)
        # return the value
        return hostid
    else:
        # Log an error message
        logging.warning("get_hostid ERROR %s", hostname)
        # return 0 as an 'error flag'
        return 0     