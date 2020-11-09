import json

import requests

root = "https://api.warframe.market/v1"

def getItemPrice(itemUrl):
    if itemUrl == "":
        return 0.0

    response = requests.get(root + "/items/" + itemUrl + "/orders")
    if response.status_code != 200:
        print("Status Code: " + str(response.status_code))
        print(json.dumps(response.json(), indent=4, sort_keys=True))

    orderListJson = response.json()["payload"]["orders"]
    price = 100000000000
    for orderJson in orderListJson:

        if (orderJson["user"]["status"] == "ingame") & \
                (orderJson["platinum"] < price) & \
                (orderJson["order_type"] == "sell"):
            price = orderJson["platinum"]

    if price == 100000000000:
        price = 0

    return price
