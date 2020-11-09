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

f = open("jsonFiles/setList.json", "r")
jsonItemList = json.loads(f.read())
f.close()

sets = []
for jsonSet in jsonItemList:
    set = Set(
        name=jsonSet["name"],
        url=jsonSet["url"],
        items=[],
        priceSet=0,
        priceSum=0,
        profit=0
    )
    for i in range(len(jsonSet["itemNames"])):
        item = Item(
            name=jsonSet["itemNames"][i],
            url=jsonSet["itemUrls"][i],
            price=0
        )
        set.items.append(item)
    sets.append(set)

for set in sets:
    set.priceSet = warframeMarket.getItemPrice(set.url)
    time.sleep(apiPingSpeed)

    for item in set.items:
        item.price = warframeMarket.getItemPrice(item.url)
        time.sleep(apiPingSpeed)

        set.priceSum += item.price

    set.profit = set.priceSet - set.priceSum

    print(set.name +
          " || Set price: "+ str(set.priceSet) +
          " || Parts sum: "+ str(set.priceSum) +
          " || Profit: "+ str(set.profit))


sets.sort(key=lambda x: x.profit, reverse=True)

print("------------- Sorted List -------------")
f = open("outputFiles/profit.txt", "w")
f.truncate(0)


for set in sets:
    text = set.name +\
          " || Set price: " + str(set.priceSet) +\
          " || Parts sum: " + str(set.priceSum) +\
          " || Profit: " + str(set.profit)

    f.write(text + "\n")
    print(text)

f.close()