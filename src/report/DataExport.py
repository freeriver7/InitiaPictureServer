
# -*- coding: utf-8 -*-  
#sqlserver to handle chapter 13

#ctrl + f10  show line numbers

from ctypes import *  
import win32ui
import win32api
import win32con
import os
from pywin.mfc import dialog

IDC_COMBO_PORT = 2000
IDC_COMBO_BAUD = 2001
IDC_COMBO_BITS = 2002
IDC_COMBO_TEST = 2003
IDC_COMBO_STOP = 2004
ID_BTN_READ     = 2005
ID_BTN_OPEN     = 2006
IDC_STATIC_STATUS = 2007
IDC_STATIC_READ = 2008

dll = CDLL("SerialPort.dll")  

def MakePictureServerDlgTemplate(title):
    style = win32con.DS_SETFONT | win32con.DS_MODALFRAME | win32con.DS_FIXEDSYS | win32con.WS_POPUP | win32con.WS_VISIBLE | win32con.WS_CAPTION | win32con.WS_SYSMENU
    cs = win32con.WS_CHILD | win32con.WS_VISIBLE
    listCs = cs | win32con.LBS_NOINTEGRALHEIGHT | win32con.WS_VSCROLL | win32con.WS_TABSTOP
    # Window frame and title
#    dlg = [ [title, (0, 0, 467, 334), style, None, (8, "MS Sans Serif")], ]
    dlg = [ [title, (0, 0, 321, 168), style, None, (8, "MS Sans Serif")], ]

    # ID label and text box
    dlg.append([130, "波特率:", -1, (173, 15, 36, 13), cs | win32con.SS_LEFT])
    dlg.append([130, "串口号:", -1, (36,15,36,13), cs | win32con.SS_LEFT])
    dlg.append([130, "校验位:", -1, (36,36,36,13), cs | win32con.SS_LEFT])
    dlg.append([130, "数据位:", -1, (173, 36, 36, 13), cs | win32con.SS_LEFT])
    dlg.append([130, "停止位:", -1, (36, 59, 36, 13), cs | win32con.SS_LEFT])
    dlg.append([130, "串口状态:", -1, (173, 59, 36, 13), cs | win32con.SS_LEFT])
    dlg.append([130, "读取状态:", -1, (37,86,36,13), cs | win32con.SS_LEFT])
    dlg.append([130, "关闭", IDC_STATIC_STATUS, (218,59,36,13), cs | win32con.SS_LEFT])
    dlg.append([130, "等值读取", IDC_STATIC_READ, (83,85,55,13), cs | win32con.SS_LEFT])
    
    s = cs | win32con.CBS_DROPDOWN | win32con.WS_VSCROLL | win32con.WS_TABSTOP
    
    dlg.append(['COMBOBOX', None, IDC_COMBO_PORT, (77,16,62,56), s])
    dlg.append(['COMBOBOX', None, IDC_COMBO_BAUD, (216,16,62,72), s])
    dlg.append(['COMBOBOX', None, IDC_COMBO_BITS, (216,37,62,55), s])
    dlg.append(['COMBOBOX', None, IDC_COMBO_TEST, (77,37,62,55), s])
    dlg.append(['COMBOBOX', None, IDC_COMBO_STOP, (77,60,62,69), s])

    # OK/Cancel Buttons
    s = cs | win32con.WS_TABSTOP     
    dlg.append([128, "读取数据", ID_BTN_READ, (250,116,53,23), s | win32con.BS_DEFPUSHBUTTON])
    dlg.append([128, "打开端口", ID_BTN_OPEN, (189,116,53,23), s | win32con.BS_DEFPUSHBUTTON])
    s = win32con.BS_PUSHBUTTON | s
    dlg.append([128, "退出", win32con.IDCANCEL, (54,129,40,23), s])

    return dlg


