import curses, asyncio
import main, time
from curses import textpad

async def updateSimple(sc, xx, highlight):
    sc.addstr(3,3,str(highlight))
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



async def update(sc, highlight) -> list:
    programTitle = "OPEN HARDWARE MONITOR"
    navHelpText = "USE ARROW KEYS"
    y, x = sc.getmaxyx()
    titlePlacement = (x // 2) - (len(programTitle) // 2)
    quitPlacement = y - 2
    boundingBox = [1, 1, y-3, x-3]
    navHelpPlacement = (x // 2) - (len(navHelpText) // 2)
    textpad.rectangle(sc, 1, 1, y-3, x-3)
    sc.addstr(0, titlePlacement, programTitle)
    sc.addstr(quitPlacement, 1, "Press \'q\' to quit.")
    sc.addstr(y - 2, navHelpPlacement, navHelpText)
    
    # BUILD NAV, LOWER RIGHT
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



async def run(sc: curses.window):
    sc.nodelay(True)
    navHighlight = 0
    curses.curs_set(0)
    x = 1
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
        # getHwData(sc, navHighlight)
        # upd = loop.create_task(update(sc, navHighlight))
        r1 = asyncio.create_task(updateSimple(sc, x, navHighlight))
        x += 1
        await asyncio.sleep(1)
        # await r1
        sc.refresh()
        # time.sleep(1)
        
        # getHwData(sc)
        
if __name__ == "__main__":
    try:
        asyncio.run(curses.wrapper(run))
    except Exception as ex:
        print(ex)
    finally:
        loop.close()
