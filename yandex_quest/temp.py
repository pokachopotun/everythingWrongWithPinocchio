import os


with open('C:/Users/Denis/Google Диск/STUDYHARD/7th semester/ИММОД курсач/daily_stat.csv', 'r') as file:
    contents = [x.strip().split(';') for x in file.readlines()]

n = len(contents)
m = len(contents[0])


file = open('C:/Users/Denis/Google Диск/STUDYHARD/7th semester/ИММОД курсач/output.txt', 'w')

file.write('station,day,month,year,flow' + '\n')
for i in range(1, n):
    for j in range(1 , m):
        date = [int(x) for x in contents[0][j].split('.')]
        money = 0
        print(contents[i][j].split(' '))
        for elem in contents[i][j].split(' '):
            money*=pow(10, len(elem))
            money+=int(elem)
        file.write(contents[i][0] + "," + str(date[0]) + ',' + str(date[1]) + ',' + str(date[2]) + ',' + str(money) + '\n')