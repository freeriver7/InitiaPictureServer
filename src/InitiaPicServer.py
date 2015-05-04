# -*- coding: utf-8 -*-  

from ScoutDir import *
from ctypes import *
from datetime import datetime, date, timedelta
import PubFunction
import MyFtp
import UserStruct
import _hInitiativePic
import os,copy
import sys,re
import threading
import sqlite3
import string
import time,subprocess
import OfficeStart
from ScoutDirEx import InitiaMicaps
#import win32ui
#import win32api
#import win32con


#import logging
#import logging.config
'''
filetype:
1-100  all micaps or meteorology data
101  基数据的exe处理，临时使用
102  word pdf的产品制作类型
'''

#LOG_FILENAME = 'logging.conf'
#logging.config.fileConfig(LOG_FILENAME)
#logger = logging.getLogger("simple_log_example")

#dllfile = "PictureFactoryPlugin.dll"
#print(dllfile)
#dll = CDLL(dllfile)  
dll = CDLL("PictureFactoryPlugin_Int.dll")  
#dll = CDLL("PictureFactoryPlugin_Pup.dll")  
g_iPupProduct = 0
g_dictScoutDirOutPutSelf = {}
g_dictScoutDirScale = {}
g_listZhidaoChanpin  = []
g_dictScoutDirLwfd = {}
g_strPrdIndexFile = ""
g_strPrdIndexFileTemp = "" #记录上次处理的是哪个txt文件
g_strScoutFileDir  = ""
g_strPicSaveDir = ""
g_strCappiLevels = ""
g_strSWFToolsPath = ""
g_strSWFOutput = ""
g_micapsDir = "";
g_micapsLatestFile ={}
g_micapsLatestFileNew ={}
g_strSOffice = "default"
g_strHaveGeneratedSqlte3Path = ""
g_timeRadarUnit = 0
g_lstInitiaType = []
datetimeFromList = []
g_dictInitiaType ={}
g_dictInitiaGenFile = {}
g_dictNotInitiaGenFile = {}
dicProductTypeMap = {}
g_dicScoutOrtherFileDir  = {}
g_listPhoneServer = []
g_listLastestFile = []
iKeepPicDayNum = 1
g_iExecuteTimes = 0
g_dResolution = -1.0
g_iTransparent = 128
g_lstLatestScourFindFile =  [time.time()]
g_datetimeSwanIndex = datetime.now()
g_datetimeSwanIndex = datetime.min 

#datetimeFrom = datetime(2012,4,11,7,9)
datetimeFrom = datetime.now()
datetimeFrom = datetimeFrom + timedelta(minutes = -30)
#datetimeFrom = datetimeFrom + timedelta(hours = -10)
datetimeFromList.append(datetimeFrom)
datetimeFromList.append(datetimeFrom)
#fileHandle = open("log.txt",'w')
listFtp = []

def InitiaConfig():
    global g_strScoutFileDir
    global g_dicScoutOrtherFileDir
    global g_dictInitiaType
    global g_strPicSaveDir
    global g_strHaveGeneratedSqlte3Path
    global dicProductTypeMap
    global iKeepPicDayNum
    global datetimeFromList
    global g_dictScoutDirOutPutSelf
    global g_dictScoutDirScale
    global g_listPhoneServer
    global g_lstInitiaType
    global g_iTransparent
    global g_dResolution
    global g_iPupProduct
    global g_strSWFToolsPath
    global g_strSWFOutput
    global g_strSOffice
    global g_strCappiLevels
    global g_dictScoutDirLwfd
    global g_micapsDir
    global g_micapsLatestFile
    global g_micapsLatestFileNew
    

    #print("the work dir is %s"%os.getcwd())
    file = open("config.ini")
    historydays = 0
    g_strSWFOutput = os.getcwd()[0:-4] + "\webapps\output\Office2SWF"
    if os.path.exists(g_strSWFOutput) == False:
        os.makedirs(g_strSWFOutput)
    
    for line in file.readlines():
       
        listDir = []
        line = line.strip()
        if not line or line[0] == '#' or line[0] == '[':
            print(line)
            continue
        if line.find("=") == -1:
            if line.endswith(";"):
               line = line[0:-1] 
            line = "ScoutOrtherDir=%s"%line
            
        list = line.split("=")        
        if list[0].strip().lower() == "productdir".lower():
            g_strScoutFileDir= list[1].replace('\n',' ').strip()
            if g_strScoutFileDir.endswith("/") or g_strScoutFileDir.endswith("\\"):
                g_strScoutFileDir = g_strScoutFileDir[0:-1]
            if g_iPupProduct == 0:
                print(g_strScoutFileDir)
        elif list[0].strip().lower() == "InitiativeType".lower():
            g_lstInitiaType = list[1].strip().split(",")    
        elif list[0].strip().lower() == "GenePicDir".lower():   
            g_strPicSaveDir = list[1].replace('\n',' ').strip()
            g_strHaveGeneratedSqlte3Path = "%s\\pictures.db"%g_strPicSaveDir
            print(g_strHaveGeneratedSqlte3Path)
