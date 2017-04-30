import os
import string
import codecs
valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)

if os.path.exists('speaker'):
    for f in os.listdir(os.getcwd() + "\\speaker"):
        os.remove(os.getcwd() + "\\speaker\\" + f)
else:
    os.makedirs('speaker')
    

lines = []
fdir = os.getcwd() + "\\result"
flist = os.listdir(fdir)

for fname in flist:
    f = codecs.open(fdir+"\\"+fname, "r", "utf-8")
    for line in f:
        line = line.strip()
        toks = line.split("\t")
        if len(toks) != 2:
            continue
        (speaker, content) = toks
        content = content.strip()

        valid_name = "".join(x for x in speaker if x in valid_chars)
        tmpf = codecs.open("speaker/" + valid_name + ".txt", "a", "ascii")
        tmpf.write(content.encode('ascii', 'ignore') + '\n')
        tmpf.close()

