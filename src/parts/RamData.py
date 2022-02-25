import converter
import subprocess

#reads how many RAM sticks are installed, returns vendor, size, and clock
#This method might change how the whole program is executed. Will need root privelages
def getConfiguration():
    config = []
    response = subprocess.Popen(
        ["sudo", "lshw", "-class", "memory"], stdout=subprocess.PIPE
        ).communicate()
    response = response[0].decode("utf-8").split("\n")[20:]
    cutoff = 0
    #this loop shortens the output to what we actually need, cuts off info about cpu cache
    #must be found iteratively to work on any machine
    for idx, item in enumerate(response[::-1]):
        if "*-cache:0" in item:
            cutoff = len(response) - idx - 1
            break
    response = response[:cutoff]
    response = [res.strip() for res in response]
    # print(response)
    idx = 0
    #filters out any non ram stick information in-between
    while (idx < len(response)):
        if "vendor" in response[idx]:
            for i in range(idx, idx + 7):
                config.append(response[i])
            idx += 6 #ensures we do not iterate over the same info again
        idx += 1
    # print("config: {}".format(config))
    counter = 1; stickCount = 0
    finalOutput = []
    # print(finalOutput)

    #assembles each ram stick into a list of dicts: [{stick1}, {stick2}, etc]
    for i, data in enumerate(config):
        if i == 0 or counter % 8 == 0: #make a new dict for each ram stick
            finalOutput.append({})
        if counter % 8 == 0 and i != 0: #counter % 8 checks if all data for each ram stick is parsed
            #7 data points per ram stick so need to check 7+1
            stickCount += 1
        data = data.split(": ")
        finalOutput[stickCount][data[0]] = data[1]
        counter += 1
    return finalOutput


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
    master = getRamData()
    master["RAM Stick Info"] = getConfiguration()
    print(master)
