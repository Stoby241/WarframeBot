import json

import cv2
import numpy
import pyautogui


def doScreenShot():
    img = pyautogui.screenshot()
    img = cv2.cvtColor(numpy.array(img),
                       cv2.COLOR_RGB2BGR)
    cv2.imwrite("image4.png", img)
    return img


def loadImage(name):
    img = cv2.imread(name)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img