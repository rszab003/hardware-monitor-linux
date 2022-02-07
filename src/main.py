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
    # start = time.perf_counter()
    # init.createTempFS()
    # with concurrent.futures.ThreadPoolExecutor() as thread:
    #     if not exists("/tmp/openhwmon_linux"):
    #         thread.submit(init.createTempFS)
    #     cpuData = thread.submit(CpuData.fetch)
    #     gpuData = thread.submit(NvidiaGpuData.fetch)
    #     ramData = thread.submit(RamData.getRamData)
    #     boardBiosData = thread.submit(MotherboardData.fetch)
    # finish = time.perf_counter()
    init.createTempFS()
    cpuData = CpuData.fetch()
    print(cpuData)
    # print(cpuData.result())
    # print("*" * 30)
    # print(gpuData.result())
    # print("*" * 30)
    # print(ramData.result())
    # print("*" * 30)
    # print(boardBiosData.result())
    # print("DATA RETREIVED IN::: {}".format(finish - start))
    # testWithThreading()


if __name__ == "__main__":
    main()