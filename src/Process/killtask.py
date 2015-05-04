
#-------------------------------������killtask.py------------------------------------------------

import getopt
import winproc #winproc����ͬ��Ŀ¼�µ�winproc.py

procList2=[]
def lookproc():
    procList = winproc.getProcList()
    for proc in procList:
        #print(proc.szExeFile.decode('gbk')+'  '+str(proc.th32ParentProcessID) + '  '+str(proc.th32ProcessID))
        print(proc.szExeFile.decode('gbk')+'  '+str(proc.th32ProcessID))
        procList2.append([proc.szExeFile.decode('gbk'),proc.th32ProcessID])

if __name__ =='__main__':
    lookproc()
    while True:
        cmd = input('>>')
        if cmd=='exit':
            break
        elif cmd=='look':
            print('�鿴����')
            procList2=[]
            lookproc()
        elif cmd.isnumeric():
            pid = int(cmd)
            winproc.killPid(int(cmd))
            for proc in procList2:
                if pid == proc[1]:
                    print('�������̣�"'+proc[0]+'"\t'+str(pid))
        else:
            pid = 0
            for proc in procList2:
                #print('�ҵ�',proc[0],type(proc[0]))
                if proc[0].find(cmd) != -1:
                    pid = proc[1]
                    winproc.killPid(pid)
                    print('�������̣�"'+proc[0]+'"\t'+str(pid))
            if pid == 0:
                print('û���ҵ�"'+cmd+'"')
       
       
    #args = sys.argv
    #if len(args) >1 :
    #    pid = int(args[1])
    #    killPid(pid)
    #else:
    #    procList = getProcList()
    #    for proc in procList:
    #        print(str(proc.szExeFile)+'  '+str(proc.th32ParentProcessID) + '  '+str(proc.th32ProcessID))
    #        print(str(proc.