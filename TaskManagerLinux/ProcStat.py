import os, sys, glob, time
import psutil

class ProcStat():
    def __init__(self):
        self.strCPUInfo = ""
        self.strOSInfo  = ""
        self.strCPUStat = ""
        self.strMeminfo = ""

        self.strProcs = []


    def __openFiles(self):
        try:
            self.fileCPUInfo = open("/proc/cpuinfo")
            self.fileOSInfo  = open("/proc/version")
            self.fileCPUStat = open("/proc/stat")
            self.fileMeminfo = open("/proc/meminfo")
            self.fileModinfo = open("/proc/modules")
            # self.fileDiskinfo = open("proc/")

            self.fileProcs   = []
            globFiles = glob.glob("/proc/*")
            for fileProc in globFiles:
                if fileProc.split("/")[-1].isdigit():
                    fileCur = open(fileProc + "/stat")
                    self.fileProcs += [fileCur]

        except:
            print ("Exception: ProcStat.__openFiles()")
            print (sys.exc_info())
            time.sleep(0.1)
            self.__openFiles()


    def __readFiles(self, CPUStat = False):
        try:
            self.__openFiles()
            self.strCPUStat = self.fileCPUStat.read()

            # if CPUStat == True, means this request is for refresh cpu usage
            # the files below need not to reread
            if CPUStat == False:
                self.strCPUInfo = self.fileCPUInfo.read()
                self.strOSInfo  = self.fileOSInfo.read()
                self.strMeminfo = self.fileMeminfo.read()
                self.strModules = self.fileModinfo.read()

                self.strProcs = []
                for fileProc in self.fileProcs:
                    self.strProcs += [fileProc.read()]
            self.__closeFiles()

        except:
            print ("Exception: ProcStat.__readFiles()")
            print (sys.exc_info())
            time.sleep(0.1)
            self.__readFiles()


    def __closeFiles(self):
        try:
            self.fileCPUInfo.close()
            self.fileOSInfo.close()
            self.fileCPUStat.close()
            self.fileMeminfo.close()

            for fileProc in self.fileProcs:
                fileProc.close()
        except:
            print ("Exception: ProcStat.__closeFiles()")
            print (sys.exc_info())


    def getCPUInfo(self):
        if len(self.strCPUInfo) < 2:
            self.__readFiles()

        cpuinfo = {}
        listCPUInfo = self.strCPUInfo.split("\n")
        for x in range(0, len(listCPUInfo) - 1):
            if len(cpuinfo) == 3:
                break
            info = listCPUInfo[x].split("\t: ")
            if info[0].find("model name") != -1:
                cpuinfo.update({"name":info[1]})
                continue
            if info[0].find("vendor_id") != -1:
                cpuinfo.update({"type":info[1]})
                continue
            if info[0].find("cpu MHz") != -1:
                cpuinfo.update({"frequency":info[1]})
                continue
        return cpuinfo


    def getOSInfo(self):
        if len(self.strOSInfo) < 2:
            self.__readFiles()
        osinfo = {}
        listOSInfo = self.strOSInfo.rsplit(")", 1)[0].replace("gcc version", "gccver").split()
        #1. delete the building time information, which is after the last ")"
        #2. replace "gcc version" to "gccversion", this can avoid "gcc version" splits to 2 parts
        #3. split the string
        ostype = listOSInfo[0]
        osinfo.update({"type":ostype})
        for x in range(0, len(listOSInfo)):
            if len(osinfo) == 3:
                break;
            if listOSInfo[x].find("version") != -1:
                osver = listOSInfo[x + 1]
                if listOSInfo[x + 2].find("build") != -1:
                    osver += listOSInfo[x + 2]
                osinfo.update({"version":osver})
                continue
            if listOSInfo[x].find('gccver') != -1:
                gccver = " ".join(listOSInfo[x + 1:])
                osinfo.update({"GCCversion":gccver})
                continue
        return osinfo


    def getMemInfo(self):
        if len(self.strMeminfo) < 2:
            self.__readFiles()

        meminfo = {}
        listMemInfo = self.strMeminfo.split("\n")
        for x in range(0, len(listMemInfo)):
            if len(meminfo) == 4:
                break
            info = listMemInfo[x].split(":")
            if info[0].find("MemTotal") != -1:
                meminfo.update({"MemTotal":info[1].strip()})
                continue
            if info[0].find("MemFree") != -1:
                meminfo.update({"MemFree":info[1].strip()})
                continue
            if info[0].find("SwapTotal") != -1:
                meminfo.update({"SwapTotal":info[1].strip()})
                continue
            if info[0].find("SwapFree") != -1:
                meminfo.update({"SwapFree":info[1].strip()})
                continue
        return meminfo


    def getProcInfos(self):
        if len(self.strProcs) < 2:
            self.__readFiles()

        procinfos = []
        total     = 0
        runnable  = 0
        sleeping  = 0
        defunct   = 0
        total_thread = 0
        for x in range(0, len(self.strProcs)):
            procinfo = self.strProcs[x].split()
            try:
                p = psutil.Process(int(procinfo[0]))#pid
                # cpu_percent = p.cpu_percent()
                username = p.username()
                meminfo = p.memory_info()
                mem_percent = p.memory_percent()
                total_thread += p.num_threads()

                # print(cpu_percent)
                procinfos += [{"pid":procinfo[0], "name":procinfo[1][1:-1].ljust(20), "status":procinfo[2],"ppid":procinfo[3], "priority":procinfo[17], "virt":meminfo[1],"username":username,"res":meminfo[0],"shr":meminfo[2],"mem_percent":mem_percent}]
            except:
                procinfos += [{"pid":procinfo[0], "name":procinfo[1][1:-1].ljust(20), "status":procinfo[2],"ppid":procinfo[3], "priority":procinfo[17], "virt":"0","username":"0","res":0,"shr":0,"mem_percent":0}]
            total += 1
            if procinfo[2] == "R":
                runnable += 1
                continue
            if procinfo[2] == "S":
                sleeping += 1
                continue
            if procinfo[2] == "Z":
                defunct += 1
                continue

        procstat = {"Total":total, "Runnable":runnable, "Sleeping":sleeping, "Defunct":defunct,"Thread":total_thread}

        return [procinfos, procstat]
    # def getProcInfosDetailed(self):
    #     if len(self.strProcs) < 2:
    #         self.__readFiles()

    #     procinfos = []
    #     # total     = 0
    #     # runnable  = 0
    #     # sleeping  = 0
    #     # defunct   = 0
    #     for x in range(0, len(self.strProcs)):
    #         procinfo = self.strProcs[x].split()
    #         # print(procinfo)
    #         p = psutil.Process(int(procinfo[0]))#pid
    #         cpu = p.cpu_percent(interval = 1.0)
    #         # print(cpu)
    #     return procinfos

    def getModuleInfos(self):
        if len(self.strModules) < 2:
            self.__readFiles()

        moduleinfos = []
        total       = 0
        listModInfo = self.strModules.strip("\n").split("\n")
        for x in range(0, len(listModInfo)):
            modinfo = listModInfo[x].split()
            moduleinfos += [{"name":modinfo[0], "memory":modinfo[1], "usage":modinfo[2]}]
            total += 1
        return [moduleinfos, total]


    def getCPUStat(self, gapTime = 0.1):
        if len(self.strCPUStat) < 2:
            self.__readFiles()

        cpustats = []
        listCPUStat = self.strCPUStat.strip("\n").split("\n")
        for x in range(0, len(listCPUStat)):
            listTime = listCPUStat[x].split()
            if listTime[0].find("cpu") < 0:
                break
            # calculate the usage of CPU
            # usage = (busy1 - busy0) / (total1 - total0)
            cpuStat0 = {listTime[0]:str(sum([int(i) for i in listTime[1:-1]])),
                        "busy":str(sum([int(i) for i in listTime[1:4]]))}
            #print "cpu:" + cpuStat0[listTime[0]] + " busy:" + cpuStat0["busy"] + "\n"
            time.sleep(gapTime) # wait for gapTime
            self.__readFiles(True) # reread the stat file
            listCPUStat = self.strCPUStat.split("\n")
            listTime = listCPUStat[x].strip("\n").split()
            cpuStat1 = {listTime[0]:str(sum([int(i) for i in listTime[1:-1]])),
                        "busy":str(sum([int(i) for i in listTime[1:4]]))}
            #print "cpu:" + cpuStat1[listTime[0]] + " busy:" + cpuStat1["busy"] + "\n"
            if cpuStat0[listTime[0]] == cpuStat1[listTime[0]]:
                cpuUsage = 0
            else:
                cpuUsage = ((float(cpuStat1["busy"]) - float(cpuStat0["busy"])) /
                           (float(cpuStat1[listTime[0]]) - float(cpuStat0[listTime[0]])))

            cpustats += [{listTime[0]:str(sum([int(i) for i in listTime[1:-1]])),
                          "busy":str(sum([int(i) for i in listTime[1:4]])),
                          "usage":str(cpuUsage)}]

        total_util = psutil.cpu_stats()
        totalcpustats ={"ctx_switches":total_util[0],"interrupts":total_util[1],"soft_interrupts":total_util[2],"sys_call":total_util[3]}
        return [cpustats,totalcpustats]


    def refresh(self):
        self.__readFiles()



if __name__ == "__main__":
    procRead = ProcStat()
    cpuinfo  = procRead.getCPUInfo()
    meminfo  = procRead.getMemInfo()
    osinfo   = procRead.getOSInfo()
    procinfo = procRead.getProcInfos()
    modinfo  = procRead.getModuleInfos()
    cpustat,totalcpustats  = procRead.getCPUStat()
    # test = procRead.getProcInfosDetailed()
    # print(cpustat)
    # print(totalcpustats)
    # # print(osinfo)
    print(procinfo)
    # print(test)
    # print(cpustat)
