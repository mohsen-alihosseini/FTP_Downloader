# FTP_Downloader
Copy main.py and Config.py to desire directory

IP,Username and password should be configured in config.py file in HOST_LIST. it is possible to add many as FTP server
following path with indicate the location for download file from FTP,EP(that is a CSV file for filter desire files), source is the path for files on server and destination is the path with indicate location of file which would move as desire files

LOCALFOLDER="D:\\path\\to\\download\\location\\"

EPpath='D:\\path\\to\\EP\\location\\EP.csv'

source='D:\\psth\\to\\XML\\location\\on Server\\'

destination = 'D:\\path\\to\\move\\location\\'

REMOTEFOLDER = "/path to xml files on servers/"

two main class develop with belo descriptions:

class XMLDownloader: for connect to ftp, list directories and files and download files with data filter(filter data to download just today or any desire date downloading)

classRegion_XML_Copy: for filter data wich indicate in EP and moving them to destination folder
