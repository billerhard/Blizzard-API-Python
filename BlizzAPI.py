# Python wrapper for WoW BFA Web API
# 8/29/2018
# Bill Erhard wherhard@student.rtc.edu
import requests


# Assumes that the key is plaintext
# Returns the API key stored in the file found at relative path ./api_key.txt
def get_api_key_from_file():
    with open('./api_key.txt', "r") as f:
        return f.read()


# Returns a uri for a given achievement from the WoW Web API
def build_achievement_request(args):
    uri = "https://"
    region = args["region"]
    achievement_id = str(args["id"])
    locale = args["locale"]
    apikey = args["apikey"]

    uri += region + ".api.battle.net/wow/achievement/"
    uri += achievement_id + "?locale=" + locale + "&apikey=" + apikey
    return uri


# Returns a uri for a given realm's auction house data from the WoW Web API
def build_auction_request(request_args):
    uri = "https://"
    region = request_args["region"]
    realm = request_args["realm"]
    locale = request_args["locale"]
    apikey = request_args["apikey"]

    uri += region + ".api.battle.net/wow/auction/data/" + realm + "?locale="
    uri += locale + "&apikey=" + apikey
    return uri


def main():
    request_args = {
        "region": "us",
        "id": "2144",
        "locale": "en_US",
        "apikey": get_api_key_from_file(),
        "realm": "moon-guard"
        }

    uri = build_achievement_request(request_args)
    response = requests.get(uri)
    print(response.json())

    uri = build_auction_request(request_args)
    response = requests.get(uri)
    print(response.json())


if __name__ == '__main__':
    main()
