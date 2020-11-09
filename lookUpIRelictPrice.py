import json
from dataclasses import dataclass
import pytesseract
import cv2
import numpy as np
import warframeMarket
import utility


def printItem(item):
    text = item[0].name + " " + str(warframeMarket.getItemPrice(item[0].url)) + "p"
    if not item[1]:
        text += " (probably wrong!)"
    print(text)


showImg = False
showParsedText = False
loadImg = False
imgName = "screenshot1"


@dataclass
class Item:
    name: str
    url: str


lower = [79, 121, 135]
upper = [102, 169, 190]
boxesX = [
    630, 840, 1080,
    500, 730, 960, 1190,
]
boxY = 400
boxW = 240
boxH = 75

f = open("jsonFiles/item.json", "r")
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

if loadImg:
    img = utility.loadImage("screenshot\\" + imgName + ".png")
else:
    img = utility.doScreenShot()

img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

lower = np.array(lower, dtype="uint8")
upper = np.array(upper, dtype="uint8")
mask = cv2.inRange(img, lower, upper)

datas = []

for boxX in boxesX:
    cimg = mask[boxY:boxY + boxH, boxX:boxX + boxW]
    datas.append(pytesseract.image_to_string(cimg))

    if showImg:
        cv2.imshow('image', cimg)
        cv2.waitKey(0)

if showParsedText:
    print(datas)

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


if len(foundItems) == 0:
    print("Nothing Found!")
else:
    print("\n--- 4 Player: ---")
    for item in foundItems[3:]:
        printItem(item)

    print("\n--- 3 Player: ---")
    for item in foundItems[:3]:
        printItem(item)

    print("\n--- 2 Player: ---")
    printItem(foundItems[4])
    printItem(foundItems[5])
