from matplotlib import pyplot as plot
import numpy as np
from math import pow, exp
alpha = [3.0, -1.2]
beta = [-2.1, 5.0]
A = 4.0
B = -1.0
a = 1.8
b = 2.9
h = 0.25
n = int((b - a)/h)
col_knots = [float(a + i * h) for i in range(0, n + 2)]

n = len(col_knots) - 2

print n
# a = np.array([[3,1], [1,2]])
# b = np.array([9,8])
# x = np.linalg.solve(a, b)

def get_phi0_quotients():
    mat = np.array([
        [alpha[0], alpha[0] * a + alpha[1]],
                    [beta[0], beta[0] * b + beta[1]]
    ])
    res = np.array([A,B])
    x = np.linalg.solve(mat, res)
    return x

phi0_quotients = get_phi0_quotients()
print "phi0_quotients", phi0_quotients

def pi():
    return float(-4)

def qi():
    return float(3)

def f(x):
    return exp(-2 * x)

# col_knots = [a + (i + 1) * float(b - a)/(n + 1) for i in range(n)]
print "collocations knots", col_knots

def x_idx(idx):
    return float(col_knots[idx])




def calc_gamma_i(i):
    num = float(beta[0] * (b - a) * (b - a) + (i + 2) * beta[1] * (b - a))
    denum = float(beta[0] * (b - a) + (i + 1) * beta[1])
    return -float(num)/float(denum)

gammas = [calc_gamma_i(i) for i in range(n + 1)]

def phi(i, x):
    if i == 0:
        return float(phi0_quotients[0] + phi0_quotients[1] * x)
    return float(gammas[i] * pow(x - a, i + 1) + pow(x - a, i + 2))



def phi_1(i, x):
    if i == 0:
        return float(phi0_quotients[1])
    return float(gammas[i] * pow(x - a, i) * (i + 1) + pow(x - a, i + 1) * (i + 2))

def phi_2(i, x):
    if i == 0:
        return 0
    return gammas[i] * pow(x - a, i - 1) * (i + 1) * i + pow(x - a, i) * (i + 2) * (i + 1)

def calc_aij(i, j):
    return float(phi_2(j, x_idx(i)) + pi() * phi_1(j, x_idx(i)) + qi() * phi(j, x_idx(i)))

def calc_b_i(i):
    return float(f(x_idx(i)) - phi_2(0, x_idx(i)) - pi() * phi_1(0, x_idx(i)) - qi() * phi(0, x_idx(i)))


aij = np.array( [[calc_aij(i, j) for j in range(1, n + 1)] for i in range(1, n + 1)])
bi = np.array( [calc_b_i(i) for i in range(1, n + 1)] )
print aij
print bi
cj = np.linalg.solve(aij, bi)
print cj

def yn(x):
    val = 0
    for i in range(1, n + 1):
        val += float(cj[i - 1] * phi(i, x))
    val += float(phi(0, x))
    return val

def y(x):
    return 0.0666667 * exp(-2*x) + 0.363254 * exp(x) - 0.000260118 * exp(3 * x)


# print alpha[0] * phi(20, a) + alpha[1] * phi_1(20, a)
# print beta[0] * phi(20, b) + beta[1] * phi_1(20, b)
# exit()


plot_x = list()
plot_y = list()
plot_x1 = list()
plot_y1 = list()

for i in range(0, len(col_knots)):
    cur_x = x_idx(i)
    plot_x.append(cur_x)
    plot_y.append(yn(cur_x))
    plot_x1.append(cur_x)
    plot_y1.append(y(cur_x))

print plot_y
print plot_y1
print plot_y1[0] - plot_y[0]

plot.plot(plot_x, plot_y, label="approximation")
plot.plot(plot_x1, plot_y1, label="original")
plot.legend()
plot.title('collocation')
plot.grid()
plot.show()