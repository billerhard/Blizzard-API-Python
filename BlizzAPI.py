# This program gets a response from the Blizzard API
# CNA 336, 5/17/2018
# Bill Erhard wherhard@student.rtc.edu

# This program uses requests (HTTP for humans) package.
# Make sure to install the package before using it.

import requests
from tkinter import *
from PIL import Image, ImageTk
from io import BytesIO


# Gets your blizzard API key, hope you put it at '../api_key.txt' also, the
# api key should be the only line in it.
def get_api_key_from_file():

    # Open file with key in it, then return the key.
    with open('../api_key.txt', "r") as f:
        return f.read()


# This is where you input the stuff you need for the request - region, realm,
#  character, request type, etc.
# Right now it just finds one particular character.
def build_request():

    # These are the parts needed for a request... of a particular type.
    region = "us"
    realm = "moon-guard"
    character = "Nettleberry"
    rtype = "character"

 #   realm = input("Realm: ")
 #   character = input("Character: ")

    # build the request
    return "https://" + region + ".api.battle.net/wow/" + rtype + "/" + realm \
           + "/" + character + "?"


# We need the params to feed requests.get. Everything after the '?' in the
# url goes here.
def get_params():

    # Another param will be fields[] which lets you get various character data
    fields = []
    # At this point we just need the API key and locale
    locale = "en_US"
    return {'apikey': get_api_key_from_file(), 'locale': locale,
            'fields': fields}


# This is where the fun happens.
def main():
    r = build_request()
    p = get_params()
    rget = requests.get

    response = rget(r, params=p)

    # Hey look, requests does json!
    print(response.json())

    # We can even get specific things from it!
    level = response.json()['level']
    name = response.json()['name']
    print(str(name) + ", level: " + str(level))

    thumbnail_url = "http://render-us.worldofwarcraft.com/character/" + \
                    str(response.json()['thumbnail'])

    print(thumbnail_url)
    avatar = requests.get(thumbnail_url)
    root = Tk()
    root.title("Blizz API")

    img = ImageTk.PhotoImage(Image.open(BytesIO(avatar.content)))

    label = Label(root, image=img)
    label.pack()

    root.mainloop()


# Just in case you use this somewhere else?
if __name__ == "__main__":
    main()
