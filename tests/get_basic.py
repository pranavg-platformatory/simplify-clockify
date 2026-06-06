import requests

#############################################################
# CONFIG
#############################################################

api_key_name = 'enter-your-api-key-name-here'
api_key_value = 'enter-your-api-key-value-here'
api_endpoint = 'https://api.clockify.me/api/v1/'

#############################################################
# MAKE REQUESTS
#############################################################

response = requests.get(api_endpoint + 'user', headers={'x-api-key': api_key_value})
print(response.json())
