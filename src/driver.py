import math
import parts.CpuData as CpuData, parts.NvidiaGpuData as NvidiaGpuData, parts.RamData as RamData, parts.MotherboardData as MotherboardData
import concurrent.futures
import sys
from time import sleep, perf_counter
from json import dump

USAGE = "python3 driver.py -r (float)"
MANIFEST = "/tmp/openhwmon_linux/manifest.json"

def executeThreads() -> list:
    # parts.createTempFS()
    with concurrent.futures.ThreadPoolExecutor() as thread:
        results = []
        results.append(thread.submit(CpuData.fetch))
        results.append(thread.submit(NvidiaGpuData.fetch))
        results.append(thread.submit(RamData.fetch))
        results.append(thread.submit(MotherboardData.fetch))
    return results


def main():
    # UNCOMMENT for ONE-TIME display of Data
    
    # allData = executeThreads()
    # for x in allData:
        # print(x.result())
        # print("*" * 30)
    # print(len(argv))
    if len(sys.argv) != 3:
        print("INCORRECT USAGE !")
        print("USAGE:", USAGE)
        print(f"LENARGS::: {len(sys.argv)}")
        exit(-1)
    else:
        if sys.argv[1] == "-r":
            print("REPEAT!!")
            if sys.argv[2] != None:
                try:
                    delay = float(sys.argv[2])
                except ValueError as ex:
                    print(ex)
                    print("Please provide a number for the delay")
                    exit(-1)
            try:
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
                        data = x.result()
                        if type(data) == dict:
                            exp[data["BaseName"]] = data
                        elif type(data) == list:
                            exp[data[0]["BaseName"]] = data
                    
                    #Add/remove comment to see output in console
                    print("EXPORT TO JSON!! {}".format(exp))
                    
                    with open(MANIFEST, "w") as outFile:
                        dump(exp, outFile, indent=3)
                    try: #in case refresh arg is too low
                        sleep(delay - delta)
                        # print(f"Sleeping for: {delay - delta} sec")
                    except ValueError:
                        sleep(math.ceil(delta) - delta)
                        # print(f"Sleeping for: {math.ceil(delta) - delta} sec")
            except KeyboardInterrupt:
                print("ABORTING...")
                exit(1)
        else:
            print("INCORRECT USAGE!\n{}".format(USAGE))
    # print(boardBiosData)



if __name__ == "__main__":
    main()
