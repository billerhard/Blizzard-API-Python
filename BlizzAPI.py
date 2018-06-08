# This program gets a response from the Blizzard API
# CNA 336, 5/17/2018
# Bill Erhard wherhard@student.rtc.edu

# This program uses requests (HTTP for humans) package.
# Make sure to install the package before using it.

from io import BytesIO
from tkinter import *
import json
from pathlib import Path

import requests
from PIL import Image, ImageTk


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
    character = "nettleberry"
    rtype = "character"

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
    root = Tk()
    root.title("Blizz API")

    mounturl = "http://media.blizzard.com/wow/icons/36/"
    mountlisturl = "https://us.api.battle.net/wow/mount/?locale=en_US"
    data = ""
    imgs = []

    p = Path('../mounts.json')

    if p.exists():
        with open(p, "r") as f:
            data = json.loads(f.read())
    else:
        with open(p, "w") as f:
            data = requests.get(mountlisturl, params={'apikey': get_api_key_from_file()}).json()
            json.dump(data, f)

    p = Path('../imgs/')

    if not p.exists():
        p.mkdir(parents=True, exist_ok=True)

    for mount in data['mounts']:
        p = Path('../imgs/' + str(mount['creatureId']) + '.jpg')
        if p.exists():
            try:
                with Image.open(p, "r") as f:
                    imgs.append(ImageTk.PhotoImage(f))
            except OSError:
                p.unlink()
                continue
        else:
            with open(p, "wb") as f:
                response = requests.get(mounturl + mount['icon'] + '.jpg')

                if response.status_code == 404:  # No mount image found
                    continue  # So skip it.
                else:
                    imgs.append(ImageTk.PhotoImage(Image.open(BytesIO(response.content))))
                    f.write(response.content)

    labels = []

    for i in range(len(imgs)):
        labels.append(Label(root, image=imgs[i]).grid(row=i // 40, column=i % 40))
        try:
            labels[i].pack(anchor=NW)
        except AttributeError:
            continue

    root.mainloop()


# Just in case you use this somewhere else?
if __name__ == "__main__":
    main()
