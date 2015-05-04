# -*- coding: utf-8 -*-  

from PIL import Image
import os,math,time,sys
import shutil
from globalmaptiles import GlobalMercator

mercator = GlobalMercator()

def pictureFormatConvert(picSrcFile,picDesFile):

    im = Image.open("c:\\aaa\\C000201.jpg")
    
    # PIL complains if you don't load explicitly
    im.load()
    
    # Get the alpha band
    alpha = im.split()[-1]
    
    im = im.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
    
    # Set all pixel values below 128 to 255,
    # and the rest to 0
    mask = Image.eval(alpha, lambda a: 255 if a <=128 else 0)
    
    # Paste the color of index 255 and use alpha as a mask
    im.paste(255, mask)
    
    # The transparency index is 255
    im.save("c:\\aaa\\C000201_py.jpg", transparency=255)


def CalculateGoogleIndex(file,outputdir):
    "calculate google index"
    global mercator
    lat, lon, latmax, lonmax = 35.0, 90, 45, 100
    boundingbox = False
    txtFile = file[0:-3] +"txt"
    iindex = 0
    print(file)
    for line in open(txtFile):
        if iindex == 1:
            print(line)
            valueIndex = line.index(":") + 1
            latlon = line[valueIndex:]
            valuelist = latlon.split(",")
            lon = float(valuelist[0])
            latmax = float(valuelist[1])
            print(lon,latmax)
        elif iindex == 3:
            print(line)
            valueIndex = line.index(":") + 1
            latlon = line[valueIndex:]
            valuelist = latlon.split(",")
            lonmax = float(valuelist[0])
            lat = float(valuelist[1])
            print(lonmax,lat)
        
        iindex += 1
    
    adjust = 0.001
    lat += adjust
    lon += adjust
    lonmax -= adjust
    latmax -= adjust
    for zoomlevel in range(15,3,-1):
            
        tz = zoomlevel
    
        mx, my = mercator.LatLonToMeters( lat, lon )
        tminx, tminy = mercator.MetersToTile( mx, my, tz )

        mx, my = mercator.LatLonToMeters( latmax, lonmax )
        tmaxx, tmaxy = mercator.MetersToTile( mx, my, tz )        
        
        if tmaxx > tminx or tmaxy > tminy:
             continue
        print("*********************************************************************")
        for ty in range(tminy, tmaxy+1):
            for tx in range(tminx, tmaxx+1):
                gx, gy = mercator.GoogleTile(tx, ty, tz)
                #197 103 8
                googlefile = "%s\\Sat_x=%dy=%dzoom=%d.png"%(outputdir,gx,gy,tz)
                print(googlefile)
                shutil.copy(file, googlefile)
#                pictureFormatConvert(file, googlefile)
        break
    
    
def ConvertPicture(picDir,OutPut):
    "convert google old map to new"
    try:
        listDir = os.listdir(picDir)
        for str1 in listDir:
            list1 = os.listdir("%s\\%s"%(picDir,str1))
            for str2 in list1:
                list2 = os.listdir("%s\\%s\\%s"%(picDir,str1,str2))
                list = [filetmep for filetmep in list2 if filetmep.find("jpg") != -1]
                print(list)
                for picfile in list:
                    file = "%s\\%s\\%s\\%s"%(picDir,str1,str2,picfile)
                    CalculateGoogleIndex(file,OutPut)
#                    throw(TypeError, "spam")
                    
    #                print(file)
    except Exception as E:
       print(str(E))         
    
if __name__ == "__main__":

#    picdir = "D:\\work\\AIW\\testdata\\demo_google"
#    ConvertPicture(picdir,"C:\\Output\\googleOutput")
       
    if  None:
        print("cann't convert!")    
    
    if  len(sys.argv) < 3:
        print("invalid argvs")        
    else:
        print(sys.argv[0])
        print(sys.argv[1]) 
        print(sys.argv[2])
        
        ConvertPicture(sys.argv[1],sys.argv[2])
    
        print("All the picture converted successfully!")


