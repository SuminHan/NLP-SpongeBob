# Creates hypernym tree structure to be visualized by pajek.
# Information for the number of V, E and list of popular synsets are also documented.

import codecs, sys, nltk, os
from nltk.corpus import wordnet as wn, brown, gutenberg, stopwords

NUMBER_TO_LOOK = 300

def addToList(L, e):
	if e not in L:
		L.append(e)

stpwd = stopwords.words('english')
W = []		# Checked Word list
V = []		# Node list
E = []		# Edge list
EforV = {}	# Edge list for each Node
EforVn = {}	# Number of Edges for each Node
leafN = 0
maxPath = 0

if len(sys.argv) == 1:
  print "usage: hypernetwork-keyword.py \"filename\""
  exit(1)
  
fname = sys.argv[1]

myfile = codecs.open(fname, 'r', 'utf-8')
	
file_net = open('./net-' + fname + '.net', 'w')
file_clu = open('./net-' + fname + '.clu', 'w')
file_inf = open('./net-' + fname + '-info.txt', 'w')
	

for line in myfile:
	line = line.strip();
	#print line
	if not line or line[0] == '#':
		continue
	if leafN > 100:
		break
	
	spl = line.split('\t')
	#score = (int)spl[2]
	w = spl[3]
	
	if w.lower() not in stpwd and w not in W:
		addToList(W, w)
		syns = wn.synsets(w)
		if syns != []:
			ws = syns[0] # use the first synset
			leafN += 1
			for path in ws.hypernym_paths():
				if(len(path) > maxPath): maxPath = len(path)
				addToList(V, path[0].name()) # adding first node
				for i in range(1, len(path)):
					addToList(V, path[i].name())
					addToList(E, (V.index(path[i].name()), V.index(path[i-1].name())))

file_net.write('*Vertices %d\n' % (len(V)))
for index, word in enumerate(V):
	file_net.write('%d \"%s\"\n' % (index+1, word))
file_net.write('*Arcs : 1 "SAMPLEK"\n')
for v, w in E:
	file_net.write('%d %d\n' % (v+1, w+1))
file_inf.write('#FILE:' + fname + '\n')
file_inf.write('#Vertices %d\n' % (len(V)))
file_inf.write('#Arcs %d\n' % (len(E)))
file_inf.write('#MaxPath %d\n' % (maxPath))
file_inf.write('#LeafN %d\n' % (leafN))

for v, w in E:
	if w not in EforV:
		EforV[w] = []
	if w not in EforVn:
		EforVn[w] = 0
	EforV[w].append(w)
	EforVn[w]+=1
fd = nltk.FreqDist(EforVn)
fdL = [w for w, c in fd.most_common(NUMBER_TO_LOOK)]

file_inf.write('Rank\tCount\tSynset\n')
for r, w in enumerate(fdL):
	file_inf.write('%d\t%d\t%s\n' % (r, fd[w], V[w]))

file_clu.write('*Vertices %d\n' % (len(V)))
for index, word in enumerate(V):
	file_clu.write('%d\n' % (3 if index in fdL[:20] else 1))

print(fdL)
print([V[w] for w in fdL])
file_net.close()
file_clu.close()
file_inf.close()



