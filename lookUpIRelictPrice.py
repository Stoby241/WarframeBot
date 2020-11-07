from dataclasses import dataclass
import pytesseract
import cv2

import warframeMarket
import utility

player = 4
boxesX = [
    730, 960,
    630, 840, 1080,
    500, 730, 960, 1190,
]
boxesY = 410
boxesW = 240
boxesH = 45

items, itemUrls = warframeMarket.getItemList()
items.append("Forma Blueprint")
itemUrls.append("not to sell")

pytesseract.pytesseract.tesseract_cmd = "H:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"

img = utility.loadImage("image3.png")
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
    bestItemUrl = ""
    bestAccuracy = 0

    for i in range(len(items)):
        item = items[i]
        itemUrl = itemUrls[i]

        itemNameParts = item.split(" ")

        accuracy = 0
        for itemNamePart in itemNameParts:
            if itemNamePart in data:
                accuracy += 1

        accuracy /= len(itemNameParts)

        if accuracy > bestAccuracy:
            bestItem = item
            bestItemUrl = itemUrl
            bestAccuracy = accuracy

    foundItems.append(bestItem + " " + str(warframeMarket.getItemPrice(bestItemUrl)) +"p")

for item in foundItems:
    print(item)
