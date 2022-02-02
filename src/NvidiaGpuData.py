import subprocess
from sys import stdout


master = {}


def getGpuTemp():
    global master
    # print("HELLO!!! GET THE TEMP!!!")

    temperatureData = subprocess.run(["nvidia-smi", "--query-gpu=temperature.gpu", "--format=csv"], text=True, capture_output=True)
    temperatureData = temperatureData.split()
    master[temperatureData[0]] = temperatureData[1]
    # print(temperatureData.stdout)


def getGpuClock():
    pass


def fetch():
    getGpuTemp()
    getGpuClock()