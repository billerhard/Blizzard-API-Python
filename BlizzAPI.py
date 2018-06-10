# This program gets a response from the Blizzard API
# CNA 336, 5/17/2018
# Bill Erhard wherhard@student.rtc.edu

# This program uses a bunch of packages, make sure they're installed
# before using them.
import json
import requests
from io import BytesIO
from pathlib import Path
from tkinter import *
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
    request_type = "character"

    # build the request
    return "https://" + region + ".api.battle.net/wow/" + request_type \
           + "/" + realm + "/" + character + "?"


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

    mount_url = "http://media.blizzard.com/wow/icons/36/"
    mount_list_url = "https://us.api.battle.net/wow/mount/?locale=en_US"
    images = []
    labels = []
    path_to_mount_list = Path('../mounts.json')
    path_to_images = Path('../imgs/')

    if path_to_mount_list.exists():
        with open(path_to_mount_list, "r") as f:
            data = json.loads(f.read())
    else:
        with open(path_to_mount_list, "w") as f:
            data = requests.get(mount_list_url, params={
                'apikey': get_api_key_from_file()}).json()
            json.dump(data, f)

    if not path_to_images.exists():
        path_to_images.mkdir()

    for mount in data['mounts']:
        path_to_each_image = Path('../imgs/' + str(mount['creatureId'])
                                  + '.jpg')
        if path_to_each_image.exists():
            try:
                with Image.open(path_to_each_image, "r") as f:
                    images.append(ImageTk.PhotoImage(f))
            except OSError:
                path_to_each_image.unlink()
                continue
        else:
            with open(path_to_each_image, "wb") as f:
                response = requests.get(mount_url + mount['icon'] + '.jpg')

                if response.status_code == 404:  # No mount image found
                    continue  # So skip it.
                else:
                    images.append(ImageTk.PhotoImage(Image.open(
                        BytesIO(response.content))))
                    f.write(response.content)

    for i in range(len(images)):
        labels.append(Label(root, image=images[i]).grid(row=i // 40,
                                                        column=i % 40))
        try:
            labels[i].pack(anchor=NW)
        except AttributeError:
            continue

    root.mainloop()


# Just in case you use this somewhere else?
if __name__ == "__main__":
    main()
