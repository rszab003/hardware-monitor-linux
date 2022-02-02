import init, CpuData, NvidiaGpuData
from enum import Enum

class Driver(Enum):
    nvidia = 1
    nouveau = 2
    amd = 3

def main():
    #TODO Make a method in init that determines which sort of Driver one is using
    driverVersion = Driver.nvidia
    # print("DRIVERVER!!!:: {}".format(driverVersion.value))
    init.createTempFS()
    init.determineCpuTempDirectory()
    CpuData.fetch()
    print("*" * 30)
    print(CpuData.master)
    print("*" * 30)
    if driverVersion == Driver.nvidia:
        NvidiaGpuData.fetch()

    
if __name__ == "__main__":
    main()