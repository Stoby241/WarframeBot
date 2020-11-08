import json
from dataclasses import dataclass
import time

import warframeMarket


@dataclass
class Item:
    name: str
    url: str

@dataclass
class Set:
    name: str
    url: str
    itemNames: []
    itemUrls: []


f = open("item.json", "r")
jsonItemList = json.loads(f.read())
f.close()

items = []
sets = []
for jsonItem in jsonItemList:
    name = jsonItem["name"]
    parts = name.split(" ")
    if "Set" == parts[len(parts) -1]:
        set = Set(
            name=name,
            url=jsonItem["url"],
            itemNames=[],
            itemUrls=[]
        )
        sets.append(set)
    else:
        item = Item(
            name=name,
            url=jsonItem["url"]
        )
        items.append(item)


for set in sets:
    print(" --- " + set.name + " --- ")
    parts = set.name.split(" ")
    for item in items:
        parts1 = item.name.split(" ")

        isInSet = False
        if len(parts) <= len(parts1):
            isInSet = True
            for i in range(len(parts) - 1):
                if parts[i] != parts1[i]:
                    isInSet = False
                    break

        if isInSet:
            set.itemNames.append(item.name)
            set.itemUrls.append(item.url)
            print(item.name)


jsonString = json.dumps([ob.__dict__ for ob in sets], indent=2)

f = open("setList.json", "w")
f.truncate(0)
f.write(jsonString)
f.close()