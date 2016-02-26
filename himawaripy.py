#!/usr/bin/env python3
from json import loads
from io import BytesIO
from urllib.request import urlopen
from time import strptime, strftime, gmtime
from os import system, makedirs
from os.path import expanduser
from PIL import Image
import subprocess
# Configuration
# =============

# Increases the quality and the size. Possible values: 4, 8, 16, 20
level = 2

# ==============================================================================

def main():
    width = 550
    height = 550
    save_dir = expanduser("~/himawaripy")

    print("Updating...")
    with urlopen("http://himawari8-dl.nict.go.jp/himawari8/img/D531106/latest.json") as latest_json:
        latest = strptime(loads(latest_json.read().decode("utf-8"))["date"], "%Y-%m-%d %H:%M:%S")
    print("Latest version: {} GMT\n".format(strftime("%Y/%m/%d/%H:%M:%S", latest)))

    url_format = "http://himawari8.nict.go.jp/img/D531106/{}d/{}/{}_{}_{}.png"

    png = Image.new('RGB', (width*level, height*level))

    print("Downloading tiles: 0/{} completed".format(level*level), end="\r")
    for x in range(level):
        for y in range(level):
            with urlopen(url_format.format(level, width, strftime("%Y/%m/%d/%H%M%S", latest), x, y)) as tile_w:
                tiledata = tile_w.read()

            tile = Image.open(BytesIO(tiledata))
            png.paste(tile, (width*x, height*y, width*(x+1), height*(y+1)))

            print("Downloading tiles: {}/{} completed".format(x*level + y + 1, level*level), end="\r")
    print("\nDownloaded\n")

    command = "mv himawari-latest.png " + save_dir + "/archive/" + str(strftime("%Y-%m-%d-%H:%M:%S", gmtime())) + ".png"
    print (command)
    status, output = subprocess.getstatusoutput(command)

    makedirs( save_dir, exist_ok=True )
    png.save( save_dir + "/himawari-latest.png", "PNG")

    # Because of a bug and stupid design of gsettings, see http://askubuntu.com/a/418521/388226
    #system("gsettings set org.gnome.desktop.background draw-background false \
    #        && gsettings set org.gnome.desktop.background picture-uri file://"
    #        + expanduser("~/.himawari-latest.png") +
    #        " && gsettings set org.gnome.desktop.background picture-options scaled")

    print("Done!\n")



    command = 'gsettings set org.gnome.desktop.background picture-uri "file://'+ save_dir +'/himawari-latest.png"'
    status, output = subprocess.getstatusoutput(command)

if __name__ == "__main__":
    main()
