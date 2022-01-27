import init, CpuData

def main():
    init.createTempFS()

    CpuData.cpuInfo()
    init.determineCpuTempDirectory()
    CpuData.getCpuTemp()
    CpuData.getUsage()
    print("*" * 30)
    print(CpuData.master)

if __name__ == "__main__":
    main()