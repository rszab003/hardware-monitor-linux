import init, CpuData, NvidiaGpuData, RamData, MotherboardData
import concurrent.futures
from sys import argv
from time import sleep, perf_counter
from json import dump

#USAGE: python3 main.py -r (float)


MANIFEST = "/tmp/openhwmon_linux/manifest.json"

def executeThreads() -> list:
    init.createTempFS()
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

    # for i in allData[0].result().values():
    #     print(i)

    # for x in allData:
        # print(x.result())
        # print("*" * 30)
    
    if len(argv) > 1 and len(argv) < 4:
        if argv[1] == "-r":
            print("REPEAT!!")
            if argv[2] != None:
                try:
                    delay = float(argv[2])
                except ValueError as ex:
                    print(ex)
                    print("Please provide a number for the delay")
                    exit(-1)
            while True:
                start = perf_counter()
                allData = executeThreads()
                end = perf_counter()
                delta = end - start
                print("GOT DATA IN::: {}".format(delta))
                exp = {}
                for idx, x in enumerate(allData):
                    # print(x.result())
                    # print("*" * 30)
                    exp[idx] = x.result()
                
                print("EXPORT TO JSON!! {}".format(exp))
                
                with open(MANIFEST, "w") as outFile:
                    dump(exp, outFile, indent=3)
                
                sleep(delay - delta)
    # print(boardBiosData)



if __name__ == "__main__":
    main()