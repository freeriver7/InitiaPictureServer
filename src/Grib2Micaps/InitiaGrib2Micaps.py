
# -*- coding: utf-8 -*-  

g_dictGrphType = {"ProbabilityGrh" : 0,"AverageGrh" : 1,"NoodleGrh" : 2,"StampleGrh" : 3,"SingleStationGrh" : 4}
g_dictT213GrhProducts = {"ProbabilityGrh" : [],"AverageGrh" : [],"NoodleGrh" : [],"StampleGrh" : [],"SingleStationGrh" : []}
g_dictECMWFGrhProducts = {"ProbabilityGrh" : [],"AverageGrh" : [],"NoodleGrh" : [],"StampleGrh" : [],"SingleStationGrh" : []}
g_mapT213Ele2FileName = {}
g_mapECMWFEle2FileName = {}

class GraphType(object):
    "Ensemble GraphType:Propobility,Average,Noodle,Stample,SingleStation"
    def __init__(self):
        self.element = ""
        self.products = []
        self.nameTemplate = ""
        
def OperatorParser(strProduct):
    "parse operator"
    strProduct.strip()
    
    operator = ""
    
    if  str.find("=") != -1:
        operator = strProduct[0:2]
        if operator == ">="
    elif str.fin 
        
        
    pass
        
def InitiaGenPicture():
    
    "InitiaConfig.ini"
    print("open initia config file %s"%"InitiaConfig.ini")
    file = open("InitiaConfig.ini")
    grhType = ""
    dataType = ""
    
    for line in file.readlines():
        line = line.strip()
        if not line :
            continue
        
        if line[0] == '#':
            print(line)
        if line[0] == '{' and line[-1] == '}':
            dataType = line[1:-1]
            continue
            
        if line[0] == '[' and line[-1] == ']':
            grhType = line[1:-1]
        else:
            listEle = line.split("=")
            element=listEle[0]
            products = listEle[1] if len(listEle) > 1 else "" 
            
            if dataType == "t213":
                g_dictT213GrhProducts[grhType].append((element,products))                
            elif dataType == "ecmwf":
                g_dictECMWFGrhProducts[grhType].append((element,products))
            
    file.close()
    print(g_dictT213GrhProducts,g_dictECMWFGrhProducts)
    
    file = open("Element2FileName.ini")
    dataType = ""
       
    for line in file.readlines():
        line = line.strip()
        if not line :
            continue
        
        if line[0] == '#':
            print(line)
        if line[0] == '[' and line[-1] == ']':
            dataType = line[1:-1]
        else:
            listEle = line.split("=")
            element=listEle[0]
            products = listEle[1] if len(listEle) > 1 else "" 
            if dataType == "t213":
                 g_mapT213Ele2FileName[element] = products            
            elif dataType == "ecmwf":
                g_mapECMWFEle2FileName[element] = products
            
    file.close()
    print(g_mapT213Ele2FileName,g_mapECMWFEle2FileName)

def updateT213LatestFile():
    
    for key in g_dictT213GrhProducts.keys():
        
        
        print(key,g_dictT213GrhProducts[key])   
        
           
    
        
if __name__ == "__main__":
    
    InitiaGenPicture()
    updateT213LatestFile()