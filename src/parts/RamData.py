# import UnitConverter_hwmon
# from parts import UnitConverter_hwmon
import subprocess, concurrent.futures

#reads how many RAM sticks are installed, returns vendor, size, and clock
#This method might change how the whole program is executed. Will need root privelages
def getConfiguration():
    config = []
    response = subprocess.run(["sudo", "lshw", "-class", "memory"], text=True, capture_output=True).stdout
    response = response.split("\n")[20:]
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
            for idx in range(idx, idx + 7):
                config.append(response[idx])
            idx += 6 #ensures we do not iterate over the same info again
        idx += 1
    # print("config: {}".format(config))
    counter = 1; stickCount = 0
    finalOutput = []
    # print(finalOutput)

    #assembles each ram stick into a list of dicts: [{stick1}, {stick2}, etc]
    for idx, data in enumerate(config):
        if idx == 0 or counter % 8 == 0: #make a new dict for each ram stick
            finalOutput.append({})
        if counter % 8 == 0 and idx != 0: #counter % 8 checks if all data for each ram stick is parsed
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
            
            newVal, unit = UnitConverter_hwmon.convert(int(memData[1]), "kilobyte", "megabyte")
            newVal = round(newVal, 4)
            master[memData[0][:-1]] = str(newVal) + " " + unit
    return master


def fetch() -> dict:
    results = []
    with concurrent.futures.ThreadPoolExecutor() as thread:
        results.append(thread.submit(getRamData))
        results.append(thread.submit(getConfiguration))
    master = results[0].result()
    master["Ram Stick Data"] = results[1].result()
    return master


if __name__ == "__main__":
    import UnitConverter_hwmon
    master = fetch()
    print(master)
else:
    from parts import UnitConverter_hwmon
