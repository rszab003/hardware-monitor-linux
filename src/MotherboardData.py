import os, json

def getBoardTemp(boardData: dict) -> dict:
    boardTemp = {}
    try:
        with open("/tmp/openhwmon_linux/maps.json", "r") as fi:
            targetDir = json.load(fi)
            targetDir = targetDir["motherboardTempDir"]
    except Exception as ex:
        print("ERROR RETRIEVING BOARD TEMP LOCATION!!")
        print(ex)
    for fi in os.listdir(targetDir):
        if "input" in fi:
            with open(targetDir + "/" + fi, "r") as tempFile:
                boardData[fi] = tempFile.read()[:-1]
    return boardData


#Get name and models for Motherboard and BIOS
def getGeneralInfo() -> list:
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
    return [boardData, biosData]


def fetch() -> list:
    boardBiosData = getGeneralInfo()
    boardBiosData[0] = getBoardTemp(boardBiosData[0])
    return boardBiosData