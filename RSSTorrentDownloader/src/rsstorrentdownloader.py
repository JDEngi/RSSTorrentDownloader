# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
#http://raspberrywebserver.com/cgiscripting/rpi-temperature-logger/building-an-sqlite-temperature-logger.html

__author__ = "Jelle"
__date__ = "$7-jun-2015 19:41:20$"

import feedparser
import requests
import re

def download_file(source, location):
    r = requests.get(source, stream=True)
    with open(location, 'wb') as file:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: 
                file.write(chunk)
                file.flush()
    
    return

#Keep the URL's and Regex's per series together:
class SeriesData:
    series_name = ""
    group_name = ""
    URL = ""
    regex = ""
    file_path = ""
    
OnePiece = SeriesData();
    
OnePiece.URL = "http://feeds.feedburner.com/YibisFansubs?format=xml"
OnePiece.regex = "http://tracker.yibis.com/torrents/%5Byibis%5D_One_Piece_\d*.*720p.*\.mkv\.torrent"
OnePiece.file_path = "D:\\Desktop\\OnePieceTorrents"
OnePiece.series_name = "One Piece"
OnePiece.group_name = "Yibis"

seriesList = [OnePiece]

for series in seriesList:
    target_regex = re.compile(series.regex, re.IGNORECASE)
    file_path = series.file_path
    URL_match = None
    
    feeds = feedparser.parse(series.URL)

    for item in feeds.entries:
        if item.title.lower().find("one piece") >= 0:            #if it is a one piece post                
            URL_match = target_regex.search(item.summary)
            if URL_match:
                target_url = URL_match.group(0)
                episode_number = re.sub("[^0-9]", "", re.findall("_\d+_", target_url)[0])
                local_filename = r"%s\\%s - %s [%s].torrent" % (series.file_path, series.series_name, episode_number, series.group_name)
                
                download_file(target_url, local_filename)
                            
                
            
print("done")