import curses
import main
from curses import textpad



def update(sc, highlight) -> list:
    programTitle = "OPEN HARDWARE MONITOR"
    navHelpText = "USE ARROW KEYS TO SWITCH FOCUS"
    y, x = sc.getmaxyx()
    titlePlacement = (x // 2) - (len(programTitle) // 2)
    quitPlacement = y - 2
    boundingBox = [1, 1, y-3, x-3]
    navHelpPlacement = (x // 2) - (len(navHelpText) // 2)
    textpad.rectangle(sc, 1, 1, y-3, x-3)
    sc.addstr(0, titlePlacement, programTitle)
    sc.addstr(quitPlacement, 1, "Press \'q\' to quit.")
    sc.addstr(y - 2, navHelpPlacement, navHelpText)
    
    #BUILD NAV, LOWER RIGHT
    navItems = ["CPU", "GPU", "RAM", "MOTHERBOARD"]
    yPlacement = y - 2
    xPlacement = x - 3
    totNavLength = 0; count = 0
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    for i in range(0, len(navItems)):
        totNavLength += len(navItems[i]) + 1
        if i == highlight:
            sc.addstr(yPlacement, xPlacement - totNavLength, navItems[i], curses.color_pair(1))
        else:
            sc.addstr(yPlacement, xPlacement - totNavLength, navItems[i])
    return boundingBox

def getHwData(sc):
    allHwData = main.executeThreads()
    cpuData = allHwData[0]
    sc.addstr(2,3, str(cpuData.result()))


def run(sc):
    navHighlight = 0
    curses.curs_set(0)
    # sc.nodelay(1)
    update(sc, navHighlight)
    while True:
        key = sc.getch()
        sc.clear()
        if key == ord("q") or key == ord("Q"):
            break
        if key == curses.KEY_RIGHT and navHighlight > 0:
            navHighlight -= 1
        elif key == curses.KEY_RIGHT and navHighlight == 0:
            navHighlight = 3
        if key == curses.KEY_LEFT and navHighlight < 3:
            navHighlight += 1
        elif key == curses.KEY_LEFT and navHighlight == 3:
            navHighlight = 0
        # time.sleep(1.5)
        update(sc, navHighlight)
        sc.refresh()
        
        # getHwData(sc)
        



curses.wrapper(run)
