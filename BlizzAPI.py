# This program gets a response from the Blizzard API
# CNA 336, 5/17/2018
# Bill Erhard wherhard@student.rtc.edu

# This program uses requests (HTTP for humans) package.
# Make sure to install the package before using it.
import requests


# Gets your blizzard API key, hope you put it at '../api_key.txt' also, the api key should be the only line in it.
def get_api_key_from_file():

    # Open file with key in it, then return the key.
    with open('../api_key.txt', "r") as f:
        return f.read()


# This is where you input the stuff you need for the request - region, realm, character, request type, etc.
# Right now it just finds one particular character.
def build_request():

    # These are the parts needed for a request... of a particular type.
    region = "us"
    realm = "moon-guard"
    character = "Nettleberry"
    rtype = "character"

    # build the request
    return "https://" + region + ".api.battle.net/wow/" + rtype + "/" + realm + "/" + character + "?"


# We need the params to feed requests.get. Everything after the '?' in the url goes here.
def get_params():

    # At this point we just need the API key and locale
    locale = "en_US"
    return {'apikey': get_api_key_from_file(), 'locale': locale}


# This is where the fun happens.
def main():

    # GET character profile from API
    response = requests.get(build_request(), params=get_params())

    # Hey look, requests does json!
    print(response.json())

    # We can even get specific things from it!
    level = response.json()['level']
    print(str(level))


# Just in case you use this somewhere else?
if __name__ == "__main__":
    main()
