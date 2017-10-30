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
p = -4
q = 3

n = int((b - a)/h) + 1
xi = [a + i * h for i in range(n + 1)]

def runge_kutta_get_next(f, g, x0, y0, z0):
    k1 = f(x0, y0, z0)
    q1 = g(x0, y0, z0)

    k2 = f(x0 + h / 2.0, y0 + q1 / 2.0, z0 + k1 / 2.0)
    q2 = g(x0 + h / 2.0, y0 + q1 / 2.0, z0 + k1 / 2.0)

    k3 = f(x0 + h / 2.0, y0 + q2 / 2.0, z0 + k2 / 2.0)
    q3 = g(x0 + h / 2.0, y0 + q2 / 2.0, z0 + k2 / 2.0)

    k4 = f(x0 + h, y0 + q3, z0 + k3)
    q4 = g(x0 + h, y0 + q3, z0 + k3)

    deltaY = h * (q1 + 2.0 * q2 + 2.0 * q3 + q4) / 6.0
    deltaZ = h * (k1 + 2.0 * k2 + 2.0 * k3 + k4) / 6.0

    y1 = y0 + deltaY
    z1 = z0 + deltaZ

    return (y1, z1)

def solve_cowell(f, g, x0, y0, z0):
    res = list()
    y1, z1 = runge_kutta_get_next(f, g, x0, y0, z0)
    for i in range(1, len(xi)):
        x1 = xi[i]
        res.append((x0, y0, z0))
        f0 = f(x0, y0, z0)
        f1 = f(x1, y1, z1)

        g0 = g(x0, y0, z0)
        g1 = g(x1, y1, z1)

        y21 = y1 + (h/2.0) * (3 * g1 - g0)
        z21 = z1 + (h / 2.0) * (3 * f1 - f0)
        f21 = f(x1 + h, y21, z21)
        g21 = g(x1 + h, y21, z21)

        y22 = y1 + (h/12.0) * (5  * g21 + 8 * g1 - g0)
        z22 = z1 + (h / 12.0) * (5 * f21 + 8 * f1 - f0)
        f22 = f(x1 + h, y22, z22)
        g22 = g(x1 + h, y22, z22)

        y3 = y22 + (h/12.0) * ( 23 * g22 - 16 * g1 + 5 * g0)
        z3 = z22 + (h / 12.0) * (23 * f22 - 16 * f1 + 5 * f0)
        f3 = f(x1 + 2 * h, y3, z3)
        g3 = g(x1 + 2 * h, y3, z3)

        y23 = y1 + (h/24.0 ) * ( - g3 + 13 * g22 + 13 * g1 - f0)
        z23 = z1 + (h / 24.0) * (- f3 + 13 * f22 + 13 * f1 - f0)
        x0, y0, z0 = x1, y1, z1
        y1, z1 =  y23, z23


    res.append( (x0, y0, z0) )
    return res

def f(x):
    return exp(-2 * x)

def f0(x, y, z):
    return -p * z - q * y

def g0(x, y, z):
    return z


def f1(x,y,z):
    return -p * z - q * y + f(x)

def g1(x,y,z):
    return z

#solve u equation
u_res = solve_cowell(f0, g0, xi[0], alpha[1], -alpha[0])
v_res = solve_cowell(f1, g1, xi[0], 0, A/alpha[1])

print u_res

print v_res


C = float(B - beta[0] * v_res[-1][1] - beta[1] * v_res[-1][2])/float(beta[0] * u_res[-1][1] + beta[1] * u_res[-1][2])


def y_res(i):
    return C * u_res[i][1] + v_res[i][1]

def y(x):
    return 0.0666667 * exp(-2*x) + 0.363254 * exp(x) - 0.000260118 * exp(3 * x)

plot_x = list()
plot_y = list()
plot_x1 = list()
plot_y1 = list()

for i in range(0, n + 1):
    plot_x.append(xi[i])
    plot_y.append(y(xi[i]))
    plot_x1.append(xi[i])
    plot_y1.append(y_res(i))
print plot_x

plot.plot(plot_x, plot_y, label='original')
plot.plot(plot_x1, plot_y1, label = 'approximation')
plot.title('reduction + cowell + runge')
plot.grid()
plot.legend()
plot.show()