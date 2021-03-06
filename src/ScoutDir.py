# -*- coding: utf-8 -*- 

import shutil
from datetime import datetime,date,timedelta
from ctypes import *  
import os,re,sys
import time,glob
import string,winproc



def printHelloMsg():
    print("\n")
    print("           *                              ")
    print("                                          ")
    print("       *       *                          ")
    print("                                          ")
    print("           *                              ")
    print("Everything is going all right!       ")
    print("\n")


def ScoutDir(dicScoutDir,datetimeFromList,dicToGenerFiles,iPupProduct,lstLastestScoutTime):
   #    dir = "\\\\10.28.17.102\\rmdata2008\\mosaic\\latlon"
   
    iIndex = -1
    dirCur = "default"
#    print(dicScoutDir)
    #get scout file by orther progress
    if iPupProduct == 1:
        ScoutDirIndex(dicScoutDir,datetimeFromList,dicToGenerFiles,lstLastestScoutTime)
        return
    #else:
    #    IsDirWatchRunning(dicScoutDir,datetimeFromList,dicToGenerFiles,lstLastestScoutTime)
    #get latest file in scout dir
    dictRadar_C = {}
    for dirCur in dicScoutDir.keys():                
        try:
            #if dicScoutDir[dirCur] == 21 or dicScoutDir[dirCur] == 17:
             #  continue
            #if dirCur.endswith("\\") :
            NewDirCur = dirCur + "/"
            if not os.path.exists(NewDirCur):
                continue

            iIndex += 1
            datetimeMax = datetimeFromList[iIndex]
#            print("begin: ",NewDirCur,"  ",datetime.now())
            list=os.listdir(NewDirCur)
            #按创建时间排序
            #list.sort(key=lambda fn: os.path.getmtime(NewDirCur+fn) if not os.path.isdir(NewDirCur+fn) else 0,reverse=True)
            list.sort();
            list.reverse()
#            print("end: ",NewDirCur,"  ",datetime.now())
            
            iControl = 0
            print(NewDirCur,"   ",datetimeMax,"  fileFind:", len(list))
            for filename in list:
                iControl += 1
#                    if not filename.endswith(".latlon"):
#                         continue 
                if dicScoutDir[dirCur] == 17 and  iControl <= 1:
                    continue
                file = NewDirCur + filename            
#                    print(file) 
    #            datetimeCurFile = datetime.datetime.fromtimestamp(datetime.utcfromtimestamp(os.stat(file).st_mtime))
                timecurr = time.localtime(os.stat(file).st_mtime)
                datetimeCurFile =  datetime(timecurr.tm_year,timecurr.tm_mon,timecurr.tm_mday,timecurr.tm_hour,timecurr.tm_min,timecurr.tm_sec)
                if datetimeCurFile > datetimeFromList[iIndex]:
                    if datetimeMax < datetimeCurFile:
                        datetimeMax = datetimeCurFile
#                     print(file,datetimeCurFile,"    ",datetimeFromList)
                    if dicScoutDir[dirCur] == 102:
                        print(datetimeCurFile,"  ",datetimeFromList[iIndex],"   ",iIndex," ",file)

                    if dicScoutDir[dirCur] == 17:
                        dictRadar_C[file] = 17
                    else:
                        dicToGenerFiles[file] = dicScoutDir[dirCur]
                        
                    if datetimeFromList[iIndex] == datetime.min:
                        break 

                #elif dicScoutDir[dirCur] != 102:
                elif dicScoutDir[dirCur] != 102 :
                    break
        #update latest time of file
            datetimeFromList[iIndex] = datetimeMax
#            print("the latest time of ScoutOrther %s: "%dirCur) 

        except Exception as E:
            print("fail to read file from %s"%dirCur)
            continue
    #     logger.error(g_strHaveGeneratedSqlte3Path + strInfo)
  
    if len(dictRadar_C) > 0:
        timeNow = time.localtime() 
        file = "scoutdir/%02d%02d%02d.scout" % (timeNow.tm_hour,timeNow.tm_min,timeNow.tm_sec)
        fileHandle = open(file,'w')
        for dirCur in dictRadar_C.keys():
            fileHandle.write(dirCur)
            fileHandle.write("\n")
        fileHandle.close()
#    print(dicToGenerFiles)


# 获得一个目录及子目录下的最新文件
def getfilelist(latestFile,filepath, tabnum=1):
    
    simplepath = os.path.split(filepath)[1]
    returnstr = simplepath+"目录<>"+"\n"

    filelist = os.listdir(filepath)
    #print(filelist)
    for num in range(len(filelist)):
        filename=filelist[num]
        if os.path.isdir(filepath+"/"+filename):
            #print(filename)
            getfilelist(latestFile,filepath+"/"+filename)
            #returndirstr += "\t"*tabnum+getfilelist(filepath+"/"+filename, tabnum+1)
        else:
            files = os.listdir(filepath)
            #files.sort(compare)
            base_dir = filepath + "/"
            files.sort(key=lambda fn: os.path.getmtime(base_dir+fn) if not os.path.isdir(base_dir+fn) else 0)
            #print(files)
            latestFile[filepath] = files[len(files)-1]
            break
            #returnfilestr += "\t"*tabnum+filename+"\n"
    #returnstr += returnfilestr+returndirstr
    #return returnstr+"\t"*tabnum+"</>\n"



