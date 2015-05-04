import os,re,shlex
import subprocess


'''
STATE
1 STOPPED
2 START_PENDING
3 STOP_PENDING
4 RUNNING
'''

import winproc


def start_office(listPath):
    
    bRet = winproc.IsProcStarted("soffice.exe")
    if bRet:
        print("soffice have started")
        return
    
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
    
        
    if(os.path.exists(fullpath)):
       # commands = "soffice.exe -headless "" -accept "" -nofirststartwizard "socket,host=127.0.0.1,port=8100;urp;" "
        listPath.append(fullpath)
        print("find soffice path:",listPath)
        curDir = os.path.curdir
        #print(os.path.dirname(fullpath))
        os.chdir(os.path.dirname(fullpath))
        commands = '''soffice -headless -accept="socket,host=127.0.0.1,port=8100;urp;" -nofirststartwizard'''
        args = shlex.split(commands)
        try:
            subprocess.Popen(args, stdout=True) 
        except Exception as E:
            strInfo = str(E)
            print("start sofficee exception:  %s"%strInfo)
        os.chdir(curDir)
    else:
        print("haven't find soffice.exe")
#    C:\Program Files\OpenOffice.org 3\program\soffice.exe

if __name__ == '__main__':
    
    start_office()