class DataReadDlg(dialog.Dialog):
        
    def __init__(self, title):  
              
        dialog.Dialog.__init__(self, MakePictureServerDlgTemplate(title))
        
        
        
    def OnInitDialog(self):
        rc = dialog.Dialog.OnInitDialog(self)
        #init the element of the window
        self.bInitPort = False
        
        self.cbxPort = self.GetDlgItem(IDC_COMBO_PORT)
        for i in range(1,9):
            self.cbxPort.AddString(str(i))
        self.cbxPort.SetCurSel(0)
        
        self.cbxBaud = self.GetDlgItem(IDC_COMBO_BAUD)
        self.cbxBaud.AddString("4800")
        self.cbxBaud.AddString("9600")
        self.cbxBaud.AddString("19200")
        self.cbxBaud.AddString("38400")
        self.cbxBaud.AddString("57600")
        self.cbxBaud.AddString("115200")
        self.cbxBaud.SetCurSel(2)

        self.cbxTest = self.GetDlgItem(IDC_COMBO_TEST)
        self.cbxTest.AddString("偶校验")
        self.cbxTest.AddString("奇校验")
        self.cbxTest.AddString("无校验")
        self.cbxTest.SetCurSel(2)
        
        self.cbxBits = self.GetDlgItem(IDC_COMBO_BITS)
        for i in range(5,9):
            self.cbxBits.AddString(str(i))
        self.cbxBits.SetCurSel(3)
        
        self.cbxStop = self.GetDlgItem(IDC_COMBO_STOP)
        self.cbxStop.AddString("1")
        self.cbxStop.AddString("2")
        self.cbxStop.SetCurSel(0)
        
        
        self.lblPortStates = self.GetDlgItem(IDC_STATIC_STATUS)
        self.btnOpenPort = self.GetDlgItem(ID_BTN_OPEN)
        self.btnReadData = self.GetDlgItem(ID_BTN_READ)
        #print(self.combol1.GetCount())
        self.HookCommand(self.OnPenPort, ID_BTN_OPEN)
        self.HookCommand(self.OnReadData, ID_BTN_READ)
        
        return rc
    
    def OnReadData(self,cid,code):
        if  code == win32con.BN_CLICKED:
            iRead = dll.ReadData()
            if iRead >= 0:
                win32ui.MessageBox("数据成功导出！","提示")
            else:
                win32ui.MessageBox("数据导出失败！","提示")
            
            print("OK")
    def OnPenPort(self,cid,code):
        if  code == win32con.BN_CLICKED:
            print("open portOK")
            
        if self.bInitPort:
            self.btnOpenPort.SetWindowText("打开串口")
            self.lblPortStates.SetWindowText("关闭")
            self.bInitPort = False
#            dll.StopMonitoring()
            return
        
        m_nPort = self.cbxPort.GetCurSel();
        if m_nPort < 0:
            return
        m_nBard = 19200
        n = self.cbxBaud.GetCurSel() 
        if  n == 0:
            m_nBard = 4800
        elif n == 1:
            m_nBard = 9600
        elif n == 2:
            m_nBard = 19200
        elif n == 3:
            m_nBard = 38400
        elif n == 4:
            m_nBard = 57600
        elif n == 5:
            m_nBard = 115200

        Test = ""
        n = self.cbxTest.GetCurSel()
        if  n == 0:
            Test = 'O'
        elif n == 1:
           Test = 'E'
        elif n == 2:
           Test = 'N'

        m_nBits = 0
        n = self.cbxBits.GetCurSel()
        if  n == 0:
            m_nBits = 5
        elif n == 1:
           m_nBits = 6
        if  n == 2:
            m_nBits = 7
        elif n == 3:
           m_nBits = 8
           
        n = self.cbxStop.GetCurSel()
        m_nStop = 1 if n == 0 else 2
        print("port:%d,bard:%d,Test:%s,bits:%d,stop:%d"%(m_nPort,m_nBard,Test,m_nBits,m_nStop))
        r = dll.InitPort(None, m_nPort + 1, m_nBard )

#        r = dll.init_port(m_nPort, m_nBaud, Test, m_nBits, m_nStop);
        if r < 0:
            win32ui.MessageBox("打开串口失败！","提示")
        else:
            self.btnOpenPort.SetWindowText("关闭串口")
            self.btnReadData.EnableWindow(True)
            self.lblPortStates.SetWindowText("打开")
            dll.StartMonitoring()
            self.bInitPort = True
            print("open port successfully!")

            
if __name__ == "__main__":
    picDlg = DataReadDlg("数据读取")
    picDlg.DoModal()

  