def updateMicapsData(totalDir,dictMicapsDir,newMicapsData):
    
    files = glob.glob("scoutdir/*.micaps")
    print(files)
    
    try:
        iControl = 0
        for file in files:
            
           iControl += 1
           fileHandler = open(file)
           for strLine in fileHandler.readlines():                 
   #            if(line.find("TITAN") == -1):
   #                continue
                strLine.replace("\\","/")
                if strLine.startswith("/"):
                    strLine = strLine[1:]
                
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


                
def IsDirWatchRunning(dicScoutDir,datetimeFromList,dicToGenerFiles,lstLastestScoutTime):
   #    dir = "\\\\10.28.17.102\\rmdata2008\\mosaic\\latlon"
   
    bFind = 0
    iIndex = 0
#    print(dicScoutDir)         

    scoutdir = os.getcwd() + "\scoutdir"
    list = os.listdir(scoutdir)
    
    #time.sleep(0.05)
    fileCur = ""
    dirCur = "default"
    iControl = 0
    
    try:
        for file in list:
            #print(file)
            iIndex += 1
            fileCur = scoutdir + "\\" + file
            if file.find(".scout") != -1:
                bFind = 1
                break
        
        if bFind == 0:
            print(time.time() - lstLastestScoutTime[0])
            if time.time() - lstLastestScoutTime[0] > 60*10:
                lstLastestScoutTime[0] = time.time()
                time.sleep(2)
                print("we will restart DirWatcher.exe")
                winproc.restart_pro("DirWatcher.exe")
        else:
            lstLastestScoutTime[0] = time.time()

    except Exception as E:
        print("Exception in ScoutDirIndex...")


def ScoutDirIndex(dicScoutDir,datetimeFromList,dicToGenerFiles,lstLastestScoutTime):
   #    dir = "\\\\10.28.17.102\\rmdata2008\\mosaic\\latlon"
   
    bFind = 0
    iIndex = 0
#    print(dicScoutDir)         

    scoutdir = os.getcwd() + "\scoutdir"
    list = os.listdir(scoutdir)
    
    #time.sleep(0.05)
    fileCur = ""
    dirCur = "default"
    iControl = 0
    
    #handle too much file
    if len(list) > 60:
        try:
            for file in list:
                fileCur = scoutdir + "\\" + file
                os.remove(fileCur)
        except Exception as E:
            print("Exception in handle to much file (maybe haven't the file's path in config.ini scoutdir)...")
       
        return
    
    
    try:
        for file in list:
            print(file)
            if file.endswith(".scout") == False:
                continue
            iIndex += 1
            fileCur = scoutdir + "\\" + file
            fileHandler = open(fileCur) 
            for newFile in fileHandler.readlines():
                newFile = newFile.rstrip("\n")
                if(os.path.exists(newFile) == False):
                    continue
                #print(newFile,os.path.dirname(newFile))
                dicToGenerFiles[newFile] = dicScoutDir[os.path.dirname(newFile)]
            fileHandler.close()           
            os.remove(fileCur)
            if(iIndex >= 3):
                break
        
    except Exception as E:
        print("Exception in ScoutDirIndex (maybe haven't the file's path in config.ini scoutdir)...")

       
       #     logger.error(g_strHaveGeneratedSqlte3Path + strInfo)
#    print(dicToGenerFiles)
    
def ClearTempFiles(picturePath,datetimeFromList,dayBeforeToday):
    
    def DeleteHistoryPicture(rootDir,dayBeforeToday):
        "recursion upate file from a root dir"
        iRet = -1
        print("DeleteHistoryPicture")
        if not os.path.isdir(rootDir):
            return iRet
        
     
        bHaveOld = None            
        for name in os.listdir(rootDir):

            try:       
                curFile = "%s/%s"%(rootDir,name)
                #you can't print file ,for it will got a error when it handle unicode char
#                 print("file",curFile)
                #juduge the file to delete or not by iKeepDay
                dtNow = datetime.now()
                timecurr = time.localtime(os.stat(curFile).st_ctime)
                datetimeCurFile =  datetime(timecurr.tm_year,timecurr.tm_mon,timecurr.tm_mday,timecurr.tm_hour,timecurr.tm_min,timecurr.tm_sec)
                datetimeCurFile +=  timedelta(days=dayBeforeToday)
                #print("os.stat(curFile).st_ctime"," histroyDay:",dayBeforeToday," days")
                if datetimeCurFile <= dtNow:
                    iRet = 1
                    #_100x100 all output file dir must suffix by _100x100,or it will be difficult to delete old pictures 
                    #print("DeleteHistoryPicture() compare -- curfile: ",datetimeCurFile,"dtNow:",dtNow)
                    if curFile.find("_100x100") != -1 and os.path.isdir(curFile):
                        print("will shutil.rmtree dir %s"%curFile)
                        shutil.rmtree(curFile) 
                        bHaveOld = True
    #                    elif os.path.isfile(curFile):
    #                        os.remove(curFile) 
    #                        bHaveOld = True
                    elif os.path.isdir(curFile):
