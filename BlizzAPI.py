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

    # response = requests.get(build_request(), params=get_params())

    # Hey look, requests does json!
    # print(response.json())

    # We can even get specific things from it!
    #  level = response.json()['level']
    #  name = response.json()['name']
    #  print(str(name) + ", level: " + str(level))

    #  thumbnail_url = "http://render-us.worldofwarcraft.com/character/" + \
    #                 str(response.json()['thumbnail'])
    # profile_url = thumbnail_url[:-10] + 'profilemain.jpg'
    #  inset_url = thumbnail_url[:-10] + 'inset.jpg'
    mounturl = "http://media.blizzard.com/wow/icons/36/"
    mountlisturl = "https://us.api.battle.net/wow/mount/?locale=en_US"
#    mounts = requests.get(mountlisturl,
#                          params={'apikey': get_api_key_from_file()})
#    data = mounts.json()

    data = ""

    try:
        with open('../mounts.json', "r") as f:
            data = json.loads(f.read())
    except FileNotFoundError:
        with open('../mounts.json', "w") as f:
            data = requests.get(mountlisturl, params={'apikey': get_api_key_from_file()}).json()
            json.dump(data, f)

    image_bytes = []

    p = Path('../imgs/')

    if not p.exists():
        p.mkdir(parents=True, exist_ok=True)

    for mount in data['mounts']:

        try:
            with open('../imgs/' + str(mount['creatureId']) + '.jpg', "rb") as f:
                image_bytes.append(f.read())
        except FileNotFoundError:
            with open('../imgs/' + str(mount['creatureId']) + '.jpg', "wb") as f:
                response = requests.get(mounturl + mount['icon'] + '.jpg')
                image_bytes.append(response.content)
                f.write(response.content)

    imgs = []

    for i in image_bytes:

        imgs.append(ImageTk.PhotoImage(Image.open(BytesIO(i))))
'''

    imgs = []
    labels = []

    for r in responses:
        try:
            imgs.append(ImageTk.PhotoImage(Image.open(BytesIO(r.content))))
        except OSError:
            continue

    for i in range(25):
        for j in range(47):
            try:
                labels.append(Label(root, image=imgs[i*25+j]).grid(row=i, column=j))
                labels[i*25+j].pack(anchor=NW)
            except AttributeError:
                continue
            except IndexError:
                pass
    root.mainloop()
'''

'''
    label = []
    for i in range(10):
        new_url = mounturl + data['mounts'][i]['icon'] + '.jpg'
        r = requests.get(new_url)
        img = ImageTk.PhotoImage(Image.open(BytesIO(r.content)))
        label.append(Label(root, image=img))
    root.mainloop()
'''

'''
    for x in data['mounts']:
        label = []
        try:
            new_url = mounturl + x['icon'] + '.jpg'
            r = requests.get(new_url)
            img = ImageTk.PhotoImage(Image.open(BytesIO(r.content)))
            label.append(Label(root, image=img))
            label.pop().pack()
        except OSError:
            print(new_url)
            continue
'''

#   https://us.api.battle.net/wow/mount/ to get
# mount list (takes locale and api key as params)
#  avatar = requests.get(thumbnail_url)
#  profile = requests.get(profile_url)
#  inset = requests.get(inset_url)
#  maini = requests.get((thumbnail_url[:-10] + 'main.jpg'))
#  mount = requests.get()

#   img = ImageTk.PhotoImage(Image.open(BytesIO(avatar.content)))
#  pimg = ImageTk.PhotoImage(Image.open(BytesIO(profile.content)))
#   iimg = ImageTk.PhotoImage(Image.open(BytesIO(inset.content)))
#   mimg = ImageTk.PhotoImage(Image.open(BytesIO(maini.content)))
# mountimg =

#   label2 = Label(root, image=mimg)
#  label2.pack()

'''
    label = Label(root, image=img)
    label.pack()
    label1 = Label(root, image=pimg)
    label1.pack()
'''

# Just in case you use this somewhere else?
if __name__ == "__main__":
    main()
