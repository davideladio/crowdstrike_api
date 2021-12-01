# you'll need an access token every time you request something from the API
# this token lasts 30' and then you need to request a new one.
#
# In order to get a token you'll need a client ID and a CLient Secret. The idea
# is to have a .env file in the 'files' folder containing this data with the following
# format:
#
# CLIENT_ID="your client_id"
# SECRET_KEY="Your client_secret"
# please remember to include this file in a .gitignore file so github ignores it and
# you don't end up sharing that information with eberyone.
#
# once you have that file you can access it from your python code this way:
# from decouple import config
# clientid=config('CLIENT_ID')
# clientsecret=config('SECRET_KEY')
#
# and now you can write your function like this:

import requests
import json
from decouple import config

clientid=config('CLIENT_ID')
clientsecret=config('SECRET_KEY')

def get_token():
    payload = {'client_id': clientid, 'client_secret': clientsecret}
    r = requests.post('https://api.crowdstrike.com/oauth2/token', data=payload)
    return r.json()['access_token']

# you would use it somehow like:

token = get_token()

# and then use that token in other API Calls