# -*- coding: utf-8 -*-  

from ctypes import *  
import win32ui
import win32api
import win32con
import os
import sys
import threading
import time
import string
from datetime import datetime

import sqlite3
import UserStruct
from   threadpool import *
import _hInitiativePic
#from InitiativePic_singleThread import pSaveDir

dll = CDLL("PictureFactoryPlugin.dll")  

g_strHaveGeneratedSqlte3Path = ""
g_strScoutIndexDir = ""
g_strScoutFileDir  = ""
g_strPicSaveDir = ""
g_lstInitiaType = []
g_dictInitiaType ={}
g_InitiaGenFile = []

i=0

def do_something(data):
        assert isinstance(data, tuple)
        key = data[0]
        itype = data[1]
        pFile = create_string_buffer(key.encode("gbk"),100)
#        pFile = c_char_p(b"D:/work/AIW/testdata/SWAN/Swan090811/ncrad/TDMOSAIC/Z_OTHE_RADAMOSAIC_200908100818.bin.bz2")
        pElement = c_char_p(b"DBZ")
#        pSaveDir = create_string_buffer(g_strPicSaveDir.encode("gbk"),100)
        pSaveDir = c_char_p(b"Y:\\")
        dll.setLowHeightResolution(2,9)
        dResolution = c_double(-1.0) 
        fLevel = c_float(5.0)
        rectView = (c_float *4)(23.063,-13.5744,175.926,64.6542)
        iRet = -1
        iRet = dll.GetDataPicture(pFile,pElement,fLevel,dResolution,rectView,c_int(int(itype)),c_int(0),c_int(255),c_int(800),c_int(600),pSaveDir) 
#        print("do something :",pFile,dResolution,pSaveDir)
        if(iRet == -1): #if iRet = -1,it also indicate the file's picture have been generated,so we insert sqlite3 db too
            pass
 
# this will be called each time a result is available
def print_result(request, result):
    print("**** Result from request #%s: %r" % (request.requestID, result))

# this will be called when an exception occurs within a thread
# this example exception handler does little more than the default handler
def handle_exception(request, exc_info):
    if not isinstance(exc_info, tuple):
        # Something is seriously wrong...
#        print(request)
#        print(exc_info)
        raise SystemExit
    print("**** Exception occured in request #%s: %s" % \
      (request.requestID, exc_info))


def InitiaConfig():
    global g_strScoutFileDir
    global g_strScoutIndexDir
    global g_dictInitiaType
    file = open("config.ini")
    for line in file.readlines():
        line = line.strip()
        list = line.split("=")
        if list[0] == 'indexdir':
            g_strScoutIndexDir = list[1].replace('\n',' ')
            g_strScoutIndexDir = g_strScoutIndexDir.strip()
        elif list[0] == "productdir":
            g_strScoutFileDir= list[1].replace('\n',' ').strip()
        elif list[0] == "InitiativeType":
            g_lstInitiaType = list[1].strip().split(",") 
        elif list[0] == "GenePicDir":
            g_strPicSaveDir = list[1].strip()
        elif list[0] == "PictureDBPath":
            g_strHaveGeneratedSqlte3Path = list[1].strip()
    print(g_strScoutIndexDir,g_strScoutFileDir,g_lstInitiaType)    
   
    file = open("InitiaGenPicConifg.ini") 
    for line in file.readlines():
        list = line.split(",")
        if list[0] in g_lstInitiaType:
            g_dictInitiaType[list[1]] = list[2].strip()


def updateSqlite3():
    global g_InitiaGenFile

    sql = ""
#    conn = sqlite3.connect('\\\\10.28.30.189\\output\\pictures.db')
    conn = sqlite3.connect('%s\\pictures.db'%g_strHaveGeneratedSqlte3Path)
#    conn = sqlite3.connect('pictures_debug.db')
    cur = conn.cursor()
#    cur.execute('drop table if exists PictureInfo;')
#    conn.commit()
#    cur.execute('CREATE TABLE IF NOT EXISTS PictureInfo (file VARCHAR(100)  PRIMARY KEY, rects VARCHAR(200),time INTEGER)')
#    cur.execute('CREATE INDEX IF NOT EXISTS fileid ON PictureInfo(file ASC)')
#    conn.commit()
 
    for key,value in g_InitiaGenFile:
#        print(sql)
        sql = "INSERT INTO PictureInfo (file, rects,time) VALUES('%s', '%s',%d);" %(key[key.rfind("/")+1:len(key)],"OK",time.time())
        print(sql)
        cur.execute(sql)
#    print(sql)
    conn.commit()
#    cur.execute('SELECT * FROM PictureInfo LIMIT 20')
#    print(cur.fetchall())
    cur.close()
    conn.close()
 
 
def UpdataLatestFile():

    global g_strScoutFileDir
    global g_strScoutIndexDir
    global main
    global timer
    list = os.listdir(g_strScoutIndexDir)
    path = ""
    iControl = 0
    for filename in list:
        iControl += 1
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

            strFile = strLine[iPos + 1:len(strLine)- 1]
            path = g_strScoutFileDir + strFile
#            path = path.replace("\\","/")
            iFileType = _hInitiativePic.getTypeByName(strFile,g_dictInitiaType)
            
            if not os.path.exists(path):
                print("the %s isn't exists"%path)
                continue
            if iFileType != -1:
                g_InitiaGenFile.append((path,iFileType))
                print("find the file and its type : %s %d " % (path,int(iFileType)))
#            else:
#                print("file %s isn't exist  %d" % (path,int(iFileType)))
        if iControl >= 400 :
            break
        fileHandler.close()
        os.remove(file)
#        break
#    print(g_InitiaGenFile)
    
    if not g_InitiaGenFile:
        print(datetime.now(),' :there are no any file to generate')
        timer = threading.Timer(30,UpdataLatestFile)
        timer.start()
        return
#  the following begin generate pictures by call c++ dll
    requests = makeRequests(do_something, g_InitiaGenFile, print_result, handle_exception)
    # then we put the work requests in the queue...
    for req in requests:
        main.putRequest(req)
        print("Work request #%s added." % req.requestID)

    # instead we can poll for results while doing something else:
    i = 0
    while True:
        try:
            time.sleep(1)
            main.poll()
            print("Main thread working...")
            print("(active worker threads: %i)" % (threading.activeCount()-1, ))
            if i == 10:
                print("**** Adding 3 more worker threads...")
                main.createWorkers(3)
            if i == 20:
                print("**** Dismissing 2 worker threads...")
                main.dismissWorkers(2)
            i += 1
        except KeyboardInterrupt:
            print("**** Interrupted!")
            break
        except NoResultsPending:
            print("**** No pending results.")
            break
    if main.dismissedWorkers:
        print("Joining all dismissed worker threads...")
        main.joinAllDismissedWorkers()
        
#update the sqlite3 to indicate which file have been generated
    updateSqlite3()     
    del g_InitiaGenFile[:]
#   implement the function of Timer,to generate the latest pictures intervally
#    sys.exit(0)
    timer = threading.Timer(30,UpdataLatestFile)
    timer.start()
        
if __name__ == '__main__':

    InitiaConfig()
#    sys.exit(0)

    print("Creating thread pool with 3 worker threads.")
    main = ThreadPool(3)
    dll.InitializePicServer()
    timer = threading.Timer(3,UpdataLatestFile)
    timer.start()


   


