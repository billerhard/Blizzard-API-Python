# This program gets a response from the Blizzard API
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
rtype = "character"

# build the request
request_url = "https://" + region + ".api.battle.net/wow/" + rtype + "/" \
              + realm + "/" + character + "?"

# Let's do the params
get_param = {'apikey': key, 'locale': locale}

# GET character profile from API
response = requests.get(request_url, params=get_param)
'''
print("Here is the server response: ")
print(response.status_code)
print("Content: ")
print(response.content)
'''
'''def main():
  print("Hello World!")
  
if __name__== "__main__":
  main()'''

print(response.json())
level = response.json()['level']
print(str(level))
