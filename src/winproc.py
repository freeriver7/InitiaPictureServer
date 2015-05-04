
# -------------------------winproc.py-------------------------------

import ctypes,subprocess
import sys,time

TH32CS_SNAPPROCESS = 0x00000002
class PROCESSENTRY32(ctypes.Structure):
     _fields_ = [("dwSize", ctypes.c_ulong),
                 ("cntUsage", ctypes.c_ulong),
                 ("th32ProcessID", ctypes.c_ulong),
                 ("th32DefaultHeapID", ctypes.c_ulong),
                 ("th32ModuleID", ctypes.c_ulong),
                 ("cntThreads", ctypes.c_ulong),
                 ("th32ParentProcessID", ctypes.c_ulong),
                 ("pcPriClassBase", ctypes.c_ulong),
                 ("dwFlags", ctypes.c_ulong),
                 ("szExeFile", ctypes.c_char * 260)]

def getProcList():
    CreateToolhelp32Snapshot = ctypes.windll.kernel32.CreateToolhelp32Snapshot
    Process32First = ctypes.windll.kernel32.Process32First
    Process32Next  = ctypes.windll.kernel32.Process32Next
    CloseHandle    = ctypes.windll.kernel32.CloseHandle
    hProcessSnap   = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
    pe32 = PROCESSENTRY32()
    pe32.dwSize = ctypes.sizeof(PROCESSENTRY32)
    if Process32First(hProcessSnap,ctypes.byref(pe32)) == False:
        print("Failed getting first process.", file=sys.stderr)
        return
    while True:
        yield pe32
        if Process32Next(hProcessSnap,ctypes.byref(pe32)) == False:
            break
    CloseHandle(hProcessSnap)

def getChildPid(pid):
    procList = getProcList()
    for proc in procList:
        if proc.th32ParentProcessID == pid:
            yield proc.th32ProcessID
   
def killPid(pid):
    childList = getChildPid(pid)
    for childPid in childList:
        killPid(childPid)
    handle = ctypes.windll.kernel32.OpenProcess(1, False, pid)
    ctypes.windll.kernel32.TerminateProcess(handle,0)

def restart_pro(name):
    procList = getProcList()
    for proc in procList:
        if str(proc.szExeFile)[2:-1] == name:
            print("restart",proc.th32ProcessID," ",name)
            killPid(proc.th32ProcessID)
            break
    subprocess.Popen([name]) 
    
def kill_pro(name):
    procList = getProcList()
    for proc in procList:
        if str(proc.szExeFile)[2:-1] == name:
            print("stop proc: ",proc.th32ProcessID," ",name)
            killPid(proc.th32ProcessID)
            break


def IsProcStarted(name):
    procList = getProcList()
    for proc in procList:
       # print(str(proc.szExeFile)[2:-1])
        if str(proc.szExeFile)[2:-1] == name:
            #print(str(proc.szExeFile)[2:-1]," is running... ")
            return True
    print("not found....",name)
    return False 

    
if __name__ =='__main__':
    args = sys.argv
    if len(args) >1 :
        pid = int(args[1])
        killPid(pid)
    else:
        procList = getProcList()
        name = "DirWatcher.exe"
        for proc in procList:
            if str(proc.szExeFile)[2:-1] == name:
                restart_pro(name)
            print(str(proc.szExeFile)+'  '+str(proc.th32ParentProcessID) + '  '+str(proc.th32ProcessID))
   