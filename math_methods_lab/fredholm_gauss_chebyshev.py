import numpy as np
from math import sqrt, cos, exp, pi, sin
import matplotlib.pyplot as plot
class solution:
    def __init__(self, ti, Ai):
        self.test = False
        self.ti = ti
        self.Ai = Ai

        # if self.test:
        #     self.ti = [-0.577350, 0.577350]
        #     self.Ai = [1, 1]

        self.n = len(self.ti)


        if self.test:
            self.a = 0
            self.b = pi/2
            self.la = 0.95 #( self.b - self.a ) / 2.0
        else:
            self.a = 0
            self.b = pi/2
            self.la = 0.5 #( self.b - self.a ) / 2.0

        self.steps = 10
        self.h = float((self.b - self.a)/self.steps)


        self.mat = np.zeros((self.n, self.n))
        self.r = np.zeros((self.n, ))

        self.si = [self.shift_node(elem) for elem in self.ti]

        for i in range(self.n):
            self.r[i] = self.f(self.si[i])
            for j in range(self.n):
                self.mat[i][j] = self.matij(i, j)

        self.xi = np.linalg.solve(self.mat, self.r)

        self.tt = [self.a + i * self.h for i in range(self.steps + 1)]
        self.yi = [self.x_approx(t) for t in self.tt]

        print ( self.yi )

        self.y_orig = [self.original(t) for t in self.tt]

        print ( self.y_orig )

    def matij(self, i, j):
        return int(i == j) - self.Ai[i] * self.la * self.phi(self.si[i], self.si[j])

    def x_approx(self, t):
        res = 0
        for i in range(self.n):
            res += self.Ai[i] * self.la * self.phij(t, i) * self.xi[i]
        res += self.f(t)
        return res

    def shift_node(self, t):
        return (self.a + self.b + (self.b - self.a) * t)/2.0

    def phi(self, t, s):
        if self.test:
            return cos(t - 5.0 * s)
            # return 1 / sqrt(t + s ** 2)
        else:
            return sin(t - 3 * s)

    def phij(self, t, j):
        if self.test:
            return cos(t - 5.0 * self.si[j])
            # return 1/sqrt(t + self.si[j] ** 2)
        else:
            return sin(t - 3 * self.si[j])

    def f(self, t):
        if self.test:
            return t * t /(1.0 + t)
            # return sqrt(t + 1) - sqrt(t + 4) + t
        else:
            return exp(2 * t)

    def original(self, t):
        if self.test:
            return 0.1836783 * cos(t) + 0.0502564 * sin(t) + t * t / (t + 1.0)
            # return t
        else:
            return -0.5 * (-4.38764) * cos(t) + 0.5 * (-4.42616) * sin(t) + exp(2 * t)

if __name__ == "__main__":

    gauss_ti = [-0.906180, -0.538469, 0, 0.538469, 0.906180]
    gauss_Ai = [0.236927, 0.478629, 0.568889, 0.478629, 0.236927]


    g = solution(gauss_ti, gauss_Ai)

    chebyshev_ti = [-0.832497, -0.374541, 0, 0.374541, 0.832497]
    chebyshev_Ai = [0.4, 0.4, 0.4 , 0.4, 0.4]
    f = solution(chebyshev_ti, chebyshev_Ai)

    plot.plot(g.tt, g.y_orig, label = "original")
    plot.plot(g.tt, g.yi, label = "gauss")
    plot.plot(f.tt, f.yi, label = "chebyshev")
    plot.legend()
    plot.grid()
    plot.show()

