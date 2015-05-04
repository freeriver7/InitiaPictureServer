# -*- coding: utf-8 -*-

# -*- coding: cp936 -*-

#############################################
#   Written By Qian_F                        #     
#   2013-08-10                               #
#   获取文件路径列表，并写入到当前目录生成test.txt #
#############################################

import os
import os

DIR = ""

def compare(x, y):
    global DIR
    stat_x = os.stat(DIR + "/" + x)
    stat_y = os.stat(DIR + "/" + y)
    if stat_x.st_ctime < stat_y.st_ctime:
        return -1
    elif stat_x.st_ctime > stat_y.st_ctime:
        return 1
    else:
        return 0

def getfilelist(latestFile,filepath, tabnum=1):
    
    simplepath = os.path.split(filepath)[1]
    returnstr = simplepath+"目录<>"+"\n"
    returndirstr = ""
    returnfilestr = ""

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
            latestFile[filepath] = files[0]
            break
            #returnfilestr += "\t"*tabnum+filename+"\n"
    #returnstr += returnfilestr+returndirstr
    #return returnstr+"\t"*tabnum+"</>\n"
            

path = "c:\\aaa"
path = "C:\\aaa\\output\\cache\\ANI_IR1_R04_20140527_1400_FY2E.AWX_100x100\\501567\\7\\16"
usefulpath = path.replace('\\', '/')
if usefulpath.endswith("/"):
    usefulpath = usefulpath[:-1]
if not os.path.exists(usefulpath):
    print("error path ",usefulpath)
elif not os.path.isdir(usefulpath):
    print("not dir")
else:
    latestFile = {}
    getfilelist(latestFile,usefulpath)
    print(latestFile)

    '''
    filelist = os.listdir(usefulpath)
    o=open("test.xml","w+")
    o.writelines(getfilelist(usefulpath))
    o.close()
    '''
    print("ok")