#            logger.info(g_strHaveGeneratedSqlte3Path)
        elif list[0].strip().lower() == "ScoutOrtherDir".lower():
            strScoutOrtherFileDir = list[1].replace('\n',' ').strip()
            #print(strScoutOrtherFileDir)
            if strScoutOrtherFileDir.endswith('|'):
                listDir.append(strScoutOrtherFileDir[0:-1].strip())
                for scoutLine in file.readlines():
                    if scoutLine.find("=") != -1:
                        break
                    elif scoutLine.endswith('|'):
                        listDir.append(scoutLine[0:-1].strip())
                    else:
                        listDir.append(scoutLine)
                        break
            else:
                listDir.append(strScoutOrtherFileDir)
                
#            listDir = strScoutOrtherFileDir.split(";")
            for dir in listDir:
                listType = dir.split("#")
                if len(listType) >= 2:
                    #print(listType)

                    if listType[1].find(";") != -1:
                        listType[1] = listType[1][0:-1]
                    print(listType[0],"   ",listType[1])
                    g_dicScoutOrtherFileDir[listType[0]] = int(listType[1])
                    g_dictScoutDirOutPutSelf[listType[0]] = ""
                    g_dictScoutDirScale[listType[0]] = -1
                    if len(listType) <= 2:
                        continue 

                    if(listType[2].endswith(";")):
                        listType[2] = listType[2][0:-1]
                    g_dictScoutDirOutPutSelf[listType[0]] = listType[2]
                    if int(listType[1]) == 102:
                        list0 = listType[0] 
                        list2 = listType[2] 
                        while(1):
                            if list0.endswith("/") or list0.endswith("\\"):
                                list0 = list0[0:len(list0)-1]
                            else:
                                break
                        if list0 in g_dictScoutDirLwfd:
                            g_dictScoutDirLwfd[list0].append(list2)
                        else:
                            g_dictScoutDirLwfd[list0] = []
                            g_dictScoutDirLwfd[list0].append(list2)
                      
                        continue
                          
                             
                    if(len(listType) >= 4):
                        g_dictScoutDirScale[listType[0]] =listType[3]
                    if listType[2].startswith("\\") or listType[2].startswith("/"):
                        PubFunction.MakeDir("%s%s"%(g_strPicSaveDir,listType[2]))
                    else:   
                        PubFunction.MakeDir("%s/%s"%(g_strPicSaveDir,listType[2]))
            #print(g_dicScoutOrtherFileDir,g_dictScoutDirOutPutSelf)
            
        elif list[0].strip().lower() == "KeepPicturesDayNum".lower():
            iKeepPicDayNum = int(list[1].replace('\n',' ').strip())    
        elif list[0].strip().lower() == "Transparent".lower():
            g_iTransparent = int(list[1].replace('\n',' ').strip())    
        elif list[0].strip().lower() == "Scale".lower():
            g_dResolution = float(list[1].replace('\n',' ').strip())    
        elif list[0].strip().lower() == "historyDays".lower():
            iDays = int(list[1].replace('\n',' ').strip())
            if iDays <= 0:
                continue
            historydays = iDays*(-1)
        elif list[0].strip().lower() == "cappiLevels".lower():
           g_strCappiLevels =  list[1].replace('\n',' ').strip()
        elif list[0].strip().lower() == "SWFToolPath".lower():
           g_strSWFToolsPath =  list[1].replace('\n',' ').strip()
        elif list[0].strip().lower() == "PhoneServer".lower():
            #PhoneServer=ip:10.28.17.224;user:iphone;psw:ip123
            info = list[1].replace('\n',' ').strip()
            listftpInfo = info.split(";")
            for item in listftpInfo:
                listInner = item.split(":")
                if len(listInner) >= 2:
                    g_listPhoneServer.append(listInner[1])
    datetimeFromList = []
    
    for i in range(len(g_dicScoutOrtherFileDir)):
            datetimeFrom = datetime.now()
            if historydays == 0:
                datetimeFrom = datetime.min
            else:
                datetimeFrom = datetimeFrom + timedelta(days = historydays)
#            datetimeFrom = datetimeFrom + timedelta(minutes = -10)
            datetimeFromList.append(datetimeFrom)
       
    #print(g_strScoutFileDir,g_lstInitiaType,datetimeFromList)    
    file.close()
    #print("g_dicScoutOrtherFileDir \n",g_dicScoutOrtherFileDir,g_dictScoutDirOutPutSelf)

    if os.path.exists("scoutdir") == False:
        os.mkdir("scoutdir")
    if os.path.exists("temp") == False:
        os.mkdir("temp")

    file = open("InitiaGenPicConifg.ini") 
    for line in file.readlines():
        list = line.split(",")
        if list[0] in g_lstInitiaType:
            g_dictInitiaType[list[1]] = list[2].strip()
    file.close()
    
    if len(g_dictInitiaType) == 0:
        print("error parse swan file: g_dictInitiaType:\n",g_dictInitiaType)

    file = open("productTypeMap.ini")
    for line in file.readlines():
        line = line.strip()
        if not line:
            continue
        list = line.split(' = ')
        dicProductTypeMap[re.sub('\d{12,14}','@',list[1])] = list[0]
