import codecs, sys, nltk, os
from nltk.corpus import wordnet as wn, brown, gutenberg, stopwords

name_list = ['gary', 'mr. krabs', 'mrs. puff', 'narrator', 'patrick', 'plankton', 'sandy', 'spongebob', 'squidward']

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


for n in ['spongebob', 'gary', 'mr. krabs', 'patrick', 'plankton', 'sandy', 'squidward']:
 sentence = ''
 winner = ''
 count = 0
 total = 0
 f = open(n + "script.txt", "r")
 for sentence in f:
     sentence = sentence.strip()
     #sentence = raw_input('::: ')
     
     tokens = nltk.word_tokenize(sentence)
      #print tokens
     maxscore = 0
     for i in mydic:
         score = 0
         for tok in tokens:
             tok = tok.lower()
             if tok in stpwd: continue
             if tok in name_list: continue
             if tok in ['krusty', 'krab', 'krabs']: continue
             if mydic[i].has_key(tok):
                 #print score, dic_list[i][tok]
              score = score + mydic[i][tok]

         #print 'why? ', i, score
         if maxscore < score:
          maxscore = score
          winner =  i
     if maxscore != 0 and winner == n: count += 1
     total += 1
    #print winner, maxscore
 print n, count, total, float(count)/total
