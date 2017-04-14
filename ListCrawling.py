# -*- coding: utf-8 -*-
"""
@author: suminhan
"""

import codecs

from bs4 import BeautifulSoup            # HTML parsing library
from lxml import html

file= codecs.open('SpongeBob_Script_List.txt','w', 'utf-8')
file.write('http://spongebob.wikia.com\n')

with open('TranscriptList.html','r') as f:
    page = f.read()


#soup = BeautifulSoup(page)
soup = BeautifulSoup(page, "lxml")
tabbertabs = soup('table', {'class':'wikitable',})

idx = 1
for div in tabbertabs:
    
    for tr in div.select("tr"):
        tds = tr.select("td")
        title_text = tds[1].text[:-1]
        
        if title_text.lower() == 'title':
            continue

        
        title_text
        href = tds[2].a['href']
    
        #print idx, title_text, href
        file.write(str(idx) + "\t" + title_text + "\t" + href + "\n")
        idx = idx + 1

    
#file.close()
