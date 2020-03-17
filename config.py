
from datetime import datetime
#################
#Date to process leave blank if today

#DATE_TO_PROCESS = "20200216"
DATE_TO_PROCESS = "" 

todayDate = datetime.now()
todayDate = "{:04d}{:02d}{:02d}".format(todayDate.year, todayDate.month, todayDate.day)

HOST_LIST = [["10.10.10.01", "user", "password"], #FTP1
             ["10.10.10.01", "user", "password"], #FTP2
             ["10.10.10.01", "user", "password"]] #FTP3

FOL_LIST = [""]

#local path for laptop
LOCALFOLDER="D:\\path\\to\\download\\location\\"
EPpath='D:\\path\\to\\EP\\location\\EP.csv'
source='D:\\psth\\to\\XML\\location\\on Server\\'
destination = 'D:\\path\\to\\move\\location\\'


REMOTEFOLDER = "/path to xml files on servers/"
DL_FILETYPE = 1 
