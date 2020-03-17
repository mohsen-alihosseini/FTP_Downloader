import os
from datetime import datetime
import time
from stat import S_ISDIR, S_ISREG
import logging
from logging.handlers import RotatingFileHandler
import config as cfg
import pysftp
import pandas as pd
import csv
import shutil
i=0

temp = datetime.now()
DIRFILTER = "AUTOBAKDATA{:04d}{:02d}{:02d}".format(temp.year, temp.month, temp.day)
#print("Will look for directory with filter " + DIRFILTER)

PATHFILTER = ""


if cfg.DATE_TO_PROCESS == "":
    todayDate = datetime.now()
    todayDate = "{:04d}{:02d}{:02d}".format(todayDate.year, todayDate.month, todayDate.day)
else:
    todayDate = cfg.DATE_TO_PROCESS

class XMLDownloader:
    AUTOBAK = 1
    GEXPORT = 2
    NEEXPORT = 3

    def __init__(self,  HOST_LIST, FOL_LIST, LOCALFOLDER, type=AUTOBAK, PATHFILTER = ""):
        self.logger = self.setupLogger()
        self.logger.warning(
            "Please note that this utility does not use hostkeys to verify the hosts. If this is insecure for "
            "your setup, then kindly update the code or submit a feature request.")
        self.cnopts = pysftp.CnOpts()
        self.cnopts.hostkeys = None
        self.PATHFILTER = PATHFILTER
        self.HOST_LIST = HOST_LIST
        self.FOL_LIST = FOL_LIST
        self.LOCALFOLDER = LOCALFOLDER
        self.type = type		
        if self.PATHFILTER.strip() == "":
            self.PATHFILTER = DIRFILTER

    def setupLogger(self):
        '''
        Just sets up the logger and returns the logger instance which was setup with the init function.

        :return: logger instance
        '''
        LOG_TAG = 'FTP_Download'+ '_' +str(todayDate)
        self.myLogger = logging.getLogger(LOG_TAG )
        self.myLogger.setLevel(logging.DEBUG)
        self.fh = RotatingFileHandler(LOG_TAG  + ".txt", 'a', maxBytes=20*1024*1024,
                                      backupCount=20)
        self.fh.setLevel(logging.INFO)
        self.ch = logging.StreamHandler()
        self.ch.setLevel(logging.INFO)


        formatter = logging.Formatter('[ %(asctime)s ] [ %(name)s ][ %(levelname)s ] %(message)s')
        self.ch.setFormatter(formatter)
        #self.sh.setFormatter(formatter)
        self.fh.setFormatter(formatter)

        self.myLogger.addHandler(self.ch)
        self.myLogger.addHandler(self.fh)
        #self.myLogger.addHandler(self.sh)
        return self.myLogger


    def get_r_portable(self, sftp, remotedir, localdir, preserve_mtime=False):
        for entry in sftp.listdir(remotedir):
            remotepath = remotedir + "/" + entry
            localpath = os.path.join(localdir, entry)
            mode = sftp.stat(remotepath).st_mode
            # if S_ISDIR(mode):
            #     try:
            #         #os.makedirs(localpath) # Floders not copy! no need!
            #         print('Folder',i+1)
            #     except OSError:  # dir exists
            #         pass
            #     self.get_r_portable(sftp, remotepath, localpath, preserve_mtime)
            if S_ISREG(mode):
                if self.PATHFILTER.strip() != "":
                    if str(remotepath).lower().find(self.PATHFILTER.lower()) > -1:
                        sftp.get(remotepath, localpath, preserve_mtime=preserve_mtime)
                        self.logger.info("Current remotepath is : " + str(remotepath) + ", Filter is " + self.PATHFILTER.strip().lower())

    def run(self):
        if self.type == self.AUTOBAK:
            REMOTEFOLDER = cfg.REMOTEFOLDER
        else:
            self.logger.info("Other types not implemented yet.")
            return

        for host in self.HOST_LIST:
            self.logger.info("Attempting connection to " + host[0])
            with pysftp.Connection(host[0], username=host[1], password=host[2], cnopts=self.cnopts) as sftp:
                try:
                    for dirs in self.FOL_LIST:
                        self.logger.info("Attempting download from " + dirs + "on " + host[0])
                        currdir = REMOTEFOLDER + dirs + ""
                        self.logger.info("Joining via os = " + os.path.join(REMOTEFOLDER, dirs,
                                                                            "") + " , currdir = " + currdir)
                        try:
                            self.get_r_portable(sftp, currdir, self.LOCALFOLDER, True)
                        except Exception as e:
                            self.logger.error("Exception in dir exploration" + str(e))

                except Exception as e:
                    self.logger.error("Exception " + str(e))





def Sitename(s):
    ext = s.split('.')[-1] #find the extention of file.if it is gz would process els it wouldn't enter. privent folder issue and unwanted braeks
    if ext=='gz':
        for i, c in enumerate(s):
            if c.isdigit():
                if s[i-2]=="D":
                    break
                return s[i-1:i+5]
def RNC_BSC(s):
    ext = s.split('.')[-1]
    if ext=='gz':
        a=s.split("_", 2)
        if len(s)>2:
            return a[1]

class Region_XML_Copy:

    def copy():
        source=cfg.source
        filelist=os.listdir(source)
        destination = cfg.destination
        #EP date Read
        EP=[]
        EPpath=cfg.EPpath
        with open(EPpath) as f:
            EP=[line[0] for line in csv.reader(f)]
            print('EP Read Successfully')
        #site name
        for i in range(0,len(filelist)):
            for j in range(0,len(EP)):
                if Sitename(filelist[i])==EP[j]:
                    shutil.copyfile(source+filelist[i],destination+filelist[i])
                    print(filelist[i],EP[j],'Copy Done')
                elif RNC_BSC(filelist[i])==EP[j]:
                    shutil.copyfile(source+filelist[i],destination+filelist[i])
                    print(filelist[i],EP[j],'Copy Done')
    
    
    print('END of Region_XML_Copy_initiation ')

def delete_files_temp():
    folder = cfg.source
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


downloader = XMLDownloader(PATHFILTER=todayDate,
                                   HOST_LIST=cfg.HOST_LIST, FOL_LIST=cfg.FOL_LIST,
                                   LOCALFOLDER=cfg.LOCALFOLDER, type=cfg.DL_FILETYPE)

downloader.run()

Region_XML_Copy.copy()
delete_files_temp()









    
