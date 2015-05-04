# -*- coding: utf-8 -*-  

from ctypes import *  
#import win32ui
#import win32api
#import win32con
import os,re,sys,threading
import time
import string
from datetime import datetime,date,timedelta

import sqlite3
import UserStruct
import _hInitiativePic
from ScoutDir import *

import logging
import logging.config

LOG_FILENAME = 'logging.conf'
logging.config.fileConfig(LOG_FILENAME)
logger = logging.getLogger("simple_log_example")

#dllfile = "%s\\PictureFactoryPlugin.dll"%os.getcwd()
dll = CDLL("PictureFactoryPlugin.dll")  


g_strScoutIndexDir = ""
g_strScoutFileDir  = ""
g_strClearTempDir  = ""
g_strScoutOrtherFileDir  = ""
g_strPicSaveDir = ""
g_strHaveGeneratedSqlte3Path = ""
g_lstInitiaType = []
datetimeFromList = []
g_dictInitiaType ={}
g_dictInitiaGenFile = {}
g_dictNotInitiaGenFile = {}
dicProductTypeMap = {}
iKeepPicDayNum = 3
#datetimeFrom = datetime(2012,4,11,7,9)
datetimeFrom = datetime.now()
datetimeFrom = datetimeFrom + timedelta(minutes = -10)
datetimeFromList.append(datetimeFrom)


def InitiaConfig():
    global g_strScoutFileDir
    global g_strScoutOrtherFileDir
    global g_strScoutIndexDir
    global g_dictInitiaType
    global g_strPicSaveDir
    global g_strHaveGeneratedSqlte3Path
    global conn
    global cur
    global g_strClearTempDir
    global dicProductTypeMap
    
    file = open("config.ini")
    for line in file.readlines():
        line = line.strip()
        list = line.split("=")
        if list[0] == 'indexdir':
            g_strScoutIndexDir = list[1].replace('\n',' ').strip()
        elif list[0] == "productdir":
            g_strScoutFileDir= list[1].replace('\n',' ').strip()
        elif list[0] == "InitiativeType":
            g_lstInitiaType = list[1].strip().split(",")    
        elif list[0] == "GenePicDir":
            g_strPicSaveDir = list[1].replace('\n',' ').strip()
        elif list[0] == "PictureDBPath":
            g_strHaveGeneratedSqlte3Path = list[1].replace('\n',' ').strip()  
            g_strHaveGeneratedSqlte3Path = "%s\\pictures.db"%g_strHaveGeneratedSqlte3Path
            print(g_strHaveGeneratedSqlte3Path)
            logger.info(g_strHaveGeneratedSqlte3Path)
        elif list[0] == "ScoutOrtherDir":
            g_strScoutOrtherFileDir = list[1].replace('\n',' ').strip()    
        elif list[0] == "KeepPicturesDayNum":
            iKeepPicDayNum = int(list[1].replace('\n',' ').strip())    
        elif list[0] == "ClearDirPeriodical":
            g_strClearTempDir = list[1].replace('\n',' ').strip()    

            
    print(g_strScoutIndexDir,g_strScoutFileDir,g_lstInitiaType)    
    file.close()
    file = open("InitiaGenPicConifg.ini") 
    for line in file.readlines():
        list = line.split(",")
        if list[0] in g_lstInitiaType:
            g_dictInitiaType[list[1]] = list[2].strip()
    file.close()

    file = open("productTypeMap.ini")
    for line in file.readlines():
        line = line.strip()
        if not line:
            continue
        list = line.split(' = ')
        dicProductTypeMap[re.sub('\d{12,14}','@',list[1])] = list[0]
#    print(dicProductTypeMap)
    file.close()
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
    
    
    #initia sqlite3 dialog
    
def updateSqlite3(sql = ""):
    global g_dictInitiaGenFile
    global g_dictNotInitiaGenFile
    global g_strHaveGeneratedSqlte3Path
    global conn
    global cur

    
#    conn = sqlite3.connect('\\\\10.28.30.189\\output\\pictures.db')
    if not g_dictInitiaGenFile and not g_dictNotInitiaGenFile:
        return
    bExist = os.path.exists(g_strHaveGeneratedSqlte3Path)
    conn = sqlite3.connect(g_strHaveGeneratedSqlte3Path)
    cur = conn.cursor()
    if not bExist:
#        cur.execute('drop table if exists PictureInfo;')
#        cur.execute('CREATE TABLE PictureInfo (time float PRIMARY KEY, file VARCHAR(100), rects VARCHAR(200))')
#        cur.execute('CREATE TABLE IF NOT EXISTS PictureInfo (file VARCHAR(100)  PRIMARY KEY, rects VARCHAR(200),time INTEGER)')
        cur.execute('CREATE TABLE IF NOT EXISTS PictureInfo (time int, file VARCHAR(100),rects VARCHAR(200))')
        cur.execute('CREATE INDEX IF NOT EXISTS fileIndex ON PictureInfo(file ASC)')

        cur.execute('CREATE TABLE IF NOT EXISTS LatestFile (time int, type VARCHAR(50) PRIMARY KEY, file VARCHAR(100))')
        cur.execute('CREATE INDEX IF NOT EXISTS typeIndex ON LatestFile(type ASC)')

