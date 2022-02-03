import subprocess


def getGpuName() -> str:
    name = subprocess.run(["nvidia-smi", "--query-gpu=name", "--format=csv"], text=True, capture_output=True, check=True)
    return name.stdout.split("\n")[1]


def getTotalMemory() -> int:
    totMem = subprocess.run(["nvidia-smi", "--query-gpu=memory.total", "--format=csv"], text=True, capture_output=True, check=True)
    totMem = totMem.stdout.split()
    return int(totMem[2])


def getUsedMemory() -> int:
    usedMem = subprocess.run(["nvidia-smi", "--query-gpu=memory.used", "--format=csv"], text=True, capture_output=True, check=True)
    usedMem = usedMem.stdout.split()
    return int(usedMem[2])


def getGpuTemp() -> int:
    temperatureData = subprocess.run(["nvidia-smi", "--query-gpu=temperature.gpu", "--format=csv"], text=True, capture_output=True, check=True)
    temperatureData = temperatureData.stdout.split()
    return int(temperatureData[1])


def getGpuClock() -> int:
    currClockSpeed = subprocess.run(["nvidia-smi", "--query-gpu=clocks.gr", "--format=csv"], text=True, capture_output=True, check=True)
    currClockSpeed = currClockSpeed.stdout.split("\n")[1][:-4]
    return int(currClockSpeed)


def getVramUse() -> int:
    currVramUse = subprocess.run(["nvidia-smi", "--query-gpu=utilization.memory", "--format=csv"], text=True, capture_output=True, check=True)
    currVramUse = currVramUse.stdout.split()
    return int(currVramUse[2])


def getVramClock() -> int:
    vramClock = subprocess.run(["nvidia-smi", "--query-gpu=clocks.mem", "--format=csv"], text=True, capture_output=True, check=True)
    vramClock = vramClock.stdout.split()
    return int(vramClock[2])


def getFanSpeed() -> int:
    currFanSpeed = subprocess.run(["nvidia-smi", "--query-gpu=fan.speed", "--format=csv"], text=True, capture_output=True, check=True)
    currFanSpeed = currFanSpeed.stdout.split()
    return int(currFanSpeed[2])


def fetch() -> dict:
    
    master = {}
    master["GPU Name"] = getGpuName()
    master["Total Memory MiB"] = getTotalMemory()
    master["Used Memory MiB"] = getUsedMemory()
    master["GPU Temp C"] = getGpuTemp()
    master["GPU Clockspeed MHz"] = getGpuClock()
    master["GPU VRAM Use %"] = getVramUse()
    master["VRAM Clock MHz"] = getVramClock()
    master["Fan Speed %"] = getFanSpeed()
    return master