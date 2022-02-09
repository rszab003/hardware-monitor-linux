import init, CpuData, NvidiaGpuData, RamData, MotherboardData
import concurrent.futures


def executeThreads() -> list:
    with concurrent.futures.ThreadPoolExecutor() as thread:
        results = []
        results.append(thread.submit(CpuData.fetch))
        results.append(thread.submit(NvidiaGpuData.fetch))
        results.append(thread.submit(RamData.getRamData))
        results.append(thread.submit(MotherboardData.fetch))
    return results


def main():
    init.createTempFS()
    allData = executeThreads()

    for x in allData:
        print(x.result())
        print("*" * 30)
    # print(boardBiosData)



if __name__ == "__main__":
    main()