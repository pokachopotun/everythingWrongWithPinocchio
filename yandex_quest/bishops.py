

with open('hash.txt', 'r') as file:
    str = 'neercsemifinal'
    s = set([str[i]  for i in range(len(str))])
    contents = [x.strip() for x in file.readlines()]
    res = ''
    proc = list()
    for content in contents:
        res = ''
        for i in range(len(content)):
            if not content[i] in s:
                res += content[i]
            else:
                res += ' '
        res += '\n'
        proc.append(res)

with open('output_2.txt', 'w') as file:
    for j in range(len(proc[0])):
        for i in range(len(proc)):
            file.write( proc[i][j] )
        file.write('\n')

