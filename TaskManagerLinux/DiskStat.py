import psutil
class DiskStat:
    def __init__(self):
        pass
    def getDiskInfo(self):
        partition = psutil.disk_partitions()
        usage = psutil.disk_usage('/')
        usage_dict = {"total": round(usage[0]/1024**3),"usage": round(usage[1]/1024**3),"free": round(usage[2]/1024**3)}
        return usage_dict

    def getIOCounters(self):
        io_counters = psutil.disk_io_counters()
        io_counters_dict = {"total_reads":io_counters[0],"total_writes":io_counters[1],"read_bytes":io_counters[2],"write_bytes":io_counters[3]}
        return io_counters_dict

if __name__ == '__main__':
    myDisk = DiskStat()
    print(myDisk.getDiskInfo())
    print(myDisk.getIOCounters())
