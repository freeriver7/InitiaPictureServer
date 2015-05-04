
#get the file unique type by file name 
def getTypeByName(filename,dicInitiaType):
    
    for key in dicInitiaType.keys():
        if filename.find(key) != -1:
                return dicInitiaType[key]
    return -1

'''
 class UserData:
     def ini(self):
         self.file = ""
         self.element = ""
         self.fLevel = 1.0
         self.dScale = -1.0
         self.arrCurScreen = get_double
         self.iFileType = 14
         self.iElementDeriveType = 0
         self.iTransparent = 128
         self.iWidth = 800
         self.iHeight = 600
         self.strSaveDir = 'C:\\aaa\\output'
'''
