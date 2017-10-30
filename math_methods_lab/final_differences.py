from matplotlib import pyplot as plot
import numpy as np
from math import *
alpha = [3, -1.2]
beta = [-2.1, 5]
A = 4
B = -1
a = 1.8
b = 2.9
h = 0.05

n = int((b - a)/h)
xi = [a + i * h for i in range(n + 1)]


def f(x):
    return exp(-2 * x)

def fi(idx):
    return f(xi[idx])

def pi():
    return float(-4)

def qi():
    return float(3)

mat = [ [0 for j in range(3)] for i in range(n + 1)]
res = [0 for i in range(n + 1)]
for i in range(1, n):
    mat[i][0] = 1.0 - (h/2) * pi()
    mat[i][2] = 1.0 + (h / 2) * pi()
    mat[i][1] = -(2.0 - h * h * qi())
    res[i] = h * h * fi(i)

mat[0][1] = 2 * h * alpha[0] - 3 * alpha[1] + alpha[1] * (1 - pi() * h/2)/(1 + pi() * h/2)
mat[0][2] = 4 * alpha[1] - alpha[1]* (2 - h * h* qi())/(1 + pi() * h/2)
res[0] = 2 * h * A + h * h * fi(1) * alpha[1]/(1 + pi() * h/2)

mat[n][0] = -4 * beta[1]+ beta[1] * (2 - h * h * qi()) / (1 - (h/2) * pi())
mat[n][1] = 2 * h * beta[0] + 3 * beta[1] - beta[1] * (1 + (h/2) * pi())/(1 - (h/2) * pi())
res[n] = 2 * B * h - beta[1] * h * h * fi(n - 1)/(1 - (h/2) * pi())

de = [0 for i in range(n + 1)]
la = [0 for i in range(n + 1)]

de[0] = - float(mat[0][2]) / mat[0][1]
la[0] = float(res[0])/mat[0][1]

for i in range(1, n + 1):
    de[i] = -float(mat[i][2])/float(mat[i][1] + mat[i][0] * de[i - 1])
    la[i] = float(res[i] - mat[i][0] * la[i - 1])/float(mat[i][1] + mat[i][0] * de[i - 1])

yi =  [0 for i in range(n + 1)]
yi[n] = la[n]
for i in range(n - 1, -1, -1):
    yi[i] = de[i] * yi[i + 1] + la[i]



def y(x):
    return 0.0666667 * exp(-2*x) + 0.363254 * exp(x) - 0.000260118 * exp(3 * x)

plot_x = list()
plot_y = list()
plot_x1 = list()
plot_y1 = list()

for elem in mat:
    print elem
print de
print la

for i in range(n + 1):
    plot_x.append(xi[i])
    plot_y.append(yi[i])
    plot_x1.append(xi[i])
    plot_y1.append(y(xi[i]))
# for x in col_knots:
#     plot_x.append(x)
#     plot_y.append(yn(x))
#     plot_x1.append(x)
#     plot_y1.append(y(x))

plot.plot(plot_x, plot_y, label='approximation')
plot.plot(plot_x1, plot_y1, label='original')
plot.title('final differences')
plot.grid()
plot.show()