# This program takes stuff from the BlizzAPI and does stuff.
# CNA 336, 5/17/2018
# Bill Erhard wherhard@student.rtc.edu

# This program uses requests (HTTP for humans) package.
# Make sure to install the package before using it.
import requests

# Open file with key in it
with open('../api_key.txt', "r") as f:
    key = f.read()

# I can get my character, or I can refactor later to get input from user
region = "us"
realm = "moon-guard"
character = "Nettleberry"
locale = "en_US"

# build the request
request_uri = "https://" + region + ".api.battle.net/wow/character/" + realm + "/" + character + "?locale=" + locale

# I don't know why, but request only seems to work using params, not adding key to request uri
get_param = {'apikey': key}

# GET character profile from API
response = requests.get(request_uri, params=get_param)

print("Here is the server response: ")
print(response.status_code)
print("Content: ")
print(response.content)
