# Code to add a Falcon console tag to a hostid
# example tag: FalconGroupingTags/tag1
# action = add to add a tag

import requests
import json
import logging

def tag_hostid(hostid, action, tag, token):
    # url 
    url="https://api.crowdstrike.com/devices/entities/devices/tags/v1"
    
    # headers
    headers = {
        'accept': 'application/json',
        'authorization': f'Bearer {token}',
        'Content-Type': 'application/json'

    }
    
    # data for the PATCH API CALL. These fields are indicated as a -d
    # in the CURL if you read the swagger documentation
    # tag format shall be like "FalconGroupingTags/YOUR_TAG_HERE"
    
    payload = json.dumps({
        "action": action,
        "device_ids": [
            hostid
            ],
        "tags": [
            tag
            ]
        })

    # API CALL
    r = requests.patch(url, data=payload, headers=headers)
    response = r.json()['resources']
    # Error control
    if response is not None:
        if response[0]['code'] == 200:
            # log success message
            logging.info("tag_hostid SUCCESS - HostID %s with Tag %s", hostid, tag)
            # # return and exit
            return response
        else:
            # log an error message
            logging.error("tag_hostid ERROR - HostID %s with Tag %s", hostid, tag)
            #return and exit
            return response
    else:
        logging.warning('tag_hostid-ERROR-Hostname-NULL-Hostid-%s', hostid)
