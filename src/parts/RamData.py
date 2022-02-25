import converter
import subprocess

#reads how many RAM sticks are installed, returns vendor, size, and clock
def getConfiguration():
    config = []
    response = subprocess.Popen(
        ["sudo", "lshw", "-class", "memory"], stdout=subprocess.PIPE
        ).communicate()
    response = response[0].decode("utf-8").split("\n")[20:]
    cutoff = 0
    for idx, item in enumerate(response[::-1]):
        if "*-cache:0" in item:
            cutoff = len(response) - idx - 1
            break
    response = response[:cutoff]
    response = [res.strip() for res in response]
    print(response)
    idx = 0

    #filters out only ram stick information
    while (idx < len(response)):
        # print(idx)
        if "vendor" in response[idx]:
            for i in range(idx, idx + 7):
                config.append(response[i])
            idx += 6
        idx += 1
    print("config: {}".format(config))


#GETS CURRENT MEMORY USAGE STATUS
def getRamData() -> dict:
    master = {}
    with open("/proc/meminfo", "r") as fi:
        for _ in range(0, 10):
            memData = fi.readline()[:-1]
            memData = memData.split()
            if len(memData) != 3: #might not be necessary i just dont know how this differs on other distros
                raise Exception("ERROR PARSING MEMORY DATA: Check length of /proc/meminfo\nShould be split into three sections.")
            
            newVal, unit = converter.convert(int(memData[1]), "kilobyte", "megabyte")
            newVal = round(newVal, 4)
            master[memData[0][:-1]] = str(newVal) + " " + unit
    
    return master


if __name__ == "__main__":
    # master = getRamData()
    # for _ in range(0, 10):
    master = getConfiguration()
    print(master)
