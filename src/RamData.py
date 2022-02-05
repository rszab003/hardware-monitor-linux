

def getRamData() -> dict:
    master = {}
    with open("/proc/meminfo", "r") as fi:
        for i in range(0, 10):
            memData = fi.readline()[:-1]
            memData = memData.split()
            if len(memData) != 3: #might not be necessary i just dont know how this differs on other distros
                raise Exception("ERROR PARSING MEMORY DATA: Check length of /proc/meminfo\nShould be split into three sections.")
            master[memData[0][:-1]] = memData[1] + " " + memData[2]
    return master