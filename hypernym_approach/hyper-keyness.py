import os.path, math
import codecs, sys, nltk, os
from nltk.corpus import wordnet as wn, brown, gutenberg, stopwords


file_names = [
 'Gary',
 'Mr. Krabs',
 'Patrick',
 'Plankton',
 'Sandy',
 'SpongeBob',
 'Squidward'
]

ddic = {}
total = 0

def addToList(L, e):
    if e not in L:
        L.append(e)
  
def keyness(a, b, c, d):
    a = float(a)
    b = float(b)
    c = float(c)
    d = float(d)
    E1 = c*(a+b) / (c+d)
    E2 = d*(a+b) / (c+d)
    ka = (a*math.log(a/E1))
    kb = (b*math.log(b/E2))
    return 2*(ka+kb)

def mykeyness(fname, word):
    global file_names
    global ddic
    global total
    a = ddic[fname][word]
    b = 0
    for w in ddic[fname]:
        b += ddic[fname][word]

    c = 0
    for fn in file_names:
        if ddic[fn].has_key(word):
            c += ddic[fn][word]
    d = total
    return keyness(a, b, c, d)
    
    
for fname in file_names:
    ddic[fname] = {}
    f = open('net-' + fname + '-info.txt', 'r')
    for line in f:
        line = line.strip()
        if line[0] == '#' or not line or line[0:4] == 'Rank': continue
        rcw = line.split('\t')
        c = int(rcw[1])
        w = rcw[2]
        if c <= 1: continue
        ddic[fname][w] = c
        total += c
    f.close()


while True:
    V = []
    ssss = '''What do you mean? You drove him away. It's right there in black and white. See? Right there and there.
It's the apocalypse! Office products falling from the sky!
But I thought you drove him away with your neglect and indifference.
Hey, their having a sale on scented pine cones.
Pine cones, pine cones, pine cones.
Old lady, quick. I'm looking for the scented pine cones. It's an emergency!
Once again, you and I are kept apart, oh sweet scented pine cones. Hey, Gary.  Um...uhh...
I want peanuts.'''
#    sent = raw_input("Chat: ")
    sent = ssss
    words = nltk.pos_tag(nltk.word_tokenize(sent))
    score = {}
    for fname in file_names:
        score[fname] = 0
    for (w, tag) in words:
        w = w.lower()
        if tag == 'NN':
            syns = wn.synsets(w, pos=wn.NOUN)
            if len(syns) > 0:
                ws = syns[0]
                for path in ws.hypernym_paths()[0]:
                    addToList(V, path.name())

    for v in V:
        for fname in file_names:
            if ddic[fname].has_key(v):
                score[fname] += mykeyness(fname, v)
    
    for who in sorted(score, key=score.get, reverse=True):
        print who, score[who]

        
    if sent == 'quit()': break
    break
