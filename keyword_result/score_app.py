import codecs, sys, nltk, os
from nltk.corpus import wordnet as wn, brown, gutenberg, stopwords

name_list = ['gary', 'mr. krabs', 'mrs. puff', 'narrator', 'patrick', 'plankton', 'sandy', 'spongebob', 'squidward']

stpwd = stopwords.words('english')

dic_list = []
for name in name_list:
    f = open(name + '.txt', 'r')

    dic = {}
    for line in f:
        if line[0] == '#': continue
        line = line.strip()
        (a, b, c, d) = line.split('\t')
        dic[d] = float(c)

    dic_list.append(dic)
        
    f.close()


sentence = ''
winner = ''
while sentence != 'exit':
    sentence = raw_input('::: ')
    
    tokens = nltk.word_tokenize(sentence)
    print tokens
    maxscore = 0
    for i in range(len(dic_list)):
        score = 0.0
        for tok in tokens:
            tok = tok.lower()
            if tok in stpwd: continue
            if tok in name_list: continue
            if dic_list[i].has_key(tok):
                #print score, dic_list[i][tok]
                score = score + dic_list[i][tok]

        #print 'why? ', name_list[i], score
        if maxscore < score:
            maxscore = score
            winner =  name_list[i]

    print winner, maxscore


            
        
    
