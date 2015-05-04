# -*- cp936 -*-

import os,math,time,sys
import win32com,shutil
import wordhelper
import win32ui,win32con
from win32com.client import Dispatch, constants

bendicaiji = 0
biaozycaiji = 1
gongzycaiji = 2
g_collectStyle = 3
g_iChanelNum = 4 #2 chanel machine or 4
#dicCaijiName = {bendicaiji : "bendicollect",biaozycaiji : "2collect",gongzycaiji : "3collect"}
dicCaijiName = {}
fileHandle = open("log.txt",'w')

g_listData = []


def sumAvg(list):
    sumAlpha = 0
    sumBeta  = 0
    iLen = int(len(list))
    if iLen <= 0:
        return 0
    for i in range(iLen):
        sumAlpha += int(list[i],10)
    sumAlpha = sumAlpha/iLen
    return sumAlpha



def sumRSD(list,avgA,avgB):
    sumAlpha = 0
    sumBeta  = 0
    iLen = int(len(list)/2)
    if iLen <= 1:
        return (sumAlpha,sumBeta)
    for i in range(iLen):
        sumAlpha += (int(list[2*i],10) - avgA)*(int(list[2*i],10) - avgA)
        sumBeta  += (int(list[2*i + 1],10) - avgB)*(int(list[2*i + 1],10) - avgB)
    sumAlpha = math.sqrt(sumAlpha/(iLen -1))
    sumBeta = math.sqrt(sumBeta/(iLen -1))
    return (sumAlpha*100,sumBeta*100)

def InitiaInfo(file,modelid):
    
    global g_listData
    global g_collectStyle
    content = open(file,"r")
    fileHandle.write(file)
    fileHandle.write("\n")
    for line in content:
        records = line.split("&")
        for singleRec in records:
            listCollect = singleRec.strip().split("|")
            if not listCollect or  len(singleRec) < 5 :
#                    print("the listCollect is empty()")
                continue
#            print(listCollect)
            print(listCollect[1])
            g_collectStyle = int(listCollect[1])
            if g_collectStyle > gongzycaiji:
                g_collectStyle = gongzycaiji
            del listCollect[1]
            print(listCollect)
            
            if modelid.strip() == listCollect[2].strip():
                g_listData = listCollect
                print("find it",g_listData,modelid)
                return
            else:
                continue
    

def GengerateWord(listCollectInfo):  
    global fileHandle
    '''
        generate word report
    '''
    print(os.getcwd())
    print(listCollectInfo)
    fileHandle.write("the select list is :\n")
    fileHandle.write(str(listCollectInfo))
    fileHandle.write("\n")
    dir = os.getcwd()
    
    

#    parentDir = dir[0:dir.rfind("\\")]
    parentDir = dir

    wordDir = "%s\\word"%parentDir
    templName = "templete_AlphaBeta.doc"
    templeteFile = "%s\\dist\\templete\\%s"%(dir,templName)
    fileHandle.write("word dir is:%s,templete is :%s\n"%(dir,templeteFile))
    
    if not os.path.exists(templeteFile):
        fileHandle.write("123")
        win32ui.MessageBox("123")
        sys.exit()
    if not os.path.exists(wordDir):
        os.mkdir(wordDir)

    templete =  "%s\\word\\templete.doc"%parentDir
    if os.path.exists(templete):
        os.remove(templete)
    shutil.copy(templeteFile,templete)
    
    try:
        w = win32com.client.Dispatch('Word.Application')
        # w = win32com.client.DispatchEx('Word.Application')
        
        w.Visible = 0
        w.DisplayAlerts = 0    
        
        doc = w.Documents.Open( FileName = templete)
        
        #myRange = doc.Range(0,0)
        #myRange.InsertBefore('Hello from Python!')
        
        #wordSel = myRange.Select()
        #wordSel.Style = constants.wdStyleHeading1
        
        w.Selection.Find.ClearFormatting()
        w.Selection.Find.Replacement.ClearFormatting()
        w.Selection.Find.Execute("shanghai", False, False, False, False, False, True, 1, True, "sh")
        
        #w.ActiveDocument.Sections[0].Headers[0].Range.Find.ClearFormatting()
        #w.ActiveDocument.Sections[0].Headers[0].Range.Find.Replacement.ClearFormatting()
        #w.ActiveDocument.Sections[0].Headers[0].Range.Find.Execute(OldStr, False, False, False, False, False, True, 1, False, NewStr, 2)
        
        
    #    doc.Tables[0].Rows[0].Cells[0].Range.Text ='123123'
        iindex = 0
        timeRec = listCollectInfo[iindex]
        timecurr = time.localtime(float(timeRec))
        timeRec = "%04d年%02d月%02d日 %02d:%02d"%(timecurr.tm_year,timecurr.tm_mon,timecurr.tm_mday,timecurr.tm_hour,timecurr.tm_min)
        
        iindex += 1
        shijian = listCollectInfo[iindex]
        iindex += 1
        modelid = listCollectInfo[iindex]
        iindex += 1
        t1jishulv = listCollectInfo[iindex][0:-1].split(",")
        print(t1jishulv)
        iindex += 1
        fanfuhe = listCollectInfo[iindex][0:-1].split(",")
        iindex += 1
        hesu = listCollectInfo[iindex]
        iindex += 1
        jishulv = float(listCollectInfo[iindex])/100
        
        fileHandle.write("\n")
        
        t1AvgAlpha = sumAvg(t1jishulv)
       
        maxrow = len(t1jishulv)
        print("maxrow is %d"%maxrow)
        iRow = 0
        for i in range(int(maxrow)):   
            print(i)    
            iRow = i+1
            doc.Tables[0].Rows.Add()
            
            doc.Tables[0].Rows[i+1].Cells[0].Range.Text = str(i+1)
            if len(t1jishulv) < i + 1 :
                doc.Tables[0].Rows[i+1].Cells[1].Range.Text = ""
                doc.Tables[0].Rows[i+1].Cells[2].Range.Text = ""
            else:
                doc.Tables[0].Rows[i+1].Cells[1].Range.Text = t1jishulv[i]
                doc.Tables[0].Rows[i+1].Cells[2].Range.Text = fanfuhe[i]
                
        doc.Tables[0].Rows.Add() 
        iRow += 1
        doc.Tables[0].Rows[iRow].Cells[0].Range.Text = "平均值"
        doc.Tables[0].Rows[iRow].Cells[1].Range.Text = "%.2f"%t1AvgAlpha
        doc.Tables[0].Rows.Add() 
        iRow += 1
        doc.Tables[0].Rows[iRow].Cells[0].Range.Text = "活度"
        doc.Tables[0].Rows[iRow].Cells[1].Range.Text = "%.2f"%jishulv

        #doc.PrintOut()
        
        #update orther
        wordhelper.MS_Word_Find_Replace(w, "clrq", timeRec)
        wordhelper.MS_Word_Find_Replace(w, "clsj", "%s 秒"%shijian)
        wordhelper.MS_Word_Find_Replace(w, "clcs", int(maxrow))
        wordhelper.MS_Word_Find_Replace(w, "xuhao", modelid)
        
