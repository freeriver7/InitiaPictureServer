
from xml.etree.ElementTree import ElementTree

class  configParser(object):
    version = 0.1
    
    def __init__(self,file):
        self.strDataType = ""
        self.tree = ElementTree()
        self.tree.parse(file)
        self.listDataBase = self.tree.findall("data")
        ppos = self.tree.find("data/datapath")
        print(ppos.get('datapath','no found'))
        self.load_xml_file(file)
        
        
    def load_xml_file(self,file):
        pass
            
    def get_config(self,iDataType = 1):
        
        if iDataType == 0:
            self.strDataType = "BJANC"
        elif iDataType == 1:
             self.strDataType = "RUC"  
        elif iDataType == 2:
             self.strDataType = "LAPS-HIGH"  
               
        for i in self.listDataBase:        
            if i.get('name','not find') == self.strDataType:
                print(i.get('name','not find'))
                return i.findtext("datapath")
                break
        else:
            print("not found")
            return ""
    
if __name__ == '__main__':

    config = configParser('ini\\datasearch.xml')
    config.get_config(2)
    
    
