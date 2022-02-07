import subprocess, concurrent.futures, time


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
    # start = time.perf_counter()
    master = {}
    with concurrent.futures.ThreadPoolExecutor() as thread:
        results = []
        results.append(thread.submit(getGpuName))
        results.append(thread.submit(getTotalMemory))
        results.append(thread.submit(getUsedMemory))
        results.append(thread.submit(getGpuTemp))
        results.append(thread.submit(getGpuClock))
        results.append(thread.submit(getVramUse))
        results.append(thread.submit(getVramClock))
        results.append(thread.submit(getFanSpeed))
    # finish = time.perf_counter()
    master["GPU Name"] = results[0].result()
    master["Total Memory MiB"] = results[1].result()
    master["Used Memory MiB"]= results[2].result()
    master["GPU Temp C"]= results[3].result()
    master["GPU Clockspeed MHz"]= results[4].result()
    master["GPU VRAM Use %"]= results[5].result()
    master["VRAM Clock MHz"]= results[6].result()
    master["Fan Speed %"]= results[7].result()
    
    # print(f"TIME ASYNCHRONOUS::: {finish - start}")
    # start = time.perf_counter()
    # tmp = getGpuTemp()
    # name = getGpuName()
    # clk = getGpuClock()
    # fan = getFanSpeed()
    # mm = getTotalMemory()
    # mu = getUsedMemory()
    # vc = getVramClock()
    # finish = time.perf_counter()
    # print(f"TIME FOR synchronous method!!!::: {finish - start}")
    return master

if __name__ == "__main__":
    fetch()