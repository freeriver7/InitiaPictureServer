
# -*- coding: utf-8 -*-  
#sqlserver to handle chapter 13

#ctrl + f10  show line numbers

from ctypes import *  
import win32ui
import win32api
import win32con
import os
import sqlite3
import UserStruct
from pywin.mfc import dialog
from xmlhelper import configParser

dictDataType = UserStruct.getdatatypedic()
'''
dictDataType = {'TYPE_SWAN_RADAR3DPT': 0, 'TYPE_SWAN_TITAN': 1, 'TYPE_SWAN_COTRECWIND': 2, 'TYPE_SWAN_RADARPUP': 3,
				'TYPE_SWAN_CLOUD': 0, 'TYPE_SWAN_QPE': 1, 'TYPE_SWAN_QPF': 2, 'TYPE_SWAN_VWP': 3,
				'TYPE_SWAN_STM': 0}
'''

dll = CDLL("PictureFactoryPlugin.dll")  


IDC_COMBOX_DATATYPE = 2000
IDC_LIST_FILE = 2001   
IDC_LIST_ELEMENT = 2002   
IDC_LIST_LEVEL = 2003

listResolution = [
		-1,
		0.4791950593725079, #1
		0.23959752968625395,#2
		0.119798764843127,  #3
		0.05989938242156348, #4
		0.02994969121078175, #5
		0.014974845605390875, #6
		0.007487422802695426, #7
		0.0037437114013477244, #8
		0.0018718557006738622, #9
		7.487422802695448E-4, #10
		3.743711401347724E-4  #11
	]

def MakePictureServerDlgTemplate(title):
	style = win32con.DS_SETFONT | win32con.DS_MODALFRAME | win32con.DS_FIXEDSYS | win32con.WS_POPUP | win32con.WS_VISIBLE | win32con.WS_CAPTION | win32con.WS_SYSMENU
	cs = win32con.WS_CHILD | win32con.WS_VISIBLE
	listCs = cs | win32con.LBS_NOINTEGRALHEIGHT | win32con.WS_VSCROLL | win32con.WS_TABSTOP
	# Window frame and title
	dlg = [ [title, (0, 0, 467, 334), style, None, (8, "MS Sans Serif")], ]

	# ID label and text box
	dlg.append([130, "数据类型:", -1, (15, 17, 42, 14), cs | win32con.SS_LEFT])
	s = cs | win32con.CBS_DROPDOWN | win32con.WS_VSCROLL | win32con.WS_TABSTOP
	dlg.append(['COMBOBOX', None, IDC_COMBOX_DATATYPE, (68, 15, 105, 68), s])
	dlg.append(['LISTBOX', None, IDC_LIST_FILE, (15, 41, 157, 145), listCs])

	
	dlg.append([130, "元素:", -1, (18, 199, 34, 8), cs | win32con.SS_LEFT])
	dlg.append(['LISTBOX', None, IDC_LIST_ELEMENT, (17, 216, 67, 99), listCs])
	dlg.append([130, "层次:", -1, (121, 200, 24, 8), cs | win32con.SS_LEFT])
	dlg.append(['LISTBOX', None, IDC_LIST_LEVEL, (105, 216, 67, 99), listCs])

	# OK/Cancel Buttons
	s = cs | win32con.WS_TABSTOP 
	dlg.append([128, "OK", win32con.IDOK, (327, 300, 50, 14), s | win32con.BS_DEFPUSHBUTTON])
	s = win32con.BS_PUSHBUTTON | s
	dlg.append([128, "Cancel", win32con.IDCANCEL, (391, 299, 50, 14), s])
	return dlg


