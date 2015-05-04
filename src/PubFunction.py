# the public function

import os,sys,time
import ctypes,socket


def CanConnectPort(port):
    line = port
    ip = "localhost"
    try:
        sc=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        #set timeout time
        sc.settimeout(2)
        sc.connect((ip,port))
        timenow=time.localtime()
        datenow = time.strftime('%Y-%m-%d %H:%M:%S', timenow)
        logstr="%s:%s connect successfully->%s \n" %(ip,port,datenow)
        print(logstr)
        sc.close()
        return True
    except:
#        file = open("log.txt", "a")
        timenow=time.localtime()
        datenow = time.strftime('%Y-%m-%d %H:%M:%S', timenow)
        logstr="%s:%s connect failedd->%s \n" %(ip,port,datenow)
        print(logstr)
        return False
#        file.write(logstr)
#        file.close()


def MakeDir(strDir):
    "recursion makedir"
    strDir = strDir.replace("\\","/")
    list = strDir.split("/")
    if len(list) <= 1:
        return
    
    curPath = list[0]
    for index,dir in enumerate(list):
        if index == 0:continue
        curPath = "%s/%s"%(curPath,dir)
        if not os.path.exists(curPath):
            os.mkdir(curPath)
    
    print(strDir,list)

def Hide_UI():
    
    #import ctypes  
    whnd = ctypes.windll.kernel32.GetConsoleWindow()  
    if whnd != 0:  
        ctypes.windll.user32.ShowWindow(whnd, 0)  
        ctypes.windll.kernel32.CloseHandle(whnd) 

if __name__ == "__main__":
    
    print("pubfunction is testing....")
    strDir = "D:\\work\\AIW\\testdata"
    #UpdateFileRecursion(strDir)
    listdir_ctime(os.curdir)