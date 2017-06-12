# -*- coding: utf-8 -*-
"""
@author: suminhan
"""

import codecs
import os
#>>> base=os.path.basename('/root/dir/sub/file.ext')
#name = os.path.basename(f.name)

from bs4 import BeautifulSoup            # HTML parsing library
from lxml import html


'''
for line in codecs.open('SpongeBob_Script_List.txt','r', 'utf-8'):
    (idx, title, href) = line.split('\t')
    print href
'''

with codecs.open('Help_Wanted.html','r', 'utf-8') as f:
    page = f.read()

file= codecs.open(f.name + '.result.txt','w', 'utf-8')

soup = BeautifulSoup(page, "lxml")
page = soup('div', {'id':'mw-content-text',})

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

                print speaker
                print content
                file.write(speaker + "\t" + content)

file.close()
