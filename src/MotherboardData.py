import os


def getBoardTemp() -> None:
    targetDir = "sys/class/hwmon"


#Gets name and models of Motherboard and BIOS
def getGeneralInfo() -> tuple:
    boardData = {}; biosData = {}
    targetDir = "/sys/devices/virtual/dmi/id"
    for fi in os.listdir(targetDir):
        if "board" in fi:
            if fi == "board_serial": #TODO must open this with root privelages
                continue
            with open(targetDir+"/"+fi, "r") as f:
                boardData[fi] = f.read()[:-1]
        if "bios" in fi:
            with open(targetDir+"/"+fi, "r") as f:
                biosData[fi] = f.read()[:-1]
    return (boardData, biosData)


def fetch() -> tuple:
    boardBiosData = getGeneralInfo()
    return boardBiosData