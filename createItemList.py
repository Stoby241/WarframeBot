import json
import time
from dataclasses import dataclass

import requests

import utility
import warframeMarket

root = "https://api.warframe.market/v1"


@dataclass
class Item:
    name: str
    url: str
    tags: []
    id: str
    drop: []

apiPingSpeed = 0.5

response = requests.get(root + "/items")
if response.status_code != 200:
    print("Status Code: " + str(response.status_code))
    print(json.dumps(response.json(), indent=4, sort_keys=True))

itemListJson = response.json()["payload"]["items"]

items = []
for itemJson in itemListJson:
    item = Item(
        name=itemJson["item_name"],
        url=itemJson["url_name"],
        id="",
        tags=[],
        drop=[]
    )
    items.append(item)

itemsLength = len(items)
i = 0
for item in items:
    response = requests.get(warframeMarket.root + "/items/" + item.url)

    timeLeft = utility.computeSecondsToHigherUnits((itemsLength - i) * apiPingSpeed, "year")
    print("\rItem " + str(i) + " of " + str(itemsLength) +
          " || Status Code: " + str(response.status_code) +
          " || Time left: " + str(timeLeft), end="")

    itemJson = response.json()["payload"]["item"]
    #print(json.dumps(itemJson, indent=4, sort_keys=True))

    item.id = itemJson["id"]
    item.tags = itemJson["items_in_set"][0]["tags"]

    item.drop = []
    drops = itemJson["items_in_set"][0]["en"]["drop"]
    for drop in drops:
        item.drop.append(drop["name"])


    i += 1
    time.sleep(apiPingSpeed)

items.append(Item(
    name="Forma Blueprint",
    url="",
    id="",
    tags=[],
    drop=["Lith","Meso","Neo","Axi"]
))

jsonString = json.dumps([ob.__dict__ for ob in items], indent=2)

f = open("item.json", "w")
f.truncate(0)
f.write(jsonString)
f.close()
