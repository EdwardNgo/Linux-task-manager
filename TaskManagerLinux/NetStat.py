import psutil

class NetStat:
    def __init__(self):
        pass
    def getNetIOCounters(self):
        net_io_counters = psutil.net_io_counters()
        net_dict = {"bytes_sent":net_io_counters[0],"bytes_recv":net_io_counters[1],"packets_sent":net_io_counters[2],"packets_recv":net_io_counters[3]}
        return net_dict
    # def refresh(self):
    #     self.getNetIOCounters(self)

if __name__ == "__main__":
    myNet = NetStat()
    print(myNet.getNetIOCounters())