#    print(dicProductTypeMap)
    file.close()
    
    
    
    #start open office service
    if g_iPupProduct == 0:
        bRet = winproc.IsProcStarted("soffice.exe")
        if bRet:
            print("soffice have started")
            #return
        
        fullpath="L:\\123455"
        driveList = ["C:","D:","E:","F:","G:"]
        officeName = "OpenOffice.org 3\program\soffice.exe"
    
        for drive in driveList:    
            if os.access("%s\\"%(drive), os.F_OK ) == False:
                continue
            listFiles1 = os.listdir("%s\\"%(drive))
            fullpath = "%s\\%s"%(drive,officeName)
            print(fullpath)
            if(os.path.exists(fullpath)):
                break
        
        if os.path.exists(fullpath) == False:
            for drive in driveList:     
                if os.access("%s\\"%(drive), os.F_OK ) == False:
                    continue
                listFiles1 = os.listdir("%s\\"%(drive))
                for dirCur in listFiles1:
                    fullpath = "%s\\%s\\%s"%(drive,dirCur,officeName)
                    #print(fullpath)
                    if(os.path.exists(fullpath)):
                        break
                if(os.path.exists(fullpath)):
                    break
        
        g_strSOffice = fullpath
        print(g_strSOffice,".....................in InitiaConfig() soffice")

'''
    sql = ""
#    conn = sqlite3.connect('\\\\10.28.30.189\\output\\pictures.db')

    bExist = os.path.exists(g_strHaveGeneratedSqlte3Path)
    conn = sqlite3.connect(g_strHaveGeneratedSqlte3Path)
    cur = conn.cursor()
    if not bExist:
        cur.execute('drop table if exists PictureInfo;')
#        cur.execute('CREATE TABLE PictureInfo (time float PRIMARY KEY, file VARCHAR(100), rects VARCHAR(200))')
        cur.execute('CREATE TABLE PictureInfo (time float, file VARCHAR(100), rects VARCHAR(200))')
        cur.execute('CREATE TABLE IF NOT EXISTS PictureInfo (file VARCHAR(100)  PRIMARY KEY, rects VARCHAR(200),time INTEGER)')
        cur.execute('CREATE INDEX IF NOT EXISTS fileid ON PictureInfo(file ASC)')
#        cur.execute('INSERT INTO PictureInfo (time, file, rects) VALUES(20120212, "apple", "12,28,32")')
        conn.commit()
'''
    
    
    

#initia micaps cofnig        
def initializeMicapsConfig():   
    global g_micapsDir
    global g_micapsLatestFileNew
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
             if totalDir.endswith("\\") or totalDir.endswith("/"):
                 totalDir = totalDir[0:-1] 
             if totalDir.startswith("\""):
                 totalDir = totalDir[1:] 
             #totalDir = "X:/data/newecmwf_grib"
             g_micapsDir = totalDir
        elif  list[0].strip().lower() == "FilterDir".lower():
             listDir = list[1].strip().split(";")
             break
    file.close()
    print(listDir)
    for item in listDir:
        
        g_micapsLatestFileNew = {}
        micapsLatestFileNew = {}
        getfilelist(micapsLatestFileNew, g_micapsDir + "/" + item)
      
        for key in micapsLatestFileNew.keys():
            g_micapsLatestFileNew[key[len(g_micapsDir)+1:]] = micapsLatestFileNew[key]
        print(g_micapsLatestFileNew)
        updateSqlite3()
    
    #initia sqlite3 dialog
    
def updateSqlite3(sql = ""):
    
    global g_dictInitiaGenFile
    global g_dictNotInitiaGenFile
    global g_strHaveGeneratedSqlte3Path
    global conn
    global cur
    global g_strPrdIndexFileTemp
    global g_strPrdIndexFile
    global g_micapsLatestFileNew
    
#    conn = sqlite3.connect('\\\\10.28.30.189\\output\\pictures.db')
    if not g_dictInitiaGenFile and not g_dictNotInitiaGenFile and len(g_micapsLatestFileNew) == 0:
#        print("in updateSqlite3 g_dictInitiaGenFile is null,so return")
        return
    bExist = os.path.exists(g_strHaveGeneratedSqlte3Path)
    try:
        conn = sqlite3.connect(g_strHaveGeneratedSqlte3Path)
    except Exception as E:
        strInfo = str(E)
        print("sqlite3 connect error so return",g_strHaveGeneratedSqlte3Path,strInfo)
