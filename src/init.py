#CREATE DIRECTORY IN TEMP TO LOG PREV CPU USAGE,
#DETERMINE CPU TEMP DIRECTORY

from os.path import exists
import os

def createTempFS():
    if not exists("/tmp/openhwmon_linux"):
        os.mkdir("/tmp/openhwmon_linux", 755)
    
    if not exists("/tmp/openhwmon_linux/maps.json"):
        with open("/tmp/openhwmon_linux/maps.json", "w") as fi:
            cpuTempDir = determineCpuTempDirectory()
            fi.write(cpuTempDir)


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