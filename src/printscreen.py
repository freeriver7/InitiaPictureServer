#!coding=utf-8
import win32ui
import win32gui
import win32con
from pywin.mfc import  dialog
import os
import string
#from pyExcelerator import *
#from PIL import ImageGrab

#====Constant Definations=======================================
IDC_COMBOBOX_1 = 2034
IDC_COMBOBOX_2 = 2039
IDC_COMBOBOX_3 = 2036
IDC_COMBOBOX_4 = 2037

BMP_FILE_NAME = "CASE.BMP"
CURRENT_DIR='C:\\'
OPEN_TOOL='mspaint'
BMP_FILE=CURRENT_DIR + BMP_FILE_NAME;

def MakeLoginDlgTemplate(title):
    style = win32con.DS_MODALFRAME | win32con.WS_POPUP | win32con.WS_VISIBLE | win32con.WS_CAPTION | win32con.WS_SYSMENU | win32con.DS_SETFONT
    cs = win32con.WS_CHILD | win32con.WS_VISIBLE
    cs2= win32con.CBS_DROPDOWN | win32con.WS_VSCROLL | win32con.WS_TABSTOP
    
    #window frame and title
    dlg = [[title,(0,0,343,90),style,None,(10,"login dialog")],]
    
    dlg.append([130, "CASE NAME:", -1, (7, 9, 69, 9), cs | win32con.SS_LEFT])
    s = cs | win32con.WS_TABSTOP | win32con.WS_BORDER
    dlg.append(['COMBOBOX',None, IDC_COMBOBOX_1, (50, 7, 243,60), s| cs2|cs])

    dlg.append([130, "CASE NO:", -1, (7, 22, 69, 9), cs | win32con.SS_LEFT])
    s = cs | win32con.WS_TABSTOP | win32con.WS_BORDER
    dlg.append(['COMBOBOX', None, IDC_COMBOBOX_2, (50, 20, 243,50), s | cs2|cs])
    
    dlg.append([130, "CASE TYPE:", -1, (7, 33, 69, 9), cs | win32con.SS_LEFT])
    s = cs | win32con.WS_TABSTOP | win32con.WS_BORDER
    dlg.append(['COMBOBOX', None, IDC_COMBOBOX_3, (50, 33, 243,63), s | cs2|cs])
    #Window Name lable and text box
    dlg.append([130, "Window NAME:", -1, (7, 46, 69, 9), cs | win32con.SS_LEFT])
    s = cs | win32con.WS_TABSTOP | win32con.WS_BORDER
    dlg.append(['COMBOBOX',None, IDC_COMBOBOX_4, (50, 46, 243,76), s| cs2|cs])

    # OK/Cancel Buttons
    s = cs | win32con.WS_TABSTOP
    dlg.append([128, "OK", win32con.IDOK, (295, 5, 40, 14), s | win32con.BS_DEFPUSHBUTTON])
    s = win32con.BS_PUSHBUTTON | s
    dlg.append([128, "Kill", win32con.IDCANCEL, (295, 20, 40, 14), s])
    return dlg

class SelectDlg(dialog.Dialog):
    def __init__(self,title):
        dialog.Dialog.__init__(self,MakeLoginDlgTemplate(title))
        self.case_name = ''
        self.case_no = ''
        self.file_name = ''
        self.window_name = ''
        
    def OnInitDialog(self):
        rc =  dialog.Dialog.OnInitDialog(self)
        #init the element of the window
        self.combol1 = self.GetDlgItem(IDC_COMBOBOX_1)
        self.combol1.AddString("case 01")
        self.combol1.AddString("case 02")
        self.combol1.AddString("case 03")
        
        
        self.combol2 = self.GetDlgItem(IDC_COMBOBOX_2)
        for i in range(1,40):
            self.combol2.InsertString(i-1,"(case_" + string.zfill(str(i),3)+")")
        
        self.combol3 = self.GetDlgItem(IDC_COMBOBOX_3)
        self.combol3.InsertStrng(0,"_Input")
        self.combol3.InsertStrng(1,"_Ounput")
        
        self.combol4 = self.GetDlgItem(IDC_COMBOBOX_4)
        self.combol4.InsertString(0,'Window name')
        self.combol4.InsertString(1,'Window name2')
        #print(self.combol1.GetCount())
        return rc
    
    def OnOK(self):
        dialog.Dialog.OnOk(self)
    
if __name__ == "__main__":
    dlg = SelectDlg("")
    dlg.DoModal()
    print('this is main function')     
        
