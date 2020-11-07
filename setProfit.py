import json
from dataclasses import dataclass
import time

import warframeMarket


@dataclass
class Item:
    name: str
    url: str
    price: int

@dataclass
class Set:
    name: str
    url: str
    priceSet: int
    priceSum: int
    profit: int
    items: []


apiPingSpeed = 0.4

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
            items=[],
            priceSet=0,
            priceSum=0,
            profit=0
        )
        sets.append(set)
    else:
        item = Item(
            name=name,
            url=jsonItem["url"],
            price=0
        )
        items.append(item)

i = 0
for set in sets:
    set.priceSet = warframeMarket.getItemPrice(set.url)
    time.sleep(apiPingSpeed)

    parts = set.name.split(" ")
    set.priceSum = 0
    for item in items:
        parts1 = item.name.split(" ")

        if parts[0] == parts1[0]:
            set.items.append(item)

            if item.price == 0:
                item.price = warframeMarket.getItemPrice(item.url)
                time.sleep(apiPingSpeed)

            set.priceSum += item.price
            set.profit = set.priceSet - set.priceSum

    print(set.name +
          " || Set price: "+ str(set.priceSet) +
          " || Parts sum: "+ str(set.priceSum) +
          " || Profit: "+ str(set.profit))
    i += 1

sets.sort(key=lambda x: x.profit, reverse=True)

print("------------- Sorted List -------------")
f = open("item.json", "w")
f.truncate(0)


for set in sets:
    text = set.name +\
          " || Set price: " + str(set.priceSet) +\
          " || Parts sum: " + str(set.priceSum) +\
          " || Profit: " + str(set.profit)

    f.write(text + "\n")
    print(text)

f.close()