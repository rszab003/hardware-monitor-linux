#!/usr/bin/python3

import os, json, itertools, init

master = {}


def refreshUsageData(currUsages):
    mapsFi = open("/tmp/openhwmon_linux/maps.json", "r+")
    maps = json.load(mapsFi)
    # print("WE ARE IN REFRESH DATA USAGE!!!!!!", maps)
    maps["prevUsageData"] = currUsages
    # print("MAPS NOW!!!", maps)
    mapsFi.seek(0); mapsFi.truncate()
    json.dump(maps, mapsFi, indent=3)
    mapsFi.close()

#TODO ADD THIS DATA TO MASTER!!!
def calcUsage(prevUsages, currUsages):
    allUsages = []
    refreshUsageData(currUsages)
    for i in range(0, len(prevUsages)):
        del prevUsages[i][0]
        # print(prevUsages[i])
        del currUsages[i][0]
        # print(currUsages[i])
        prevUsages[i] = list(map(int, prevUsages[i]))
        currUsages[i] = list(map(int, currUsages[i]))

    for i in range(0, len(prevUsages)):
        prevUseTime = 0; prevIdleTime = 0
        currUseTime = 0; currIdleTime = 0
        allUseTimeCurr = 0; allUseTimePrev = 0
        # print("CPU {} !!!!".format(i))
        for j in range(0, len(prevUsages[i])):
            if j == 3:
                prevIdleTime += prevUsages[i][j]
                currIdleTime += currUsages[i][j]
                # print("HELLOOOOO {} {}".format(prevIdleTime, currIdleTime))
            else:
                prevUseTime += prevUsages[i][j]
                currUseTime += currUsages[i][j]
            allUseTimeCurr += currUsages[i][j]
            allUseTimePrev += prevUsages[i][j]
            # print("CHECK!!!!::: ")
        # print("PREV USAGE::: {}\tCURR USAGE::: {}\tDIFF:::{}".format(prevUseTime, currUseTime, currUseTime - prevUseTime))
        # print("PREV IDLE::: {}\tCURR IDLE::: {}\tDIFF:::{}".format(prevIdleTime, currIdleTime, currIdleTime - prevIdleTime))
        # print("ALL USE TIME!!! CURR::: {}\tPREV:::{}\tDIFF:::{}".format(allUseTimeCurr, allUseTimePrev, allUseTimeCurr - allUseTimePrev))
        percentage = ((currUseTime - prevUseTime) - (currIdleTime - prevIdleTime)) / (allUseTimeCurr - allUseTimePrev)
        allUsages.append(abs(percentage))
    print("PERCENTAGES::: {}".format(allUsages))
            
    


def getUsage():
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
    calcUsage(prevUsages, currUsages)


def getCpuTemp():
    global master
    #TODO implement file creation in determineCpuTempDirectory() method
    tempDir = init.determineCpuTempDirectory() #folder that should hold temperature data
    if (tempDir == -1):
        return -1
    #core count starts at 1 here for some reason
    coreID = 0
    for i in range(1, os.cpu_count() + 2):
        cpuTempLoc = tempDir + "/temp{}_input".format(str(i))
        try:
            with open(cpuTempLoc, "r") as fi:
                temp = fi.read()[:-1]
                # print(temp)
                if i == 1:
                    master["CPU TEMP"] = temp
                else:
                    master["Cores"][coreID]["Temp"] = temp
                    coreID += 1
        except FileNotFoundError as ex:
            print("ERROR: could not find: {}".format(cpuTempLoc))
            print(ex)
    

    

# GET CPU MODEL, CACHE SIZE & CURR CLOCK SPEEDS
def cpuInfo():
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
        # exp = json.dumps(str(parsedData))
        global master
        master = parsedData
        # print("---------------")
        # print(master)
        cpuInfoFile.close()
    except Exception as ex:
        print("ERROR GETTING CPU DATA!")
        print(ex)
        