#        logger.error(g_strHaveGeneratedSqlte3Path + strInfo)
        return
    cur = conn.cursor()
    if not bExist:
#        cur.execute('drop table if exists PictureInfo;')
#        cur.execute('CREATE TABLE PictureInfo (time float PRIMARY KEY, file VARCHAR(100), rects VARCHAR(200))')
#        cur.execute('CREATE TABLE IF NOT EXISTS PictureInfo (file VARCHAR(100)  PRIMARY KEY, rects VARCHAR(200),time INTEGER)')
        cur.execute('CREATE TABLE IF NOT EXISTS PictureInfo (time int, file VARCHAR(100),rects VARCHAR(200))')
        cur.execute('CREATE INDEX IF NOT EXISTS fileIndex ON PictureInfo(file ASC)')

        cur.execute('CREATE TABLE IF NOT EXISTS LatestFile (time int, type VARCHAR(50) PRIMARY KEY, file VARCHAR(100))')
        cur.execute('CREATE INDEX IF NOT EXISTS typeIndex ON LatestFile(type ASC)')

        cur.execute('CREATE TABLE IF NOT EXISTS ScoutFile (time int, file VARCHAR(256))')
        cur.execute('CREATE INDEX IF NOT EXISTS ScoutIndex ON ScoutFile(file ASC)')

#        cur.execute('INSERT INTO PictureInfo (time, file, rects) VALUES(20120212, "apple", "12,28,32")')
        conn.commit()
 
    if  not sql:
        #initia generate picture
        for key in g_dictInitiaGenFile.keys():
    #        print(sql)
            
            #exstract the type of file
            type = ""           
            filename = "" 
            if g_dictInitiaGenFile[key] == 21 or g_dictInitiaGenFile[key] == 17:
                continue
            if key.rfind("/") != -1:                
                filename = key[key.rfind("/")+1:len(key)]
            else:
                filename = key[key.rfind("\\")+1:len(key)] 
            
            strTemp = re.sub('\d{6,14}','@',filename)
            if strTemp == filename:
                strTemp = "UNKNOW"
            if strTemp in dicProductTypeMap:
                type = dicProductTypeMap[strTemp]
            else:
                #@_0902_FY2E_TBB_DCI.dat handle date and time depart 
                strTemp = re.sub('\d{4,14}','@',strTemp) 
                type = dicProductTypeMap[strTemp] if strTemp in dicProductTypeMap else "UNKNOW" 
 
 
            try:
                sql = "INSERT INTO PictureInfo (file, rects,time) VALUES('%s', '%s', %d);" %(filename,"OK",time.time())
                #print("update PictureInfo table successfully....")
                cur.execute(sql)
                sql = "REPLACE INTO LatestFile (file, type,time) VALUES('%s', '%s', %d);" %(filename,type,time.time())
                cur.execute(sql)
        #       print(sql),
        #       logger.info(sql)
        
            except Exception as E:
                strInfo = str(E)
        #        logger.error(strInfo)
                strCommit = strInfo
                print(strInfo,"updatesqlite3 commit excetpion in g_dictInitiaGenFile")
                           
        
        #Not initia generate picture
        for key in g_dictNotInitiaGenFile.keys():
            type = ""           
            filename = "" 
            if key.rfind("/") != -1:                
                filename = key[key.rfind("/")+1:len(key)]
            else:
                filename = key[key.rfind("\\")+1:len(key)] 
            
            strTemp = re.sub('\d{6,14}','@',filename)
            if strTemp == filename:
                strTemp = "UNKNOW"
            if strTemp in dicProductTypeMap:
                type = dicProductTypeMap[strTemp]
            else:
                type = "UNKNOW"
 
            sql = "REPLACE INTO LatestFile (file, type,time) VALUES('%s', '%s', %d);" %(filename,type,time.time())
            cur.execute(sql)
#            print(sql)

        #update micaps latest file
        for key in g_micapsLatestFileNew.keys():
            filename = g_micapsLatestFileNew[key] 
            type = key
            sql = "REPLACE INTO LatestFile (file, type,time) VALUES('%s', '%s', %d);" %(filename,type,time.time())
            cur.execute(sql)
#            print(sql)
   
    
    else: 
        cur.execute(sql)
        
#    print(sql)
#    cur.execute('SELECT * FROM PictureInfo LIMIT 20')
#    print(cur.fetchall())
    strCommit = ""
    try:
        conn.commit()
        g_strPrdIndexFile = g_strPrdIndexFileTemp
        strCommit = "commit successfully!"
    except Exception as E:
        strInfo = str(E)
#        logger.error(strInfo)
        strCommit = strInfo
        print(strInfo,"updatesqlite3 commit excetpion")
    cur.close()
    conn.close()
    
    g_micapsLatestFileNew = {}
    printHelloMsg()
#    print("the latest file info have been updated to database!\n")
    tmdelta = datetime.now() -  datetimeFrom 
