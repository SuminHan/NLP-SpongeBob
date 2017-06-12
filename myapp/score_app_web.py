import codecs, sys, nltk, os
from nltk.corpus import wordnet as wn, brown, gutenberg, stopwords

name_list = ['gary', 'mr. krabs', 'mrs. puff', 'patrick', 'plankton', 'sandy', 'spongebob', 'squidward']

stpwd = stopwords.words('english')

mydic = {}
for name in name_list:
    f = open(name + '.txt', 'r')
    mydic[name] = {}

    for line in f:
        if line[0] == '#': continue
        line = line.strip()
        (a, b, c, d) = line.split('\t')
        mydic[name][d] = float(c)

    f.close()


sentence = sys.argv[1]
winner = ''
    
tokens = nltk.word_tokenize(sentence)

print "{"
idx = 0
for i in mydic:
    score = 0
    for tok in tokens:
        tok = tok.lower()
        if tok in stpwd: continue
        if tok in name_list: continue
        if tok in ['krusty', 'krab', 'krabs']: continue
        if mydic[i].has_key(tok):
             score = score + mydic[i][tok]

    print "\"" + i + "\": " + str(score)
    if (idx < len(mydic) - 1):
        print ","
    idx += 1
    
print "}"
