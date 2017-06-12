import os.path, math
import codecs, sys, nltk, os
from nltk.corpus import wordnet as wn, brown, gutenberg, stopwords

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

stpwd = stopwords.words('english')

file_names = [
    'Gary',
    'Mr. Krabs',
    'Patrick',
    'Plankton',
    'Sandy',
    'SpongeBob',
    'Squidward'
]

ttypes = ['NN', 'NNS', 'NNP', 'NNPS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'JJ', 'RB']
def tagist(tag, t):
    return tag == t
        
ftcount = {} # file type count
ttwcount = {} # total of type + word
ttcount = {} # total for each type 
for t in ttypes:
    ttcount[t] = 0

ddic = {}
for fname in file_names:
    print "tagging " + fname + " and making dictionary."

    ftcount[fname] = {}
    ttwcount[fname] = {}
    ddic[fname] = {}
    for t in ttypes:
        ftcount[fname][t] = 0
        ddic[fname][t] = {}
        ttwcount[fname][t] = {}
        
    if os.path.exists("kcount_" + fname + ".txt"):
        print "\tUse precomputed data"
        f = open("kcount_" + fname + ".txt", "r")
        for line in f:
            line = line.strip()
            if not line: break
            twc = line.split('\t')
            t = twc[0]
            w = twc[1]
            c = int(twc[2])
            
            ddic[fname][t][w] = c

            if ttwcount[fname][t].has_key(w):
                ttwcount[fname][t][w] += c
            else: ttwcount[fname][t][w] = c
            
            ftcount[fname][t] += c
            ttcount[t] += c
        f.close()
        
    else:
        f = open(fname + ".txt", "r");
        for line in f:
            line = line.strip()
            if not line: break
            words = nltk.pos_tag(nltk.word_tokenize(line))
            for (w, tag) in words:
                w = w.lower()
                if w in stpwd: continue
                if len(w) <= 1: continue
                
                for t in ttypes:
                    if tag == t:
                        if ddic[fname][t].has_key(w):
                            ddic[fname][t][w] += 1
                        else: ddic[fname][t][w] = 1
                        
                        if ttwcount[fname][t].has_key(w):
                            ttwcount[fname][t][w] += 1
                        else: ttwcount[fname][t][w] = 1
                        
                        ftcount[fname][t] += 1
                        ttcount[t] += 1
        f.close()

        f2 = open("kcount_" + fname + ".txt", "w")
        for t in ttypes:
            ndic = ddic[fname][t]
            for w in sorted(ndic, key=ndic.get, reverse=True):
                f2.write(t + "\t" + w + "\t" + str(ndic[w]) + "\n")
        f2.close()


ff = open("keyword_result.txt", "w")
sdic = {}
for fname in file_names:
    print fname
    ff.write(fname + "\n")
    sdic[fname] = {}
    for t in ttypes:
        ndic = {}
        for w in ddic[fname][t]:
            a = ddic[fname][t][w]
            c = ftcount[fname][t]
            
            b = ttwcount[fname][t][w]
            d = ttcount[t]
            if a == 0 or b == 0:
                print a, b, c, d
                continue
            
            knval = keyness(a, b, c, d)
            ndic[w] = knval 

        sdic[fname][t] = ndic 
        #print "\t", t
        ff.write("\t" + t + "\n")
        num = 20
        for w in sorted(ndic, key=ndic.get, reverse=True):
            #print "\t\t", w, ndic[w]
            ff.write("\t\t" + w + "\t" + str(ndic[w]) + "\n")
            num -= 1
            if num == 0: break

ff.close()

while True:
    sent = raw_input("Chat: ")
    words = nltk.pos_tag(nltk.word_tokenize(sent))
    score = {}
    for fname in file_names:
        score[fname] = 0
    for (w, tag) in words:
        w = w.lower()
        for fname in file_names:
            for t in ['NN']:
                if tagist(tag, t):
                    if sdic[fname][t].has_key(w):
                        score[fname] += sdic[fname][t][w]

    for who in sorted(score, key=score.get, reverse=True):
        print who, score[who]

        
    if sent == 'quit()': break
    
#print keyness(159,280,4695,55633)
