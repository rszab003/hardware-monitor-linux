#CREATE DIRECTORY IN TEMP TO LOG PREV CPU USAGE,
#DETERMINE CPU TEMP DIRECTORY

from os.path import exists
import os, json


def createTempFS():
    if not exists("/tmp/openhwmon_linux"):
        os.mkdir("/tmp/openhwmon_linux", 755)
    
    if not exists("/tmp/openhwmon_linux/maps.json"):
        data = {
            "cpuTempDir" : determineCpuTempDirectory(),
            "prevUsageData" : getUsage()
        }
        with open("/tmp/openhwmon_linux/maps.json", "w") as fi:
            json.dump(data, fi, indent=3)


def getUsage():
    usageFile = "/proc/stat"
    lst = []
    try:
        with open(usageFile, "r") as fi:
            for i in range(0, os.cpu_count() + 1):
                usageData = fi.readline()[:-1].split()
                lst.append(usageData)
    except Exception as ex:
        print("Error Getting Prev USAGE DATA")
        print(ex)
    return lst


#FIND HWMON DIRECTORY THAT HOLDS CPU TEMPS
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