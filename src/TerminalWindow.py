import curses, time
from re import S
from curses import textpad
import main


def getHwData() -> tuple:
    start = time.perf_counter()
    allData = main.executeThreads()
    finish = time.perf_counter()
    return (finish - start, allData)


def updateSimple(sc, highlight, data):
    navItems = ["CPU", "GPU", "RAM", "MOTHERBOARD"]
    y,x = sc.getmaxyx()
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
    sc.addstr(5,5, str(data))



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
    
        sc.addstr(15,15, f"KEY IS!!!::: {key}")
        #0 = CPU, 1 = GPU, 2 = RAM, 3 = Motherboard
        # sc.addstr(str(task))        
        delayAmt, hwData = getHwData()
        sc.addstr(8,8, str(delayAmt))
        updateSimple(sc, navHighlight, hwData[navHighlight].result())
        sc.refresh()
        time.sleep(1 - delayAmt)
        
        # getHwData(sc)
        
if __name__ == "__main__":
    curses.wrapper(run)