class PictureServerDlg(dialog.Dialog):
		
	def __init__(self, title):  
		      
		dialog.Dialog.__init__(self, MakePictureServerDlgTemplate(title))
		self.config = configParser('..\\ini\\datasearch.xml')
		
		
	def OnInitDialog(self):
		rc = dialog.Dialog.OnInitDialog(self)
		#init the element of the window
		self.cbxFileType = self.GetDlgItem(IDC_COMBOX_DATATYPE)
		for i in dictDataType.keys():
			self.cbxFileType.AddString(i)
		self.cbxFileType.SetCurSel(0)
		path = self.config.get_config(1)
		listFiles = os.listdir(path)
		
	
		self.lbxFile = self.GetDlgItem(IDC_LIST_FILE)
		for i in listFiles:
			self.lbxFile.AddString(i)
		
		self.lbxElement = self.GetDlgItem(IDC_LIST_ELEMENT)
		self.lbxElement.AddString("reflectivity")
		self.lbxElement.AddString("CR")
		self.lbxElement.AddString("CAPPI")
		self.lbxElement.AddString("VIL")
		
		self.lbxLevel = self.GetDlgItem(IDC_LIST_LEVEL)
		for i in range(500,6000,1000):			
			self.lbxLevel.AddString(str(i))
		#print(self.combol1.GetCount())
		self.HookCommand(self.OnDataTypeChaned, IDC_COMBOX_DATATYPE)
		
#		init database which indicate the files have generated  pictures or not	
#		conn = sqlite3.connect('pictures.db')
#		cur = conn.cursor()
#		cur.execute('CREATE TABLE PictureInfo (time INTEGER PRIMARY KEY, file VARCHAR(100), rects VARCHAR(200))')
#		conn.commit()
#		cur.execute('INSERT INTO PictureInfo (time, file, rects) VALUES(20120212, "apple", "12,28,32")')
#		conn.commit()
#		print(cur.lastrowid)

#		cur.execute('SELECT * FROM PictureInfo')
#		print(cur.fetchall())
		return rc
	
	def OnDataTypeChaned(self, cid, code):
		if code == win32con.CBN_SELCHANGE:
			text = self.GetDlgItemText(cid).upper()
			path = self.config.get_config(dictDataType[text])
			os.chdir(path)
			print(text)
#			self.FillListBox(text)
		return 1
	def  OnOK( self):
		print(dll.addtest(3, 4))
		rootDir = "D:\\work\\AIW\\testdata\\SWAN\\Swan090811\\radar\\test"
		list = os.listdir(rootDir)
		for	dir in list:
			listfile = os.listdir("%s\\%s"%(rootDir,dir))
			filename = "%s\\%s\\%s"%(rootDir,dir,listfile[0])
			print(filename)
			break
			
		
		print("this is 3DPT") 	
		filename = "d:\\work\\AIW\\testdata\\SWAN\\Swan090811\\radar\\Products\\北京SA\\CR\\38\\20120520.035859.00.37.931"
#		filename = "D:\\work\\AIW\\testdata\\SWAN\\Swan090811\\ncrad\\TDPRODUCT\\MCR\\Z_OTHE_RADAMOSAIC_20120305030000.bin.bz2"
#		pFile = c_char_p(b"D:\\work\\AIW\\testdata\\SWAN\\Swan090811\\ncrad\\TDPRODUCT\\MCR\\Z_OTHE_RADAMOSAIC_20120305030000.bin.bz2")
#		pFile 	 = c_char_p(filename.encode("gbk"))
#		pFile    = c_char_p(filename.encode("gbk")) 
#		pFile 	 = c_char_p(b"Z_RADR_I_Z9010_20120416005400_O_DOR_SA_CAP.bin.bz2")
		pFile 	 = create_string_buffer(filename.encode("gb2312"),512) 
		pElement = c_char_p(b"reflective")  
		pSaveDir = c_char_p(b"C:\\aaa\\output")  
		dll.setLowHeightResolution(2,9)
#		dResolution = c_double(0.02994969121078175) 
#		dResolution = c_double(-1.0) 
		fLevel = c_float(1.0)
		iType = c_int(17)		
		rectView = (c_float *4)(117.85,26.8029,123.226,29.4834)
		for i in range(5,6):
			dll.GetDataPicture(pFile,pElement,fLevel,c_double(-1.0) ,rectView,iType,c_int(0),c_int(255),c_int(300),c_int(600),pSaveDir) 



if __name__ == "__main__":
	picDlg = PictureServerDlg("")
	picDlg.DoModal()

