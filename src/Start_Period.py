# -*- conding:utf-8 -*-

import subprocess
import re
import random
from datetime import datetime 
import sys,os
import time
from ctypes import *




if __name__ == '__main__':
        
    #p=subprocess.call(["python", "InitiativePic_singleThread.py"])
    '''
    whnd = windll.kernel32.GetConsoleWindow()  
    if whnd != 0:  
        windll.user32.ShowWindow(whnd, 0)  
        windll.kernel32.CloseHandle(whnd) 
    '''
        
    timeNow = time.localtime() 
    g_timeLatest = timeNow.tm_hour
    p=subprocess.Popen(["start.bat"], shell=True,stdout=True) 
    while 1:
        time.sleep(2)
        timeNow = time.time()
        ret=subprocess.Popen.poll(p)
        if ret is None:
            pass
    #        print(datetime.now(),"the Initiative Programer is running!")
        else:
            timeNow = time.localtime() 
            if timeNow.tm_min > 30 and timeNow.tm_min < 40 and timeNow.tm_hour != g_timeLatest:
                g_timeLatest = timeNow.tm_hour
                #print(datetime.now(),"it has stoped,so it will restart")
                p=subprocess.Popen(["start.bat"], shell=True,stdout=True) 
