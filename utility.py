import cv2
import numpy
import pyautogui


def doScreenShot():
    img = pyautogui.screenshot()
    img = cv2.cvtColor(numpy.array(img), cv2.COLOR_RGB2BGR)
    cv2.imwrite("screenshot\\screenshot1.png", img)
    return img


def loadImage(name):
    img = cv2.imread(name)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img


def computeSecondsToHigherUnits(seconds, highestUnit):
    """
    berechnet aus seconds anz. sekunden, minuten, ...

    @param seconds: zeit in sekunden
    @type seconds: float oder int
    @param highestUnit: grösste zu berechnende zeiteinheit. möglich: sec, min, h, d, week, year
    @type highestUnit: string
    """
    units = ['sec', 'min', 'h', 'd']  # reihe der einheiten
    unreached = {'sec': 60,  # nicht zu erreichen, falls highestUnit eine grössere zeiteinheit ist
                 'min': 60,
                 'h': 24
                 }
    # anfügen von grösserer zeiteinheit zu units und unreached
    if highestUnit == 'week':
        units.append('week')
        unreached['d'] = 7
    elif highestUnit == 'year':
        units.append('year')
        unreached['d'] = 365
    # behandeln von nachkommastellen bei seconds
    res = {'partSec': seconds - int(seconds)}
    seconds = int(seconds)
    # berechnen der zeiten pro zeiteinheit
    left = seconds
    i = 0
    while left:
        if units.index(highestUnit) > i:
            res[units[i]] = left % unreached[units[i]]  # anteil der aktuellen zeiteinheit
            left = int(left / unreached[units[i]])  # übrigbleibende zeit in der nächst grösseren zeiteinheit
        else:
            res[units[i]] = left
            break
        i += 1
    return res