#    tmdelta = datetime.now() -  datetimeFrom + timedelta(hours = 45)
    print(strCommit)
    print("the process has been run :  ",tmdelta)
    print("\n")

def HandleRadarUnit():
    print("handle RadarUnit")
    global g_timeRadarUnit
    global g_dResolution
    timeNow = time.time()
    pFile = c_char_p(b"config.ini")
    pElement = c_char_p(b"reflective")
#        pSaveDir = c_char_p(b"C:\\aaa\\output")  
    strSaveDir = g_strPicSaveDir
    pSaveDir = create_string_buffer(strSaveDir.encode("utf-8"),256) 
#            dll.setLowHeightResolution(2,9)
    
    dResolution = c_double(g_dResolution)
    #dResolution = c_double(-2.0)

    rectView = (c_float *4)(23.063,-13.5744,175.926,64.6542)
    iRet = -1

    tm = int(time.time())
    dt = datetime.fromtimestamp(tm).strftime("%Y%m%d%H%M%S")
    #d_time = time.strptime(dt, '%Y%m%d%H%M%S')
    d_min = dt[-4:-2]
    #d_time = d_time[0:-4]
    k,b = divmod(int(d_min),6)
    tmNow = "%s%02d"%(dt[:-4],6*k)
    print(d_min,k,b,tmNow)

    if timeNow - g_timeRadarUnit > 6*60:
        timeHandle = float(tmNow)
        fLevel = c_float(1.0)    
        fFilter = c_float(-99999.0)
        iFileType = c_int(27)
        try:
            iRet = dll.GetDataPicture(pFile,pElement,fLevel,dResolution,rectView,iFileType,c_int(0),c_int(g_iTransparent),c_int(800),c_int(600),pSaveDir,c_int(0),fFilter) 
        except Exception as E:
             print(E)
        g_timeRadarUnit = timeNow
                
def ftpUpload(listFtp):
    
    global g_listPhoneServer
    if not listFtp or len(g_listPhoneServer) != 4:
        return
    
    rootdir_remote = '/disk2/iphone'
    rootdir_remote = ""
    hostaddr = g_listPhoneServer[0]
    username = g_listPhoneServer[1]
    password = g_listPhoneServer[2]
#    if len(g_listPhoneServer) >= 4:
#        rootdir_remote = g_listPhoneServer[3]
    port  =  21   # 端口号 
    #rootdir_remote =           # 远程目录
    
    try:
        f = MyFtp.MYFTP(hostaddr, username, password, rootdir_remote, port)
        f.login()    
        listTemp = copy.deepcopy(listFtp)
        for picPath in listTemp:
            
            basename = os.path.basename(picPath)
            basename = basename[0:-4]# remove .png
            ftpDir = "%s/%s_100x100"%(rootdir_remote,basename)
            if not os.path.exists(picPath):
                print("%s not exist"%picPath)
                listFtp.remove(picPath)
                continue
            try:
                f.makedir("%s"%(ftpDir))
                f.upload_file(picPath,"%s/%s"%(ftpDir,os.path.split(picPath)[1]))
            except Exception as E:
                listFtp.remove(picPath)
                continue
            print(picPath, os.path.split(picPath)[1])
            listFtp.remove(picPath)
        f.ClearPictPeriodly(iKeepPicDayNum)    

    except Exception as E:
        #fileHandle.write("ftpSendFile failed path:%s,file:%s \n"%(picPath, os.path.split(picPath)[1]))
        print(E)


def clearTempDir():
    
    iRet = 0
    currentTime = datetime.now()
    #print(currentTime)
    
    #notice
    if currentTime.hour >= 2:
        return iRet
    #clear the temp data file
#    dirList = os.listdir("%s\\temp\\"%os.getcwd())
#    print(dirList) 

    try:
        print("clear temp folder:%s\\temp"%os.getcwd())
        shutil.rmtree("%s\\temp"%os.getcwd()) 
    except Exception as E:
        print("windows clear  temp folder failed",E)
 
def SWFMaker():
    global g_strSWFToolsPath
    global g_strSWFOutput
    global g_listZhidaoChanpin
    global g_strSOffice
    global g_dictScoutDirLwfd
    
    if len(g_listZhidaoChanpin) < 1:
        return
#    if winproc.IsProcStarted("ExecUtil.exe") == True:
    if winproc.IsProcStarted("ExecUtil.exe") == True:
        return
    
    timeNow = time.localtime() 
    fileName = "%s/scoutdir/%02d%02d%02d.zhidaocp" % (os.getcwd(),timeNow.tm_hour,timeNow.tm_min,timeNow.tm_sec)
    print(fileName)
    dicMatch = {}
    print(g_dictScoutDirLwfd)
    for key in g_listZhidaoChanpin:
        dirname = os.path.dirname(key)
        if dirname.endswith("/"):
            dirname = dirname[0:len(dirname)-1]
        if g_dictScoutDirLwfd.get(dirname,"no_found") == "no_found":
            continue
        listFormat = g_dictScoutDirLwfd[dirname]
        lwfdfile = os.path.basename(key)
        print(lwfdfile)
        #lwfdfile.match(lwfdformat)
        for lwfdformat in listFormat:
            
            if len(lwfdformat) == 0:
                continue
        #java
