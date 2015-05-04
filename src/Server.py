import threading
import time
import os
import win32file
import win32con

ACTIONS = {

  1 : "Created",

  2 : "Deleted",

  3 : "Updated",

  4 : "Renamed from something",

  5 : "Renamed to something"

}
count = 1
litWatchDir = [" w:\productindex","E:\FtpServer\productindex"]
 
class StartThreadSwan(threading.Thread,dir):
    def run(self):
        global litWatchDir
        while 1:
            print("%s # %s: Pretending to do stuff" % (self.name, count))
            time.sleep(2)
            print ("done with stuff # %s" % self.name)
 
if __name__ == '__main__':
    for i in range(5):
        StartThread().start()