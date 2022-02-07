from asyncio import futures
import init, CpuData, NvidiaGpuData, RamData, MotherboardData
import time, concurrent.futures


def testWithThreading():
    start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor() as exe:
        results = []
        results.append(exe.submit(CpuData.fetch))
        results.append(exe.submit(NvidiaGpuData.fetch))
        results.append(exe.submit(RamData.getRamData))
        results.append(exe.submit(MotherboardData.fetch))
        finish = time.perf_counter()
        # for f in concurrent.futures.as_completed(results):
        #     print(f.result())
    print(f"FINISHED IN {finish - start} SEC WITH THREADING!!!")


def main():
    start = time.perf_counter()
    init.createTempFS()
    
    cpuData = CpuData.fetch()
    # print(cpuData)
    # print("*" * 30)

    gpuData = NvidiaGpuData.fetch()
    # print(gpuData)
    # print("*" * 30)

    ramData = RamData.getRamData()
    # print(ramData)
    # print("*" * 30)
    
    boardBios = MotherboardData.fetch()
    finish = time.perf_counter()
    print(f"{cpuData}\n{gpuData}\n{ramData}\n{boardBios}\nFINISHED IN {finish - start} SECONDS SYNCHRONOUSLY!!!")

    testWithThreading()
    # print(boardBios)

    


if __name__ == "__main__":
    main()