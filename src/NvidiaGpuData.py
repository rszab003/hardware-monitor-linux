import subprocess

master = {}


def getGpuTemp():
    global master
    # print("HELLO!!! GET THE TEMP!!!")
    temperatureData = subprocess.run(["nvidia-smi", "--query-gpu=temperature.gpu", "--format=csv"], text=True, capture_output=True)
    temperatureData = temperatureData.stdout.split()
    master["GPU Temperature"] = int(temperatureData[1])
    # print(master)


def getGpuClock():
    global master
    currClockSpeed = subprocess.run(["nvidia-smi", "--query-gpu=clocks.gr", "--format=csv"], text=True, capture_output=True)
    currClockSpeed = currClockSpeed.stdout.split("\n")[1][:-4]
    master["GPU ClockSpeed-MHz"] = int(currClockSpeed)
    print(master)


def getVramUse():
    pass


def getVramClock():
    pass


def getFanSpeed():
    pass


def fetch():
    getGpuTemp()
    getGpuClock()