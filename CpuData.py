#!/usr/bin/python3

from distutils import core
import os, json

master = {}
#FIND HWMON DIRECTORY THAT HOLDS CPU TEMPS
#TODO make this only run once when program starts, since this directory does not frequently change
def determineCpuTempDirectory():
    hwmonDir = "/sys/class/hwmon"
    for rootDirPath, subDirs, files in os.walk(hwmonDir, followlinks=True):
        distance = rootDirPath.count(os.sep) - hwmonDir.count(os.sep) #depth of os.walk
        if distance != 0: #don't check 1st directory
            checkName = rootDirPath + "/name"
            try:
                with open(checkName, "r") as fi:
                    name = fi.read()
                    if name == "coretemp\n":
                        return checkName[:-5] #remove "/name" from file path
            except FileNotFoundError as ex:
                print("ERROR WITH HWMON PARSING! No file found called \"name\"")
                print(ex)
        if distance >= 1:
            del subDirs[:]
    return -1


def getCpuTemp():
    global master
    tempDir = determineCpuTempDirectory() #folder that should hold temperature data
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
        


def gpuTemp():
    filePath = "/sys/class/hwmon/hwmon3/temp1_input"
    print("GPU TEMP: " + open(filePath).read())

def main():
    cpuInfo()
    getCpuTemp()
    print("*" * 30)
    print(master)
    gpuTemp()
    


if __name__ == "__main__":
    main()