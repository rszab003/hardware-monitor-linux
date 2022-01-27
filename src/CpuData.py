#!/usr/bin/python3

import os, json, itertools, init

master = {}

#TODO FIX BUG WHERE MAPS.JSON IS EMPTY!!!
# def refreshUsageData(currUsages):
#     mapsFi = open("/tmp/openhwmon_linux/maps.json", "w+")
#     maps = json.load(mapsFi)
#     print("WE ARE IN MAPS!!!!", maps)
#     maps["prevUsageData"] = currUsages
#     print("MAPS NOW!!!", maps)
#     json.dump(maps, mapsFi, indent=3)
#     mapsFi.close()

#TODO ADD THIS DATA TO MASTER!!!
def calcUsage(prevUsages, currUsages):
    # refreshUsageData(currUsages)
    prevIdle = []
    currIdle = []
    for i in range(0, len(prevUsages)):
        prevIdle.append(int(prevUsages[i][4]))
        currIdle.append(int(currUsages[i][4]))
        del prevUsages[i][4]; del currUsages[i][4] #deletes idle and cpu labels. 
        #this is already known from the order of the list
        del prevUsages[i][0]; del currUsages[i][0]
    totUsages = []
    for i in range(0, len(prevUsages)):
        prevUsages[i] = list(map(int, prevUsages[i])) #convert string to int
        currUsages[i] = list(map(int, currUsages[i]))
        prevUsages[i] = list(itertools.accumulate(prevUsages[i])) #quick way to get the sum total of cpu usage
        currUsages[i] = list(itertools.accumulate(currUsages[i]))
        sumCurr = currUsages[i][len(currUsages[i]) - 1]
        sumPrev = prevUsages[i][len(prevUsages[i]) - 1]
        totUsages.append(sumCurr - sumPrev)
    print("CURR IDLE BEFORE!!!!", currIdle)
    finalUsage = []
    for i in range(0, len(currIdle)):
        currIdle[i] = currIdle[i] - prevIdle[i]
        finalUsage.append( 100 * ( (totUsages[i] - currIdle[i]) / (totUsages[i] + currIdle[i]) ) )
    
    
    print("FINAL USAGES!!!!::: ", finalUsage)
    print("PREV IDLE!!!")
    print(prevIdle)
    # print("PREVUSAGES!!!")
    # print(prevUsages)
    print("CURR IDLE!!!")
    print(currIdle)
    # print(currUsages)

#TODO /proc/stat carries total usages from startup. make a method that subtracts the current values from the previous
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
        