#                         print("will remove dir %s"%curFile)
                        DeleteHistoryPicture(curFile,dayBeforeToday)   
            except Exception as E:
                print("shutil.rmtree(file:%s) exception:"%curFile,E)                   
    
        return iRet
  
                     
    #notice

    def DeleteHistoryFiles(rootDir,dayBeforeToday):
        "recursion upate file from a root dir"
        iRet = -1
        if not os.path.isdir(rootDir):
            return iRet
          
        bHaveOld = None
        for name in os.listdir(rootDir):

            try:    
                curFile = "%s/%s"%(rootDir,name)
#                 print("file",curFile)
                #juduge the file to delete or not by iKeepDay
                dtNow = datetime.now()
                timecurr = time.localtime(os.stat(curFile).st_ctime)
                datetimeCurFile =  datetime(timecurr.tm_year,timecurr.tm_mon,timecurr.tm_mday,timecurr.tm_hour,timecurr.tm_min,timecurr.tm_sec)
                datetimeCurFile +=  timedelta(days=dayBeforeToday)
                if datetimeCurFile <= dtNow:
                    iRet = 1
                    #_100x100 all output file dir must suffix by _100x100,or it will be difficult to delete old pictures 
#                     print("curfile: ",datetimeCurFile,"dtNow:",dtNow)
                    if os.path.isfile(curFile):
                        if not curFile.endswith(".db"):
#                             print("removing file %s"%curFile)
                            os.remove(curFile) 
#                             print("removed file %s"%curFile)
                        bHaveOld = True
                    elif os.path.isdir(curFile):
#                         print("will remove dir %s"%curFile)
                        DeleteHistoryFiles(curFile,dayBeforeToday)   
    #                        DeleteHistoryPicture(curFile,dayBeforeToday)                    
    
            except Exception as E:
                print("os.remove(file:%s) exception:"%curFile,E)    
        return iRet

                     
    #notice

    iRet = 0
    currentTime = datetime.now()
    print(currentTime)
    #notice
    bTest = False
    print(currentTime.year ,currentTime.month,currentTime.day)
    if currentTime.year == 2014 and currentTime.month == 8 and currentTime.day == 15:
        bTest = True
    if currentTime.hour > 3 and bTest == False:
        return iRet
    #clear the temp data file
#    dirList = os.listdir("%s\\temp\\"%os.getcwd())
#    print(dirList) 

    try:
        print("clear temp folder:%s\\temp"%os.getcwd())
        shutil.rmtree("%s\\temp"%os.getcwd()) 
    except Exception as E:
        print("windows clear  temp folder failed",E)
             
#    return iRet
#    for str in dirList:
#        file = "%s\\temp\\%s"%(os.getcwd(),str)            
#        timecurr = time.localtime(os.stat(file).st_ctime)
#        datetimeCurFile =  datetime(timecurr.tm_year,timecurr.tm_mon,timecurr.tm_mday,timecurr.tm_hour,timecurr.tm_min,timecurr.tm_sec)
#        datetimeCurFile +=  timedelta(days=dayBeforeToday)
#        if datetimeCurFile <= datetimeFromList[0]:
#            os.remove(file)
    
    #clear the picture  and update the sqlite3 db
    iRet = DeleteHistoryFiles("%s\\Office2SWF"%picturePath,dayBeforeToday)
    iRet = DeleteHistoryPicture(picturePath,dayBeforeToday)
    return iRet 

if __name__ == '__main__':

    datetimeFrom = datetime(2012,4,10,15,9)
    datetimeFrom = datetime.now()
    datetimeFrom = datetimeFrom + timedelta(hours = -1)
    datetimeFromList = []
    datetimeFromList.append(datetimeFrom)
    datetimeFromList.append(datetimeFrom)
    dir = "\\\\10.28.17.102\\rmdata2008\\mosaic\\latlon"
    dicDir = {}
    dic = {}
#    dicDir[dir] = 14
    dicDir["D:\\work\\AIW\\testdata北京\\cloud"] = 18
#    ScoutDir(dicDir,datetimeFromList,dic)
    print(dic)
#    ClearTempFiles("F:\\Output1",datetimeFromList,1)
    
    rootdir = "E:\Webmicaps\webapps\output\output\CAPPI"
    rootdir = "C:\\aaa\\output"
    
    historyDay = 0
    if  len(sys.argv) == 2:
        rootdir = sys.argv[1]
        historyDay = int(sys.argv[2])
    
    print("argc:",len(sys.argv),rootdir,historyDay,".................")
    ClearTempFiles(rootdir,datetimeFromList,historyDay)
    print("clear over")
