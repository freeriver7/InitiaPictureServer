# -*- conding:utf-8 -*-

import subprocess
import re,winproc,os,glob
import random
from datetime import datetime 
import sys
import time,winproc,PubFunction
from ctypes import *
#cxfreeze StartPeriodical.py --target-dir dist
#p=subprocess.call(["python", "InitiativePic_singleThread.py"])

g_iPupProduct = 0

def printHelloMsg():
    print("\n")
    print("           *                              ")
    print("                                          ")
    print("       *       *                          ")
    print("                                          ")
    print("           *                              ")
    print("\n")
    
if __name__ == '__main__':
    
    
    iTimes = 0
    iSleep = 3
    p1 = 0
    p2 = 0
    p3 = 0
    p4 = 0
    p4Counts = 0
    
#    bRunning = PubFunction.CanConnectPort(7137)
    processName = "PictureServer.exe"
    if os.path.exists(processName):
        winproc.kill_pro(processName)
        p1=subprocess.Popen([processName], stdout=True) 
    
    processName = "InitiaPicServer.exe"
    if os.path.exists(processName):
        winproc.kill_pro(processName)
        p2=subprocess.Popen([processName],creationflags=subprocess.CREATE_NEW_CONSOLE) 

    startinfo = None
    if os.name == "nt":
        startinfo = subprocess.STARTUPINFO()
        startinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startinfo.wShowWindow = subprocess.SW_HIDE

    processName = "InitiaPicServer_Pup.exe"
    if os.path.exists(processName):
        winproc.kill_pro(processName)
        p3=subprocess.Popen([processName],startupinfo=startinfo,creationflags=subprocess.CREATE_NEW_CONSOLE) 

    processName = "WebMICAPSWatcher.exe"
    if os.path.exists(processName):
        winproc.kill_pro(processName)
        p4=subprocess.Popen([processName],startupinfo=startinfo,creationflags=subprocess.CREATE_NEW_CONSOLE) 

    
    while 1:

        time.sleep(iSleep)
        iTimes += 1
        
        if iTimes*iSleep >= 30:
            iTimes = 0
        
            bRunning = PubFunction.CanConnectPort(7137)
    #        ret1=subprocess.Popen.poll(p1)
            if bRunning:
                pass
        #        print(datetime.now(),"the Initiative Programer is running!")
            else:
                print(datetime.now(),"PictureServer has stoped,so it will restart")
    #            winproc.killPid(p1.pid)
                winproc.kill_pro("PictureServer.exe")
                p1=subprocess.Popen(["PictureServer.exe"],stdout=True) 
                #p=subprocess.Popen(["start.bat"], shell=True,stdout=True) 
    
            #ret2=subprocess.Popen.poll(p2)
            ret2=subprocess.Popen.poll(p2)
            if ret2 is None:
                print(datetime.now()," ...  smooth running!")
                printHelloMsg()
                pass
            else:
                print(datetime.now(),"InitiaPicServer has stoped,so it will restart")
    #            winproc.killPid(p2.pid)
                winproc.kill_pro("InitiaPicServer.exe")
                p2=subprocess.Popen(["InitiaPicServer.exe"],creationflags=subprocess.CREATE_NEW_CONSOLE) 
                #p=subprocess.Popen(["start.bat"], shell=True,stdout=True) 
        
                #scout tomcat startup.bat java.exe
            if winproc.IsProcStarted("java.exe") == False:
                winproc.restart_pro("startup.bat")


        #restart InitiaPicServer_Pup.exe   
        if os.path.exists("InitiaPicServer_Pup.exe") == False:
            print("No InitiaPicServer_Pup.exe")
        else:
            ret3 =  1
            if type(p3) != type(1):
                ret3=subprocess.Popen.poll(p3)
            scoutdir = os.getcwd() + "\scoutdir\*.scout"
            list = glob.glob(scoutdir)
            #list = os.listdir(scoutdir)
            
            if ret3 is None:
                if(len(list) >= 30):
                    #winproc.killPid(p3.pid)
                    winproc.kill_pro("InitiaPicServer_Pup.exe")
                    p3=subprocess.Popen(["InitiaPicServer_Pup.exe"], startupinfo=startinfo,creationflags=subprocess.CREATE_NEW_CONSOLE) 
                pass
        #        print(datetime.now(),"the Initiative Programer is running!")
            elif len(list) > 0 :
                #print(datetime.now(),"InitiaPicServer_Pup has stoped,so it will restart")
    #            winproc.killPid(p3.pid)
    #            print("Start handle pup data...")
                winproc.kill_pro("InitiaPicServer_Pup.exe")
                p3=subprocess.Popen(["InitiaPicServer_Pup.exe"], startupinfo=startinfo,creationflags=subprocess.CREATE_NEW_CONSOLE) 
                #p=subprocess.Popen(["start.bat"], shell=True,stdout=True) 
    

        #restart WebMICAPSWatcher.exe
        if os.path.exists("WebMICAPSWatcher.exe") == False:
            print("No WebMICAPSWatcher.exe")
        else:
            
            ret4 =  1
            if type(p4) != type(1):
                ret4=subprocess.Popen.poll(p4)
            scoutdir = os.getcwd() + "\scoutdir\*.micaps"
            list = glob.glob(scoutdir)
            #list = os.listdir(scoutdir)
            
            if len(list) == 0:
                p4Counts += 1
            else:
                p4Counts = 0
                
            if iSleep*p4Counts  > 60*5:
                winproc.kill_pro("WebMICAPSWatcher.exe")
                p4=subprocess.Popen(["WebMICAPSWatcher.exe"], startupinfo=startinfo,creationflags=subprocess.CREATE_NEW_CONSOLE) 
    
                #winproc.killPid(p3.pid)
                
                #print("restart WebMICAPSWatcher.exe")


    
    '''    
        #hide the console UI
    if g_iPupProduct == 1:
        whnd = windll.kernel32.GetConsoleWindow()  
        if whnd != 0:  
            windll.user32.ShowWindow(whnd, 0)  
            windll.kernel32.CloseHandle(whnd) 
    
    iSleep = 60
    if g_iPupProduct == 0:
        p=subprocess.Popen(["InitiaPicServer.exe"], shell=True,stdout=True) 
    else:
        iSleep = 30
        p=subprocess.Popen(["InitiaPicServer_Pup.exe"], shell=True,stdout=True) 
    while 1:
        time.sleep(iSleep)
        ret=subprocess.Popen.poll(p)
        
        if g_iPupProduct == 0:
            if ret is None:
                pass
        #        print(datetime.now(),"the Initiative Programer is running!")
            else:
                print(datetime.now(),"it has stoped,so it will restart")
                p=subprocess.Popen(["InitiaPicServer.exe"], shell=True,stdout=True) 
                #p=subprocess.Popen(["start.bat"], shell=True,stdout=True) 
        else:
            if ret is None:
                pass
        #        print(datetime.now(),"the Initiative Programer is running!")
            else:
                print(datetime.now(),"Pup has stoped,so it will restart")
                p=subprocess.Popen(["InitiaPicServer_Pup.exe"], shell=True,stdout=True) 
                #p=subprocess.Popen(["start.bat"], shell=True,stdout=True) 
    '''
