import os
import sys

def MakeOutputLine(res):
    outline = ""
    for i in range(len(res)):
        r = res[i]
        cnt, corr, perc, atime = r
        line = "testid {} question_count {} correct {} percentage {:.2f} avgtime {} ".format(i + 1, cnt, corr, perc, atime)
        outline += line
    return outline

def GetName(inputFileName, mode):
    if mode == "clinic":
        sub = "_ARandEPT" # clinic
    else:
        sub = "_empathy tasks" # norm
    i = inputFileName.index(sub)
    return inputFileName[:i]

def ProcessSingleFile(inputFileName, mode):
    with open(inputFileName, 'r') as file:
        contents = list()
        for ln in file:
            line = ""
            cnt = 0
            for c in ln:
                if c == '\"':
                    cnt = (cnt + 1) % 2
                if c == ',' and cnt == 1:
                    c = ' '
                line += c
            contents.append(line.strip().split(','))
        contents = contents[1:]

    res = list()
    if mode == "clinic":
        columns = [[65, 99], [82,]] # clinic
    else:
        columns = [[24, 56], [40,]] # norm
    for cols in columns:
        corr = 0
        t = 0
        cnt = 0
        for line in contents:
            for c in cols:
                if c >= len(line):
                    continue
                scorr = line[c]
                stime = line[c + 1]
                if scorr != "" and stime != "":
                    cnt += 1
                    corr += int(scorr)
                    t += float(stime)
        res.append((cnt, corr, float(corr) / cnt * 100, int(1000 * t / cnt)))
    name = GetName(os.path.basename(inputFileName), mode)
    print(name + " " + MakeOutputLine(res))

if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("Use python3 nadya_stats.py folderpath mode")

    inputFolderName = sys.argv[1]
    mode = sys.argv[2]

    for inputFileName in os.listdir(inputFolderName):
        inputFilePath = os.path.join(inputFolderName, inputFileName)
        ProcessSingleFile(inputFilePath, mode)
