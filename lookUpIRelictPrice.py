import json
from dataclasses import dataclass
import pytesseract
import cv2

import warframeMarket
import utility

player = 3
boxesX = [
    730, 960,
    630, 840, 1080,
    500, 730, 960, 1190,
]
boxesY = 410
boxesW = 240
boxesH = 45


@dataclass
class Item:
    name: str
    url: str


f = open("item.json", "r")
jsonItemList = json.loads(f.read())
f.close()

items = []
for jsonItem in jsonItemList:
    item = Item(
        name=jsonItem["name"],
        url=jsonItem["url"]
    )
    if ("Chassis" in item.name) | ("Neuroptics" in item.name) | ("Systems" in item.name):
        item.name += " Blueprint"
    items.append(item)

pytesseract.pytesseract.tesseract_cmd = "H:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"

img = utility.loadImage("screenshot\\image4.png")
#img = utility.doScreenShot()


img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

datas = []

offset = 0
if player == 3:
    offset += 2
elif player == 4:
    offset += 5

for i in range(player):
    cimg = img[boxesY:boxesY + boxesH, boxesX[i + offset]:boxesX[i + offset] + boxesW]
    datas.append(pytesseract.image_to_string(cimg))

foundItems = []
for data in datas:
    bestItem = ""
    bestAccuracy = 0
    sure = False

    for item in items:
        itemNameParts = item.name.split(" ")

        accuracy = 0
        for itemNamePart in itemNameParts:
            if itemNamePart in data:
                accuracy += 1

        if accuracy > bestAccuracy:
            sure = accuracy >= len(itemNameParts)
            bestItem = item
            bestAccuracy = accuracy

    if bestItem != "":
        foundItems.append([bestItem, sure])

if len(foundItems) == player:
    for item in foundItems:
        text = item[0].name + " " + str(warframeMarket.getItemPrice(item[0].url)) + "p"
        if not item[1]:
            text += " (probably wrong!)"
        print(text)
else:
    print("Wrong Player Count")