#        String regex =  "^" + str.replaceAll("\\{[^{^}]*\\}","[\u4e00-\u9fa5a-zA-Z0-9]+");
                        
 #                       //handle special character
  #                      regex = regex.replace("(", "\\(").replace(")", "\\)");
   #                     if(flNames[i].matches(regex)){
            pat="{[\u4e00-\u9fa5a-zA-Z0-9]+}";
            pat1="[\u4e00-\u9fa5a-zA-Z0-9]+";
            #pat="{[a-zA-Z0-9]+}";
            repat = re.compile(pat)
            strSub=repat.sub(pat1,lwfdformat)
            strSub = strSub.replace("(", "\\(")
            strSub = strSub.replace(")", "\\)")
            if  re.match(strSub,lwfdfile):
                dicMatch[key] = ""
                break
    g_listZhidaoChanpin = []
    
    if len(dicMatch) == 0:
        return
    fileHandle = open(fileName,'w')
    for key in dicMatch:
            fileHandle.write(key)
            fileHandle.write("\n")
    fileHandle.close()
             

    command =  g_strSOffice
    command  += ","
    command  +=  g_strSWFToolsPath
    command  += ","
    command  += fileName
    command  += ","
    command  += g_strSWFOutput

    
    startinfo = None
    if os.name == "nt":
        startinfo = subprocess.STARTUPINFO()
        startinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        #startinfo.wShowWindow = subprocess.SW_HIDE
    print(command)
    p=subprocess.Popen(["ExecUtil.exe",command], shell=True,stdout=True)
#    p=subprocess.Popen(["Win32GLPainterTest.exe",command], shell=True,stdout=True)
#    p=subprocess.Popen(["ExecUtil.exe",command], shell=True,stdout=True,startupinfo=startinfo,creationflags=subprocess.CREATE_NEW_CONSOLE)
#    print(command)
    #subprocess.Popen(["ExecUtil.exe",command],startupinfo=startinfo,creationflags=subprocess.CREATE_NEW_CONSOLE) 
    #subprocess.Popen(["ExecUtil.exe"],startupinfo=startinfo,creationflags=subprocess.CREATE_NEW_CONSOLE) 
       
        
def UpdateLatestFile():
    
    global g_strScoutFileDir
    global g_strPicSaveDir
    global g_dicScoutOrtherFileDir
    global g_strPrdIndexFileTemp
    global g_strPrdIndexFile
    global g_dictScoutDirOutPutSelf
    global g_iTransparent
#    global fileHandle
    global listFtp
    global g_dResolution
    global g_iPupProduct
    global g_lstLatestScourFindFile
    global g_listZhidaoChanpin
    global g_listLastestFile
    global g_datetimeSwanIndex
    global g_micapsDir
    global g_micapsLatestFile
    global g_micapsLatestFileNew
    #clear temp dir
    
    clearTempDir()
    
    SWFOutPutPath = os.getcwd()
    dictSwanFile = {}
    list = []
    listNewFiles = []
    indexDir = "%s\\productindex\\"%g_strScoutFileDir
    #print(indexDir)
    if g_iPupProduct == 0:
        
        if os.path.exists(indexDir):
            try:
                #base_dir="E:\\FtpServer\\productindex\\"
#                print("begin: ",indexDir,"  ",datetime.now())
                list=os.listdir(indexDir)
                #按创建时间排序
                #list.sort(key=lambda fn: os.path.getmtime(indexDir+fn) if not os.path.isdir(indexDir+fn) else 0,reverse=True)
                list.sort()
                list.reverse()
