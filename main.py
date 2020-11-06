from dataclasses import dataclass
import requests, json, pytesseract, cv2, pyautogui, numpy, keyboard
from ctypes import windll, Structure, c_long, byref

root = "https://api.warframe.market/v1"
player = 3


def getItemPrice(itemUrl):
    if itemUrl == "not to sell":
        return 0.0

    response = requests.get(root + "/items/" + itemUrl + "/orders")
    # print(json.dumps(response.json(), indent=4, sort_keys=True))

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


def doScreenShot():
    img = pyautogui.screenshot()
    img = cv2.cvtColor(numpy.array(img),
                       cv2.COLOR_RGB2BGR)
    cv2.imwrite("image1.png", img)
    return img


def loadImage(name):
    img = cv2.imread(name)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img


def readScreen(img):
    pytesseract.pytesseract.tesseract_cmd = "H:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    data = []
    if player == 4:
        cimg = img[410:455, 500:740]
        data.append(pytesseract.image_to_string(cimg))

        cimg = img[410:455, 730:960]
        data.append(pytesseract.image_to_string(cimg))

        cimg = img[410:455, 960:1190]
        data.append(pytesseract.image_to_string(cimg))

        cimg = img[410:455, 1190:1420]
        data.append(pytesseract.image_to_string(cimg))

    if player == 3:
        cimg = img[410:455, 630:840]
        data.append(pytesseract.image_to_string(cimg))

        cimg = img[410:455, 850:1070]
        data.append(pytesseract.image_to_string(cimg))

        cimg = img[410:455, 1080:1300]
        data.append(pytesseract.image_to_string(cimg))

    return data


response = requests.get(root + "/items")

itemListJson = response.json()["payload"]["items"]

items = []
itemUrls = []
for itemJson in itemListJson:
    items.append(itemJson["item_name"])
    itemUrls.append(itemJson["url_name"])

items.append("Forma Blueprint")
itemUrls.append("not to sell")

#datas = readScreen(loadImage("image2.png"))
datas = readScreen(doScreenShot())

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

    print(bestItem + " " + str(getItemPrice(bestItemUrl)))
