import os, json, concurrent.futures, time


def refreshUsageData(currUsages: list) -> None:
    mapsFi = open("/tmp/openhwmon_linux/maps.json", "r+")
    maps = json.load(mapsFi)
    maps["prevUsageData"] = currUsages
    # print("MAPS NOW!!!", maps)
    mapsFi.seek(0); mapsFi.truncate()
    json.dump(maps, mapsFi, indent=3)
    mapsFi.close()


def calcUsage(prevUsages: list, currUsages: list, master: dict) -> dict:
    allUsages = []
    # refreshUsageData(currUsages)
    for i in range(0, len(prevUsages)):
        del prevUsages[i][0]
        del currUsages[i][0]
        prevUsages[i] = list(map(int, prevUsages[i]))
        currUsages[i] = list(map(int, currUsages[i]))

    for i in range(0, len(prevUsages)):
        prevUseTime = 0; prevIdleTime = 0
        currUseTime = 0; currIdleTime = 0
        allUseTimeCurr = 0; allUseTimePrev = 0
        for j in range(0, len(prevUsages[i])):
            if j == 3:
                prevIdleTime += prevUsages[i][j]
                currIdleTime += currUsages[i][j]
            else:
                prevUseTime += prevUsages[i][j]
                currUseTime += currUsages[i][j]
            allUseTimeCurr += currUsages[i][j]
            allUseTimePrev += prevUsages[i][j]
        percentage = ((currUseTime - prevUseTime) - (currIdleTime - prevIdleTime)) / (allUseTimeCurr - allUseTimePrev)
        allUsages.append(abs(percentage))
    # print("PERCENTAGES::: {}".format(allUsages))
    for i in range(0, len(master["Cores"])):
        master["Cores"][i]["Usage"] = allUsages[i]
    return master



def getUsage() -> tuple:
    currUsageFile = "/proc/stat"; prevUsageFile = "/tmp/openhwmon_linux/maps.json"
    currUsages = []
    try:
        f = open(prevUsageFile, "r")
        prevUsages = json.load(f)
        prevUsages = prevUsages["prevUsageData"]
        f.close()
    except FileNotFoundError as ex:
        print("ERROR GETTING PREV USAGE DATA")
        print(ex)
    # print("PREV USAGES!!!\n", prevUsages)
    try:
        with open(currUsageFile, "r") as fi:
            for i in range(0, os.cpu_count() + 1):
                currUsages.append(fi.readline()[:-1].split())
        # print(currUsages)
    except FileNotFoundError as ex:
        print("ERROR GETTING CURRENT USAGE DATA")
        print(ex)
    return (prevUsages, currUsages)



def getCpuTemp(master: dict) -> dict:
    try:
        with open("/tmp/openhwmon_linux/maps.json", "r") as fi:
            tempDir = json.load(fi)
            tempDir = tempDir["cpuTempDir"]
    except FileNotFoundError as ex:
        print("ERROR! FILE WAS NOT MADE IN init.py.\nCHECK init.determineCpuTempDirectory()")
        print(ex)
    if (tempDir == -1):
        return -1
    #core count starts at 1 here for some reason
    coreID = 0
    for i in range(1, os.cpu_count() + 2):
        cpuTempLoc = tempDir + "/temp{}_input".format(str(i))
        try:
            with open(cpuTempLoc, "r") as fi:
                temp = fi.read()[:-1]
                if i == 1:
                    master["CPU TEMP"] = temp
                else:
                    master["Cores"][coreID]["Temp"] = temp
                    coreID += 1
        except FileNotFoundError as ex:
            print("ERROR: could not find: {}".format(cpuTempLoc))
            print(ex)
    return master



# GET CPU MODEL, CACHE SIZE & CURR CLOCK SPEEDS
def cpuInfo() -> dict:
    parsedData = {}
    try:
        cpuInfoFile = open("/proc/cpuinfo", "r")
        cpuDump = cpuInfoFile.readlines()
        #GET MODEL AND CACHE SIZE
        model = cpuDump[4][13:]
        cacheSize = cpuDump[8][13:]
        parsedData["CPU Model"] = model[:-1] #removes \n character
        parsedData["CPU Cache Size"] = cacheSize[:-1]
        parsedData["Cores"] = []
        #GET CLOCK SPEED
        coreID = 0
        for line in cpuDump:
            if "cpu MHz" in line:
                parsedData["Cores"].append(
                    {
                        "id" : coreID,
                        "Clock MHz" : float(line[11:-1]),
                    }
                )
                coreID += 1
        cpuInfoFile.close()
        return parsedData
    except Exception as ex:
        print("ERROR GETTING CPU DATA!")
        print(ex)


def fetch() -> dict:
    master = {}
    master = cpuInfo()
    master = getCpuTemp(master)
    prevCurrUsage = getUsage()
    refreshUsageData(prevCurrUsage[1]) #Stores current usage data for next calculation
    master = calcUsage(prevCurrUsage[0], prevCurrUsage[1], master)
    return master