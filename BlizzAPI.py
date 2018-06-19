# This program gets a response from the Blizzard API
# CNA 336, 5/17/2018
# Bill Erhard wherhard@student.rtc.edu

# This program uses a bunch of packages, make sure they're installed
# before using them.
import json
from pathlib import Path
from threading import Thread
from tkinter import *

import requests
from PIL import Image, ImageTk


# Gets your blizzard API key, hope you put it at '../api_key.txt'. Also, the
# api key should be the only line in it.
def get_api_key_from_file():
    # Open file with key in it, then return the key.
    with open('../api_key.txt', "r") as f:
        return f.read()


# Gives us the response to a request for a 36x36 pixel jpg.
# needs icon number
def get_mount_image(icon):
    mount_url = "http://media.blizzard.com/wow/icons/36/"
    return requests.get(mount_url + icon + '.jpg')


# checks for dumb mounts without icons
def check_for_baddies(creature_id):
    bad = Path('./badimgs.txt')
    bad_list = populate_bad_list(bad)

    for x in bad_list:
        y = int(x)
        if creature_id == y:
            return True
    return False


# requests the world of warcraft mount list
def get_mount_list():
    mount_list_url = "https://us.api.battle.net/wow/mount/?locale=en_US"
    path_to_mount_list = Path('../mounts.json')

    if path_to_mount_list.exists():
        with open(path_to_mount_list, "r") as f:
            data = json.loads(f.read())
    else:
        with open(path_to_mount_list, "w") as f:
            data = requests.get(mount_list_url, params={
                'apikey': get_api_key_from_file()}).json()
            f.write(json.dumps(data))
    return data


# adds baddies to the bad list using baddies found in a file at bad path
def populate_bad_list(bad_path):
    bad_list = []

    if bad_path.exists():
        with open(bad_path, "r") as f:
            for baddie in f:
                bad_list.append(baddie)

    return bad_list


# get images if we don't already have them.
def get_image_response(mount, path_to_image):
    bad = Path('./badimgs.txt')
    response = get_mount_image(mount['icon'])

    if response.status_code == 404:
        with open(bad, "a") as f:
            f.write(str(mount['creatureId']) + "\n")
    else:
        with open(path_to_image, "wb") as f:
            content = response.content
            f.write(content)


# get images from the file if we already have them.
def get_image_from_file(images, path_to_image):
    with Image.open(path_to_image, "r") as f:
        images.append(ImageTk.PhotoImage(f))


# this is where the fun happens!
def main():

    def myfunction(event):
        canvas.configure(scrollregion=canvas.bbox("all"), width=1100,
                         height=800)

    def _on_mousewheel(self, event):
        self.top.yview_scroll(-1 * (event.delta / 120), "units")

    root = Tk()
    root.title("Blizzard API")

    top = Frame(root)
    top.pack()

    canvas = Canvas(top)
    scrollbar = Scrollbar(top, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    frame = Frame(canvas)

    top.bind("<MouseWheel>", _on_mousewheel)

    canvas.pack(side="left")
    scrollbar.pack(side="right", fill="y")
    canvas.create_window((0, 0), window=frame, anchor='nw')
    frame.bind("<Configure>", myfunction)

    images = []
    names = []

    path_to_images = Path('../imgs/')
    data = get_mount_list()

    threads = []
    for mount in data['mounts']:
        jpeg = str(mount['creatureId']) + '.jpg'
        path_to_image = path_to_images.joinpath(jpeg)

        if check_for_baddies(mount['creatureId']):
            continue
        if not path_to_images.exists():
            path_to_images.mkdir()
        if not path_to_image.exists():
            t = Thread(target=get_image_response, args=(mount, path_to_image))
            threads.append(t)
            t.start()
    for t in threads:
        t.join()
    for mount in data['mounts']:
        if check_for_baddies(mount['creatureId']):
            continue
        jpeg = str(mount['creatureId']) + '.jpg'
        path_to_image = path_to_images.joinpath(jpeg)
        get_image_from_file(images, path_to_image)
        names.append(mount['name'])

    count = 0
    for i in range(len(images)):
        count += 1
        irow = i // 5 * 2
        icol = i % 5
        if irow <= 0:
            irow = 0
        Label(frame, image=images[i]).grid(row=irow, column=icol)
        Label(frame, text=names[i]).grid(row=(irow+1), column=icol)

    num_mounts = '# mounts: ' + str(count)
    Label(frame, text=num_mounts).grid(columnspan=8)

    root.mainloop()


# Just in case you use this somewhere else?
if __name__ == "__main__":
    main()