#                print("end: ",indexDir,"  ",datetime.now(),"  find files:",len(list))
            except Exception as E:
                print("open index file failed",E)
        
        #print("list  in productindex..",list)
        iCnts = 5
        if list:
            index = iCnts if len(list) > iCnts else len(list)-1
            if(len(list) == 1):
                 index = 1
                
            datetimeMax = g_datetimeSwanIndex
            indexSwan = -1
            for filename in list[0:index]:
                
                indexSwan += 1
                if filename in g_listLastestFile:
                    continue;
                curFile = "%s\\productindex\\%s"%(g_strScoutFileDir,filename)
                #juduge the file to delete or not by iKeepDay
                print("cur file:",curFile)
                dtNow = datetime.now()
                timecurr = time.localtime(os.stat(curFile).st_ctime)
                datetimeCurFile =  datetime(timecurr.tm_year,timecurr.tm_mon,timecurr.tm_mday,timecurr.tm_hour,timecurr.tm_min,timecurr.tm_sec)
                datetimeCurFile +=  timedelta(minutes = 2 if len(g_listLastestFile) == 0 else 10)
                if datetimeCurFile <= g_datetimeSwanIndex:
                    continue
                else:
                    print("new file:",filename)
                    listNewFiles.append(filename)
                    if len(g_listLastestFile) > iCnts:
                        g_listLastestFile.pop()
                    g_listLastestFile.insert(0, filename)
                    if datetimeMax <  datetimeCurFile:
                        datetimeMax =  datetimeCurFile
                    
            #update time
            g_datetimeSwanIndex = datetimeMax
            print("g_datetimeSwanIndex: ",  )
        else:
                    print("没有swan数据源..")

        path = ""
        
        try:
            iControl = 0
            for filename in listNewFiles:
                iControl += 1
                if not filename.endswith(".txt"):
                    continue
                print(filename)
                file = indexDir + filename
                fileHandler = open(file)
                for line in fileHandler.readlines():                 
        #            if(line.find("TITAN") == -1):
        #                continue
                    strLine = line.replace("\\","/")
                    iPos = strLine.rfind("@")
                    if iPos == -1: 
                        continue
        
        #  需要在这里添加文件名过滤配置，以决定传输哪些产品
                    
        #            print(iPos0,fileDetailType)
                    strFile = strLine[iPos + 1:len(strLine)- 1]
        #            fileDetailType =  dicProductTypeMap[re.sub('\d{12,14}','@',strFile)]
                    path = g_strScoutFileDir + strFile
                    iFileType = _hInitiativePic.getTypeByName(strFile,g_dictInitiaType)
                    print("parse: ",path,"  filetype:",iFileType)
                    #if iFileType == -1:
                     #   print("g_dictInitiaType:\n",g_dictInitiaType)
#                    print("g_dictInitiaGenFile: ",g_dictInitiaGenFile)
#                    print("g_dictNotInitiaGenFile: ",g_dictNotInitiaGenFile)
                    if os.path.exists(path)  and iFileType != -1:
                        g_dictInitiaGenFile[path] = iFileType
        #                dictSwanFile[path] = fileDetailType
        #                print("generate the picture of  %s %d " % (path,int(iFileType)))
                    else:
                        g_dictNotInitiaGenFile[path] = iFileType
        #                print("file %s isn't exist  %d" % (path,int(iFileType)))
                if iControl >= 400 :
                    break
                fileHandler.close()
                
        except Exception as E:
            print("open index file failed",E)
            
    #if g_iPupProduct == 0    
        
        #delete after updateing sqlite databse,or it will cause some file has no pictures when exception occour 
#        os.remove(file)
#        break
#    print(g_dictInitiaGenFile)
#  if the initiative dir is empty,we will scout orther scout dir
    bSoutDirFile = None
#    print("g_dictInitiaGenFile",g_dictInitiaGenFile)
    
    #testing
    #ScoutDir(g_dicScoutOrtherFileDir, datetimeFromList,g_dictInitiaGenFile,g_iPupProduct,g_lstLatestScourFindFile)
  
    if not g_dictInitiaGenFile:
        bSoutDirFile = False
        listClearDate = []
        listClearDate.append(datetime.now())
        iRet = ClearTempFiles(g_strPicSaveDir,listClearDate,iKeepPicDayNum)
        if iRet >= 1: #update the records whose data was deleted in ClearTempFiles
            
            datetimeUpdate = listClearDate[0] - timedelta(days = iKeepPicDayNum)
            tt = time.mktime(datetimeUpdate.timetuple())
            sql = "delete from PictureInfo where time <= %f"%tt
            if g_iPupProduct == 0 :
                updateSqlite3(sql)
        ScoutDir(g_dicScoutOrtherFileDir, datetimeFromList,g_dictInitiaGenFile,g_iPupProduct,g_lstLatestScourFindFile)
        #ScoutDir1(g_dicScoutOrtherFileDir, datetimeFromList,g_dictInitiaGenFile)

        #scout micaps directory change
        g_micapsLatestFileNew = {}
        
        beginTm = datetime.now()
        updateMicapsData(g_micapsDir,g_micapsLatestFile,g_micapsLatestFileNew)
        endTm = datetime.now()
        print("update micaps data files number: ",len(g_micapsLatestFileNew))
        print(beginTm,"   ",endTm)
        
        
        
    #  the following begin generate pictures by call c++ dll
  
