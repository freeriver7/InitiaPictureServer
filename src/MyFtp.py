#!/usr/bin/python
#coding=gbk
'''
    ftp�Զ����ء��Զ��ϴ��ű������Եݹ�Ŀ¼����
'''

from ftplib import FTP
import os,sys,string,datetime,time
import socket,re

class MYFTP:
    def __init__(self, hostaddr, username, password, remotedir, port=21):
        self.hostaddr = hostaddr
        self.username = username
        self.password = password
        self.remotedir  = remotedir
        self.port     = port
        self.ftp      = FTP()
        self.file_list = []
        # self.ftp.set_debuglevel(2)
    def __del__(self):
        self.ftp.close()
        # self.ftp.set_debuglevel(0)
    def login(self):
        ftp = self.ftp
        try: 
            timeout = 60
            socket.setdefaulttimeout(timeout)
            ftp.set_pasv(True)
            print( '��ʼ���ӵ� %s' %(self.hostaddr))
            ftp.connect(self.hostaddr, self.port)
            print('�ɹ����ӵ� %s' %(self.hostaddr))
            print ('��ʼ��¼�� %s' %(self.hostaddr))
            ftp.login(self.username, self.password)
            print ('�ɹ���¼�� %s' %(self.hostaddr))
            debug_print(ftp.getwelcome())
        except Exception:
            deal_error("���ӻ��¼ʧ��")
        try:
            ftp.cwd(self.remotedir)
        except(Exception):
            deal_error('�л�Ŀ¼ʧ��')
    def makedir(self,dir):
        return self.ftp.mkd(dir)
    
    def is_same_size(self, localfile, remotefile):
        try:
            remotefile_size = self.ftp.size(remotefile)
        except:
            remotefile_size = -1
        try:
            localfile_size = os.path.getsize(localfile)
        except:
            localfile_size = -1
        debug_print('lo:%d  re:%d' %(localfile_size, remotefile_size),)
        if remotefile_size == localfile_size:
             return 1
        else:
            return 0
    def download_file(self, localfile, remotefile):
        if self.is_same_size(localfile, remotefile):
             debug_print('%s �ļ���С��ͬ����������' %localfile)
             return
        else:
            debug_print('>>>>>>>>>>>>�����ļ� %s ... ...' %localfile)
        #return
        file_handler = open(localfile, 'wb')
        self.ftp.retrbinary('RETR %s'%(remotefile), file_handler.write)
        file_handler.close()

    def download_files(self, localdir='./', remotedir='./'):
        try:
            self.ftp.cwd(remotedir)
        except:
            debug_print('Ŀ¼%s�����ڣ�����...' %remotedir)
            return
        if not os.path.isdir(localdir):
            os.makedirs(localdir)
        debug_print('�л���Ŀ¼ %s' %self.ftp.pwd())
        self.file_list = []
        self.ftp.dir(self.get_file_list)
        remotenames = self.file_list
        #print(remotenames)
        #return
        for item in remotenames:
            filetype = item[0]
            filename = item[1]
            local = os.path.join(localdir, filename)
            if filetype == 'd':
                self.download_files(local, filename)
            elif filetype == '-':
                self.download_file(local, filename)
        self.ftp.cwd('..')
        debug_print('�����ϲ�Ŀ¼ %s' %self.ftp.pwd())
    def upload_file(self, localfile, remotefile):
        if not os.path.isfile(localfile):
            return
        if self.is_same_size(localfile, remotefile):
             debug_print('����[���]: %s' %localfile)
             return
        file_handler = open(localfile, 'rb')
        self.ftp.storbinary('STOR %s' %remotefile, file_handler)
        file_handler.close()
        debug_print('�Ѵ���: %s' %localfile)
    def upload_dir(self, localdir='./', remotedir = './'):
        if not os.path.isdir(localdir):
            return
        localnames = os.listdir(localdir)
        self.ftp.cwd(remotedir)
        for item in localnames:
            src = os.path.join(localdir, item)
            if os.path.isdir(src):
                try:
                    self.ftp.mkd(item)
                except:
                    debug_print('Ŀ¼�Ѵ��� %s' %item)
                self.upload_files(src, item)
            else:
                self.upload_file(src, item)
        self.ftp.cwd('..')

    def ClearPictPeriodly(self,iDay = 10):
        
        currentTime = datetime.datetime.now()
        currentDay = currentTime.day
        #notice
        #if currentDay != 1 or currentTime.hour >= 2:
        #   return
        
        #strtemp = "ACHN.CREF000.20130124.080000.latlon_100x100"

        list =  self.ftp.nlst()
        print(list)
        for file in list:
#            self.ftp.sendcmd('rm -rf %s'%file)
            print("%s"%file)
            
            m = re.search('\d{8,14}',file)
            print(m.group()[0:4])
            
            dtNow = datetime.datetime.now() 
            dateFile = datetime.datetime(int(m.group()[0:4]),int(m.group()[4:6]),int(m.group()[6:8]))
            dateFile += datetime.timedelta(days=iDay) 
            if dateFile >= dtNow:
                continue

            self.ftp.cwd(file)
            listPng = self.ftp.nlst()            
            #timecurr = time.localtime(os.stat(listPng).st_ctime)
            for png in listPng:
                self.ftp.delete(png)
            self.ftp.cwd("..")
            self.ftp.voidcmd('RMD ' + file)
            
    
    
    def get_file_list(self, line):
        ret_arr = []
        print("line:",line)
        file_arr = self.get_filename(line)
        if file_arr[1] not in ['.', '..']:
            self.file_list.append(file_arr)
            
    def get_filename(self, line):
        pos = line.rfind(':')
        while(line[pos] != ' '):
            pos += 1
        while(line[pos] == ' '):
            pos += 1
        file_arr = [line[0], line[pos:]]
        return file_arr
def debug_print(s):
    print (s)
def deal_error(e):
    timenow  = time.localtime()
    datenow  = time.strftime('%Y-%m-%d', timenow)
    logstr = '%s ��������: %s' %(datenow, e)
    debug_print(logstr)
    file.write(logstr)
    sys.exit()

if __name__ == '__main__':
    file = open("log.txt", "a")
    timenow  = time.localtime()
    datenow  = time.strftime('%Y-%m-%d', timenow)
    logstr = datenow
    # �������±���
    hostaddr = "10.28.17.224"
    username = "iphone"
    password = "ip123"
    port  =  21   
    rootdir_remote = './'     
    port  =  21   # �˿ں� 
    rootdir_remote = './'          # Զ��Ŀ¼
    
    f = MYFTP(hostaddr, username, password, rootdir_remote, port)
    f.login()
#    f.makedir("humignfu")
    picPath = "F:\\Output1\\cache\\ACHN.CREF000.20120629.003000.latlon_100x100\\ACHN.CREF000.20120629.003000.latlon.png"
    basename = os.path.basename(picPath)
    basename = basename[0:-4]# remove .png
    ftpDir = "%s/%s_100x100"%(rootdir_remote,basename)
    #f.makedir("%s"%(ftpDir))
    #f.upload_file(picPath,"%s/%s"%(ftpDir,os.path.split(picPath)[1]))

    f.ClearPictPeriodly()
    file.close()
