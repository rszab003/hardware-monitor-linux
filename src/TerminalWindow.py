import curses, time
from distutils.log import error
from curses import textpad
import main


def parseCpuData(sc: curses.window, data: dict):
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
        
        delayAmt, hwData = getHwData()
        
        try:
            # sc.addstr(15,15, f"KEY IS!!!::: {key}")
            #0 = CPU, 1 = GPU, 2 = RAM, 3 = Motherboard
            # sc.addstr(str(task))        
            updateSimple(sc, navHighlight)
            if navHighlight == 0:
                parseCpuData(sc, hwData[navHighlight].result())
        except curses.error:
            sc.addstr("WINDOW IS TOO SMALL")
        # sc.addstr(8,8, str(delayAmt))        
        sc.refresh()
        time.sleep(1 - delayAmt)
        
if __name__ == "__main__":
    curses.wrapper(run)
