
import os,re,sys
import watcher,random,glob
import time
import threading
import sys, os,time


micapsDir = ""
swanDir = ""
latestFiles = []
timeLatestFile = time.time()
latestFiles_swan = []
timeLatestFile_swan = time.time()

secondsRestartTime = 60*5 #we will restart scout system ,if there is no new file in 60*20 seconds 

def handle(*args):
    global latestFiles
    global timeLatestFile
    
    if args[0] != 1:
        return 
    
    #if mutex.acquire(1):  
    latestFiles.append(args[1])
     #   mutex.release()
    #mutex.acquire([10])

    print(args[1],"   ",len(latestFiles))
    #latestFiles = []
 #   return

    if len(latestFiles) < 50:
        return
    
    timeNow = time.localtime() 
    timeLatestFile = time.time()
    file = "scoutdir/%02d%02d%02d.micaps" % (timeNow.tm_hour,timeNow.tm_min,timeNow.tm_sec)
    print(file)
    
    fileHandle = open(file,'w')
    for key in latestFiles:
        fileHandle.write("%s\n"%(key))
    fileHandle.close()
    
    
    #if mutex.acquire(1):  
    latestFiles = []
     #   mutex.release()
        
    #print("program exit...")

        
    return


def handle_swan(*args):
    
    global latestFiles_swan
    global timeLatestFile_swan
    
    if args[0] != 1:
        return 
    
    #if mutex.acquire(1):  
    latestFiles_swan.append(args[1])
     #   mutex.release()
    #mutex.acquire([10])

    print(args[1],"   ",len(latestFiles_swan))
    #latestFiles_swan = []
 #   return

    if len(latestFiles_swan) < 50:
        return
    
    timeNow = time.localtime() 
    timeLatestFile_swan = time.time()
    file = "scoutdir/swan%02d%02d%02d.micaps" % (timeNow.tm_hour,timeNow.tm_min,timeNow.tm_sec)
    print(file)
    
    fileHandle = open(file,'w')
    for key in latestFiles_swan:
        fileHandle.write("%s\n"%(key))
    fileHandle.close()
    
    
    #if mutex.acquire(1):  
    latestFiles_swan = []
     #   mutex.release()
        
    #print("program exit...")

        
    return


#    fsw = FileSystemWatcher("c:/aaa/output")
     #dir = "c:/aaa/output"
    
def initializeConfig():   
    global micapsDir
    global swabDir
            #print("the work dir is %s"%os.getcwd())
    file = open("ServerConfig.ini")
    dictTest = {"X:/data/newecmwf_grib/height/850":"","X:/data/newecmwf_grib/height/925":"","X:/data/newecmwf_grib/u/850":""}
    
    '''
    g_micapsLatestFile = dictTest
    g_micapsLatestFileNew = {}
    g_micapsDir = "X:/data/"
    updateMicapsData(g_micapsDir,g_micapsLatestFile,g_micapsLatestFileNew)
    updateSqlite3("")
    '''
    
    
    for line in file.readlines():
       
        listDir = []
        
        line = line.strip()
        if not line or line[0] == '#' or line[0] == '[':
            #print(line)
            continue
            
        list = line.split("=")        
        if list[0].strip().lower() == "Total".lower():
             listServer = list[1].strip().split(";")
             totalDir = listServer[0] if len(listServer) > 0 else ""
             swanDir  = listServer[0] if len(listServer) > 0 else ""
          
             if totalDir.endswith("\\") or totalDir.endswith("/"):
                 totalDir = totalDir[0:-1] 
             if totalDir.startswith("\""):
                 totalDir = totalDir[1:] 

             if swanDir.endswith("\\") or swanDir.endswith("/"):
                 swanDir = swanDir[0:-1] 
             if swanDir.startswith("\""):
                 swanDir = swanDir[1:] 
             #totalDir = "X:/data/newecmwf_grib"
             micapsDir = totalDir
             break
    file.close()




def startScout(dir):
    
    global latestFiles
    global timeLatestFile
    #dir = "C:/aaa/output"
    #dir = "N:/micapsdata"
    #print("startScout :%s\n"%dir)
    
    
    try:
        os.listdir(dir)
        print("list  :%s successfully\n"%dir)
        #w.recursive()
    except WindowsError as E:
        print("the dir is not exist...")
        time.sleep(1)
        return
    
    w = watcher.Watcher(dir, handle)
    #w.flags = watcher.FILE_NOTIFY_CHANGE_FILE_NAME
    w.flags = watcher.FILE_NOTIFY_CHANGE_CREATION | watcher.FILE_NOTIFY_CHANGE_FILE_NAME
    w.recursive=True
    #print("program start...")
    #return
    
    try:
        w.start()
        #w.recursive()
    except WindowsError as E:
        strInfo = str(E)
        print("net cann't connect error...",strInfo)
        time.sleep(1)
    #        logger.error(g_strHaveGeneratedSqlte3Path + strInfo)

    finally:
        print("try except finnally in startScout function...")

    while True:
        
        time.sleep(5)
        #isWatcherRunning()
        delta = time.time()-timeLatestFile
        if delta > secondsRestartTime:
            print("The net cann't be connected  in seconds : ",delta)
            sys.exit()
            w.stop()
            break
        #time.sleep(60*60*24)
    #return


def isWatcherRunning(totalDir,dictMicapsDir,newMicapsData):
    
    files = glob.glob("scoutdir/*.micaps")
    files.sort(reverse=True)
    print(files[0])
    
 


def updateMicapsData(totalDir,dictMicapsDir,newMicapsData):
    
    files = glob.glob("scoutdir/*.micaps")
    print(files)
    
    try:
        iControl = 0
        for file in files:
            
           iControl += 1
           fileHandler = open(file)
           for line in fileHandler.readlines():                 
   #            if(line.find("TITAN") == -1):
   #                continue
               strLine = line.replace("\\","/")
               iPos = strLine.rfind("/")
               if iPos == -1: 
                   
                   continue

   #            print(iPos0,fileDetailType)
               key = strLine[0:iPos]
               value = strLine[iPos + 1:len(strLine)- 1]
               newMicapsData[key] = value
               
           fileHandler.close()
           os.remove(file)
    except Exception as E:
       print("open index file failed",E)




mutex = threading.Lock()

if __name__ == '__main__':

    dir = "C:/aaa/output"
    dir = "N:/micapsdata"
    
    initializeConfig()
    dir = micapsDir
#     files = glob.glob("scoutdir/*.micaps")
#     print(files)

    '''
    dict1 = {}
    dict2 = {}
    updateMicapsData("",dict1,dict2)
    '''
    
    #startScout(dir)

    while True:
        #time.sleep(1)
        print("begin call startScout dir...")
        startScout(dir)

