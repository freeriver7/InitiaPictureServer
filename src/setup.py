# -*- coding: utf-8 -*-  
'''
description:
python32 to exe
the step:
D:\work\AIW\webmicaps\InitiaPictureServer\src
cxfreeze InitiaPicServer.py --target-dir dist --base-name=win32gui 
cxfreeze WebMICAPSWatcher.py --target-dir dist --base-name=win32gui 
cxfreeze LightningMerge.py --target-dir dist --base-name=win32gui 
cxfreeze StartPeriodical.py --target-dir dist
cxfreeze ScoutDir.py --target-dir dist
copy /Y dist\InitiaPicServer.exe D:\work\AIW\qgis-1.4.0_server\bin
'''

from cx_Freeze import setup, Executable
import sys  
import re
import traceback
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
name = "FtpTool",  
version = "1.0",
description = "rock game",
executables = [Executable("InitiativePic_singleThread.py",base = "Win32GUI",icon = "app.ico")])