#    print(g_dictInitiaGenFile)
    for i in range(1):
        for key in g_dictInitiaGenFile.keys():
    #        break
            #notice
            strSaveDir = g_strPicSaveDir
            iFileType = int(g_dictInitiaGenFile[key])
            
            #lwfd file format
            if iFileType == 102:
                g_listZhidaoChanpin.append(key)
                continue
            
            if bSoutDirFile:
                for index,scoutDir in enumerate(g_dicScoutOrtherFileDir):
                    if key.find(scoutDir) != -1 and g_dictScoutDirOutPutSelf[scoutDir]: 
                        strSaveDir = "%s\\%s"%(g_strPicSaveDir,g_dictScoutDirOutPutSelf[scoutDir])
                        if not os.path.exists(strSaveDir) and int():
                            os.mkdir(strSaveDir)
                        break
            pFile    = create_string_buffer(key.encode("utf-8"),256)
    #        pFile = c_char_p(b"D:\\work\\AIW\\testdata\\SWAN\\Swan090811\\ncrad\\TDPRODUCT\\MCR\\Z_OTHE_RADAMCR_200908100212.bin.bz2")
    #        pElement = c_char_p(b"DBZ")
            pElement = c_char_p(b"reflective")
    #        pSaveDir = c_char_p(b"C:\\aaa\\output")  
#            dll.setLowHeightResolution(2,9)
            
            dResolution = c_double(-1.0) if g_iPupProduct == 0 else c_double(-2.0) 
            if iFileType == 101:
                dResolution = c_double(-1.0) 
                iFileType = int(17)
            
            #dResolution = c_double(g_dResolution)
#            dResolution = c_double(-1.0) if g_dictScoutDirScale[os.path.dirname(key)] == -1 else c_double(-2.0) 
            fLevel = c_float(1.0)
            if g_dictScoutDirOutPutSelf.get(os.path.dirname(key), "default") != "default"  and len(g_dictScoutDirOutPutSelf[os.path.dirname(key)]) >= 2:
                strSaveDir = "%s\\%s"%(g_strPicSaveDir,g_dictScoutDirOutPutSelf[os.path.dirname(key)])
            
            pSaveDir = create_string_buffer(strSaveDir.encode("utf-8"),256) 
            fFilter = c_float(-99999.0)
            rectView = (c_float *4)(23.063,-13.5744,175.926,64.6542)
            iRet = -1
    #        fileHandle.write("type:%s,file:%s\n"%(g_dictInitiaGenFile[key],key))
            try:
                iRet = 1
                #print(key)
                iRet = dll.GetDataPicture(pFile,pElement,fLevel,dResolution,rectView,c_int(iFileType),c_int(0),c_int(g_iTransparent),c_int(800),c_int(600),pSaveDir,c_int(0),fFilter) 
            except Exception as E:
                print(E)
            #if iRet = -1,it also indicate the file's picture have been generated,so we insert sqlite3 db too
            if len(g_listPhoneServer) == 4:
                fileFtp = os.path.split(key)
                listFtp.append("%s\\cache\\%s_100x100\\%s.png"%(strSaveDir,fileFtp[1],fileFtp[1]))
#            objgraph.show_most_common_types(limit=20)
            if(iRet == -1): 
                pass
            ### 强制进行垃圾回收
### 打印出对象数目最多的 50 个类型信息
#            objgraph.show_most_common_types(limit=50)
   #update database before generate picture,for to handle web request
    
    if g_iPupProduct == 0 :
        SWFMaker()
        updateSqlite3()
    #print(len(listFtp),listFtp)
   # listFtp = ["C:\\aaa\\output\\cache\\ACHN.CREF000.20130125.023000.latlon_100x100\\ACHN.CREF000.20130125.023000.latlon.png"]
    ftpUpload(listFtp)
    #print(len(listFtp),listFtp)
    #HandleRadarUnit()
    if not g_dictInitiaGenFile:
        print(datetime.now(),' :there are no any file to generate')
    else:
        g_dictInitiaGenFile.clear()
        g_dictNotInitiaGenFile.clear()
        
#   implement the function of Timer,to generate the latest pictures intervally
#    sys.exit(0)
    if g_iPupProduct == 0 :
        #restart at mid night
        dtNow = datetime.now()
        hour = dtNow.hour 
        min = dtNow.minute 
        if hour <= 0 and min <=15:
            print(hour,min)
        else:
            timer = threading.Timer(5,UpdateLatestFile)
            timer.start()
    


if __name__ == '__main__':

#    #hide the console UI
#    if g_iPupProduct == 1:
#        whnd = windll.kernel32.GetConsoleWindow()  
#        if whnd != 0:  
#            windll.user32.ShowWindow(whnd, 0)  
#            windll.kernel32.CloseHandle(whnd) 


    InitiaConfig()
    initializeMicapsConfig()
    
    if g_iPupProduct == 0:
        try:
            print("start successfully....")
            #p=subprocess.Popen(["DirWatcher.exe"], shell=False,stdout=False) 
        except Exception as E:
            strInfo = str(E)
            print(strInfo,"   DirWatcher.exe")

#    ScoutDir(g_dicScoutOrtherFileDir,datetimeFromList,g_dictInitiaGenFile)
#    sys.exit(0)
    timer = threading.Timer(3,UpdateLatestFile)
    timer.start()

 