#        cur.execute('INSERT INTO PictureInfo (time, file, rects) VALUES(20120212, "apple", "12,28,32")')
        conn.commit()
 
    if  not sql:
        #initia generate picture
        for key in g_dictInitiaGenFile.keys():
    #        print(sql)
            
            #exstract the type of file
            type = ""           
            filename = "" 
            if key.rfind("/") != -1:                
                filename = key[key.rfind("/")+1:len(key)]
            else:
                filename = key[key.rfind("\\")+1:len(key)] 
            
            if key.find("latlon") != -1:
                index = key.find("latlon") + len("latlon") + 1 #it is wuhan baoyusuo data or not
                iIndex1 = key.rfind("\\")
                type = dicProductTypeMap[key[index:iIndex1]]   
            else:
                strTemp = re.sub('\d{12,14}','@',filename)
                if strTemp == filename:
                    strTemp = "UNKNOW"
                if strTemp in dicProductTypeMap:
                    type = dicProductTypeMap[strTemp]
                else:
                    type = "UNKNOW"
                    
            sql = "INSERT INTO PictureInfo (file, rects,time) VALUES('%s', '%s', %d);" %(filename,"OK",time.time())
#            print(sql)
            cur.execute(sql)
            sql = "REPLACE INTO LatestFile (file, type,time) VALUES('%s', '%s', %d);" %(filename,type,time.time())
            cur.execute(sql)
#            print(sql)
#            logger.info(sql)
        
        #Not initia generate picture
        for key in g_dictNotInitiaGenFile.keys():
            type = ""           
            filename = "" 
            if key.rfind("/") != -1:                
                filename = key[key.rfind("/")+1:len(key)]
            else:
                filename = key[key.rfind("\\")+1:len(key)] 
            
            if key.find("latlon") != -1:
                index = key.find("latlon") + len("latlon") + 1 #it is wuhan baoyusuo data or not
                iIndex1 = key.rfind("\\")
                type = dicProductTypeMap[key[index:iIndex1]]   
            else:
                strTemp = re.sub('\d{12,14}','@',filename)
                if strTemp == filename:
                    strTemp = "UNKNOW"
                if strTemp in dicProductTypeMap:
                    type = dicProductTypeMap[strTemp]
                else:
                    type = "UNKNOW"
 
            sql = "REPLACE INTO LatestFile (file, type,time) VALUES('%s', '%s', %d);" %(filename,type,time.time())
            cur.execute(sql)
#            print(sql)
    else: 
        cur.execute(sql)
        
#    print(sql)
#    cur.execute('SELECT * FROM PictureInfo LIMIT 20')
#    print(cur.fetchall())
    try:
        conn.commit()
    except Exception as E:
        strInfo = str(E)
        logger.error(strInfo)
        print(strInfo)
    cur.close()
    conn.close()
 
def UpdataLatestFile():
    
    global g_strScoutFileDir
    global g_strScoutIndexDir
    global g_strPicSaveDir
    global g_strScoutOrtherFileDir
    dictSwanFile = {}
    list = os.listdir(g_strScoutIndexDir)
    path = ""
    iControl = 0
    for filename in list:
        iControl += 1
        if not filename.endswith(".txt"):
            continue
        file = g_strScoutIndexDir + "\\" + filename
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
        os.remove(file)
#        break
#    print(g_dictInitiaGenFile)
#  if the initiative dir is empty,we will scout orther scout dir
    if not g_dictInitiaGenFile: 
        iRet = ClearTempFiles(g_strPicSaveDir,datetimeFromList,iKeepPicDayNum,g_strClearTempDir)
        if iRet >= 1: #update the records whose data was deleted in ClearTempFiles
            
            datetimeUpdate = datetimeFromList[0] - timedelta(days = iKeepPicDayNum)
            tt = time.mktime(datetimeUpdate.timetuple())
            sql = "delete from PictureInfo where time <= %f"%tt
            updateSqlite3(sql)
        ScoutDir(g_strScoutOrtherFileDir, datetimeFromList,g_dictInitiaGenFile)

    #  the following begin generate pictures by call c++ dll
    for key in g_dictInitiaGenFile.keys():
#        break
        #notice
        pFile    = create_string_buffer(key.encode("gbk"),100)
#        pFile = c_char_p(b"D:\\work\\AIW\\testdata\\SWAN\\Swan090811\\ncrad\\TDPRODUCT\\MCR\\Z_OTHE_RADAMCR_200908100212.bin.bz2")
        pElement = c_char_p(b"DBZ")
#        pSaveDir = c_char_p(b"C:\\aaa\\output")  
        pSaveDir = create_string_buffer(g_strPicSaveDir.encode("gbk"),100) 
        dll.setLowHeightResolution(2,9)
        dResolution = c_double(-1.0) 
        fLevel = c_float(5.0)
        rectView = (c_float *4)(23.063,-13.5744,175.926,64.6542)
        iRet = -1
        iRet = dll.GetDataPicture(pFile,pElement,fLevel,dResolution,rectView,c_int(int(g_dictInitiaGenFile[key])),c_int(0),c_int(128),c_int(800),c_int(600),pSaveDir) 
        #if iRet = -1,it also indicate the file's picture have been generated,so we insert sqlite3 db too
        if(iRet == -1): 
            pass
       
   #update database before generate picture,for to handle web request
    
    if not g_dictInitiaGenFile:
        print(datetime.now(),' :there are no any file to generate')
    else:
        updateSqlite3()
        g_dictInitiaGenFile.clear()
        g_dictNotInitiaGenFile.clear()
#   implement the function of Timer,to generate the latest pictures intervally
#    sys.exit(0)
    global timer
    timer = threading.Timer(30,UpdataLatestFile)
    timer.start()


if __name__ == '__main__':

    InitiaConfig()
#    ScoutDir(g_strScoutOrtherFileDir,datetimeFromList,g_dictInitiaGenFile)
#    sys.exit(0)
    timer = threading.Timer(3,UpdataLatestFile)
    timer.start()

 


