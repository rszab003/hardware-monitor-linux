#!/usr/bin/python3

import os, json, init

master = {}

#TODO /proc/stat carries total usages from startup. make a method that subtracts the current values from the previous
def calcUsage():
    usageFile = "/proc/stat"
    try:
        with open(usageFile, "r") as fi:
            for i in range(0, os.cpu_count() + 1):
                usageData = fi.readline()[:-1].split()

                print(usageData)
    except Exception as ex:
        print("ERROR Calculating Usage!!!")
        print(ex)
    return -1


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
        