#        str = "picture+server+1"
        voltage = " V"
        strhesu = hesu
        hesuname = hesu
        if strhesu.find("~") != -1:
            strhesu = strhesu.split("~")
            hesuname = strhesu[0]
            voltage  = "%s V"%(strhesu[1])   
        else:
            hesuname = strhesu
        print(hesuname,voltage)

        wordhelper.MS_Word_Find_Replace(w, "clhs", hesuname)
        wordhelper.MS_Word_Find_Replace(w, "cldy", voltage)
    
        fileGenerate = "%s\\word\\%s.doc"%(parentDir,modelid)
        if os.path.exists(fileGenerate):
    #        ret = win32ui.MessageBox("11",win32con.MB_YESNO)
            ret = 6
            if  ret == 6:
                os.remove(fileGenerate)
                w.ActiveDocument.SaveAs(fileGenerate)
        else:
             w.ActiveDocument.SaveAs(fileGenerate)
            
        # doc.Close()
    #    w.Documents.Open( FileName = "%s\\word\\%s.doc"%(dir,modelid))
    except Exception as e:
        fileHandle.write(str(e))
        fileHandle.write("\n")
    w.Documents.Close()
    w.Quit()
    os.remove(templete)
    os.system(fileGenerate)
    
if __name__ == "__main__":

#    if 2 > 1:
#        tuple = ('1336141069', '5', '201205042217', '51,0,51,0,51,0,51,0,51,0,51,0,', '51,0,51,0,51,0,51,0,51,0,51,0,', '51,0,51,0,51,0,51,0,51,0,51,0,', '51,0,51,0,51,0,51,0,51,0,51,0,', '10.00,10.00,1.00', '10.00,10.00,1.00', '10.00,10.00,1.00', '10.00,10.00,1.00', '0,0,0,0,0,0,0,0,', '408,408,408,408,408,408,')
#        listData = list(tuple)
#        GengerateWord(listData)
#        print("OK")
#        sys.exit()
    i = 100
    print("test")
    print("hello")
    if  False:
        
        InitiaInfo("20120916123226_alphabeta.txt","201209160934")
        
        print(g_listData)
        fileHandle.write("%s\n"%g_collectStyle)
        if len(g_listData) > 0:
            GengerateWord(g_listData)
        else:
            print("cann't find the mordel id in the file!")    
    
    if  len(sys.argv) == 2:
        file = sys.argv[1]
        if file.endswith(".doc") or file.endswith(".docx"):
            if os.path.exists(file):
                os.system(file)
    elif  len(sys.argv) == 3:
        print(sys.argv[0])
        print(sys.argv[1])
        print(sys.argv[2])
        
        fileHandle.write("3 argument\n")
        fileHandle.write(sys.argv[1])
        fileHandle.write("\n")
        fileHandle.write(sys.argv[2])
        fileHandle.write("\n")
        InitiaInfo(sys.argv[1],sys.argv[2])

    #    tuple = ('1336141069', '5', '201205042217', '51,0,51,0,51,0,51,0,51,0,51,0,', '51,0,51,0,51,0,51,0,51,0,51,0,', '51,0,51,0,51,0,51,0,51,0,51,0,', '51,0,51,0,51,0,51,0,51,0,51,0,', '10.00,10.00,1.00', '10.00,10.00,1.00', '10.00,10.00,1.00', '10.00,10.00,1.00', '0,0,0,0,0,0,0,0,', '408,408,408,408,408,408,')
    #    listData = list(tuple)
        if len(g_listData) > 0:                                                                                                                                                                                                                                         
            GengerateWord(g_listData)
        else:
            fileHandle.write("g_listData is empty!\n")
            print("cann't find the mordel id in the file!")
    
        print("OK")
    else:
        print("invalid argument")
    fileHandle.close()