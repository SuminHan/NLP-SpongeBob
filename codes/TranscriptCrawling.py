# -*- coding: utf-8 -*-
"""
@author: suminhan
"""

import codecs
import os
import urllib2
import string

valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)

#>>> base=os.path.basename('/root/dir/sub/file.ext')
#name = os.path.basename(f.name)

from bs4 import BeautifulSoup            # HTML parsing library
from lxml import html

if not os.path.exists('result'):
    os.makedirs('result')

list_file = codecs.open('SpongeBob_Script_List.txt','r', 'utf-8')
URL = list_file.readline()
URL = URL.strip()

startidx = 1 #starting index in the case for interruption
idx = 1
for line in list_file:
    line = line.strip()
    if not line:
        break
    (num, title, href) = line.split('\t')
    print num, title
    print URL + href
    if idx < startidx:
        idx = idx + 1
        continue
    

    #with codecs.open(URL + href,'r', 'utf-8') as f:
    #    page = f.read()

    
    response = urllib2.urlopen(URL + href)
    webContent = response.read()
    print(webContent[0:300])

    soup = BeautifulSoup(webContent, "lxml")
    page = soup('div', {'id':'mw-content-text',})

    valid_name = "".join(x for x in title if x in valid_chars)
    print valid_name
    file= codecs.open("result/" + num + ". " + valid_name + '.result.txt','w', 'utf-8')

    for div in page:
        if div.find('ul'):
            for li in div.ul.select('li'):
                v = li.b
                if v:
                    speaker = v.text
                    li.b.replace_with('')
                    
                    while li.i:
                        li.i.replace_with('')
                        
                    content = li.text

                    #print speaker
                    #print content
                    file.write(speaker + "\t" + content)

    file.close()
    #idx = idx + 1
    #if idx > 10: break
