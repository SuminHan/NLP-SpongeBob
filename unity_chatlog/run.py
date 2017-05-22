import string
valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)

f = open("Unity_Training.txt", "r")
chats = open("only_chats.txt", "w")

name_list = []

for line in f:
    line = line.strip()
    line = line[8:]
    name = ''
    comment = ''
    for i in range(len(line)):
        if line[i] == '>':
            name = line[1:i]
            comment = line[i+1:]
            break

    name = ''.join(c for c in name if c in valid_chars)
    name_list.append(name)

    ##for nm in name_list:
        ##comment = comment.replace(nm, "")

    #print name, '::::', comment
    chats.write(comment + '\n')
    
    each = open('result/' + name + "_chats.txt", "a")
    each.write(comment + '\n')
    each.close()

chats.close()
f.close()
