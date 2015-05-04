# -*- conding:utf-8 -*-

import subprocess
import re
import random
from datetime import datetime 
import sys
import time
p=subprocess.call(["python", "InitiaPicServer.py"])
#p=subprocess.Popen(["InitiativePic_singleThread.exe"], shell=True,stdout=True) 
while 1:
    time.sleep(60)
    ret=subprocess.Popen.poll(p)
    if ret is None:
        pass
#        print(datetime.now(),"the Initiative Programer is running!")
    else:
        print(datetime.now(),"it has stoped,so it will restart")
#        p=subprocess.Popen(["InitiativePic_singleThread.exe"], shell=True,stdout=True)
        p=subprocess.call(["python", "InitiaPicServer.py"]) 