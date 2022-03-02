import subprocess, concurrent.futures


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
    #make sure key and func indexes match
    keys = ["GPU Name", "Total Memory MiB", "Used Memory MiB", "GPU Temp C", "GPU Clock MHz", "VRAM Use %", "VRAM Clock MHz", "Fan Speed %"]
    funcs = [getGpuName, getTotalMemory, getUsedMemory, getGpuTemp, getGpuClock, getVramUse, getVramClock, getFanSpeed]

    with concurrent.futures.ThreadPoolExecutor() as thread:
        results = []
        for func in funcs:
            results.append(thread.submit(func))
    #assemble data and return to main
    for i in range(0, len(keys)):
        master[keys[i]] = results[i].result()
    
    master["BaseName"] = "GPU"
    return master
