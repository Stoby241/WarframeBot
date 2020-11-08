import json
from dataclasses import dataclass
import pytesseract

import utility


@dataclass
class Item:
    name: str
    url: str

f = open("item.json", "r")
jsonItemList = json.loads(f.read())
f.close()

items = []
for jsonItem in jsonItemList:
    isMod = False
    for tag in jsonItem["tags"]:
        if tag == "mod":
            isMod = True
    if isMod:
        item = Item(
            name=jsonItem["name"],
            url=jsonItem["url"]
        )
        items.append(item)

picNumber = 9

pytesseract.pytesseract.tesseract_cmd = "H:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"

datas = []
for i in range(9):
    print("\rComputing img "+ str(i))
    img = utility.loadImage("screenshot\\mod"+ str(i) +".png")
    datas.append(pytesseract.image_to_string(img))

foundMods = []
i = 0
for data in datas:
    print("\rSearching Mods in data " + str(i))
    for item in items:
        parts = item.name.split(" ")
        for part in parts:
            if part in data:
                foundMods.append(item)
    i += 1

jsonString = json.dumps([ob.__dict__ for ob in foundMods], indent=2)

f = open("modList.json", "w")
f.truncate(0)
f.write(jsonString)
f.close()