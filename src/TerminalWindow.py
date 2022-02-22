import curses, time
from curses import textpad
import main
from math import ceil

# Method that should parse all hardware data other than CPU
def parseHwPart(sc: curses.window, part: dict, startY: int, startX: int) -> None:
    # sc.addstr(15, 8, str(data))
    currY = startY; currX = startX
    maxCols = 2; currCols = 1
    
    longestLabel = [len(key) + 2 + len(str(part[key])) for key in part.keys()]
    longestLabel = max(longestLabel) + 2
    
    for key in part.keys():
        label = f"{key}:"
        data = str(part[key])
        if currX == 3: #we are on first column
            sc.addstr(currY, currX, label, curses.A_BOLD)
            currX += len(label)
            sc.addstr(currY, currX + 1, data)
        else:
            sc.addstr(currY, longestLabel + 2, label, curses.A_BOLD)
            currX = longestLabel + len(label)
            sc.addstr(currY, currX + 3, data)
        if currCols < maxCols:
            currX += 1 + len(data)
            currCols += 1
        elif currCols >= maxCols: #Starts new Row
            currY += 1; currX = startX
            currCols = 1



def parseCpuData(sc: curses.window, data: dict) -> None:
    sep = " || "
    sc.addstr(2,3, data["CPU Model"])
    sc.addstr(2, 3 + len(data["CPU Model"]), sep + "Cache: {}".format(data["CPU Cache Size"]))
    sc.addstr(4, 3, "TEMPERATURES (C)")
    currX = 4; currY = 5
    maxY, maxX = sc.getmaxyx()
    for i in range(0, len(data["Temps"])):
        if i == 0:
            newStr = "CPU: " + str(data["Temps"][i])
            sc.addstr(currY, 4, newStr)
            currX += len(newStr)
        else:
            newStr = sep + f"Core {i}: " + str(data["Temps"][i])
            if len(newStr) + currX > maxX - 3:
                currY += 1
                currX = 4
                newStr = newStr[4:]
            sc.addstr(currY, currX, newStr)
            currX += len(newStr)
    currY += 2; currX = 4
    sc.addstr(currY, 3, "CLOCK SPEEDS (MHz)")
    newStr = ""
    def parseList(lst, currY, currX):
        for i in range(0, len(lst)):
            if i != 0:
                newStr = sep + f"Core {i}: " + str(lst[i])
            else:
                newStr = f"Core {i}: " + str(lst[i])
            if currX + len(newStr) > maxX - 3:
                currY += 1
                currX = 4
                newStr = newStr[3:]
            sc.addstr(currY, currX, newStr)
            currX += len(newStr)
        return currY + 2, 4
    
    currY, currX = parseList(data["Clocks"], 9, 4)
    sc.addstr(currY, currX - 1, "USAGES (%)")
    currY, currX = parseList(data["Usages"], currY + 1, currX)

#gets all hardware data
#returns a time interval to use with time.sleep()
def getHwData() -> tuple:
    start = time.perf_counter()
    allData = main.executeThreads()
    finish = time.perf_counter()
    return (finish - start, allData)


def updateSimple(sc, highlight) -> None:
    title = "OPEN HARDWARE MONITOR"
    navItems = ["CPU", "GPU", "RAM", "MOTHERBOARD"]
    y,x = sc.getmaxyx()
    yPlacement = y - 2
    xPlacement = x - 3
    totNavLength = 0; count = 0

    sc.addstr(0, (x // 2) - len(title) // 2, title)
    sc.addstr(yPlacement, 2, "Press \'q\' to quit")

    textpad.rectangle(sc, 1, 1, y-3, x-3)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    for i in range(0, len(navItems)):
        totNavLength += len(navItems[i]) + 1
        if i == highlight:
            sc.addstr(yPlacement, xPlacement - totNavLength, navItems[i], curses.color_pair(1))
        else:
            sc.addstr(yPlacement, xPlacement - totNavLength, navItems[i])



def run(sc: curses.window):
    sc.nodelay(True)
    navHighlight = 0
    curses.curs_set(0)
    
    while True:
        try:
            key = sc.getkey()
        except:
            key = None
        
        sc.clear()

        #Process key commands
        if key == "q" or key == "Q":
            break
        elif key == "KEY_RIGHT" and navHighlight > 0:
            navHighlight -= 1
        elif key == "KEY_RIGHT" and navHighlight == 0:
            navHighlight = 3
        elif key == "KEY_LEFT" and navHighlight < 3:
            navHighlight += 1
        elif key == "KEY_LEFT" and navHighlight == 3:
            navHighlight = 0
        
        #GET HW DATA
        delayAmt, hwData = getHwData()
        
        try:
            #0 = CPU, 1 = GPU, 2 = RAM, 3 = Motherboard       
            updateSimple(sc, navHighlight)
            if navHighlight == 0:
                parseCpuData(sc, hwData[navHighlight].result())
            elif navHighlight == 1:
                parseHwPart(sc, hwData[navHighlight].result(), 2, 3)
            elif navHighlight == 2:
                parseHwPart(sc, hwData[navHighlight].result(), 2, 3)
            elif navHighlight == 3:
                parseHwPart(sc, hwData[navHighlight].result()[0], 2, 3)
                parseHwPart(sc, hwData[navHighlight].result()[1], 8, 3)
        except curses.error:
            sc.addstr("WINDOW IS TOO SMALL") 
        sc.refresh()
        try: #in case getting hw data takes longer than one sec?
            time.sleep(1 - delayAmt)
        except ValueError:
            time.sleep(ceil(delayAmt) - delayAmt)
        
if __name__ == "__main__":
    curses.wrapper(run)
