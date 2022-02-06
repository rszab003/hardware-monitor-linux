import init, CpuData, NvidiaGpuData, RamData, MotherboardData

def main():
    init.createTempFS()
    
    cpuData = CpuData.fetch()
    print(cpuData)
    print("*" * 30)

    gpuData = NvidiaGpuData.fetch()
    print(gpuData)

    print("*" * 30)
    ramData = RamData.getRamData()
    print(ramData)

    print("*" * 30)
    boardBios = MotherboardData.fetch()
    print(boardBios)

    


if __name__ == "__main__":
    main()