import json
import time
from dataclasses import dataclass

import requests

import warframeMarket

root = "https://api.warframe.market/v1"


@dataclass
class Item:
    name: str
    url: str
    tags: []
    id: str
    drop: []


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

i = 0
for item in items:
    response = requests.get(warframeMarket.root + "/items/" + item.url)
    print("Item " + str(i) + " of " + str(len(items)) + " Status Code: " + str(response.status_code))

    itemJson = response.json()["payload"]["item"]
    #print(json.dumps(itemJson, indent=4, sort_keys=True))

    item.id = itemJson["id"]
    item.tags = itemJson["items_in_set"][0]["tags"]
    item.drop = itemJson["items_in_set"][0]["en"]["drop"]

    i += 1
    time.sleep(0.5)

items.append(Item(
    name="Forma Blueprint",
    url="",
    id="",
    tags=[],
    drop=[]
))

f = open("item.txt", "w")
jsonString = json.dumps([ob.__dict__ for ob in items])
f.write(jsonString)
f.close()
