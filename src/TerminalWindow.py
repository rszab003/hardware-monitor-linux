import curses
import main, time
from curses import textpad


programTitle = "OPEN HARDWARE MONITOR"

def update(sc) -> list:
    y, x = sc.getmaxyx()
    titlePlacement = (x // 2) - (len(programTitle) // 2)
    quitPlacement = y - 2
    boundingBox = [1, 1, y-3, x-3]
    textpad.rectangle(sc, 1, 1, y-3, x-3)
    sc.addstr(0, titlePlacement, programTitle)
    sc.addstr(quitPlacement, 1, "Press \'q\' to quit.")
    return boundingBox

def parseCpuData(sc, cpuData):
    y, x = sc.getmaxyx()
    currY = 2; currX = 2
    maxX = 0
    for key in cpuData.keys():
        if key == "Cores":
            continue
        sc.addstr(currY, currX, key)
        currY += 1
        if len(key) > maxX: #FINDS STARTING POINT FOR VALUES
            maxX = len(key)
    currY = 2; currX = maxX + 3; maxX += 3
    for val in cpuData.values():
        if type(val) == list: #skip individual core data for now
            continue
        sc.addstr(currY, currX, ": " + str(val))
        currY += 1
    sc.addstr(currY + 1, 2, "CORES")
    for key in cpuData["Cores"]:
        sc.addstr(currY, currX, str(key))
        currY += 1
    for i in range(2, x - 3):
        sc.addstr(currY, i, "-")

        
    
def printHardwareData(sc):
    hwData = main.executeThreads()
    for i in range(0, len(hwData)):
        if i == 0: # CPU INDEX
            parseCpuData(sc, hwData[i].result())


def run(sc):
    curses.curs_set(0)
    sc.nodelay(1)
    update(sc)
    while True:
        boundingBox = update(sc)
        key = sc.getch()
        sc.clear()
        
        if key == ord("q") or key == ord("Q"):
            break
        if key == curses.KEY_RESIZE:
            sc.addstr(boundingBox[2]//2, boundingBox[3]//3, f"YOU ARE RESIZING!!! {boundingBox[3]} {boundingBox[2]}")
        
        time.sleep(1.5)
        printHardwareData(sc)
        sc.refresh()



curses.wrapper(run)