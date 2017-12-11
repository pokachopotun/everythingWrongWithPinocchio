import numpy as np
from math import sqrt, cos, exp, pi, sin
import matplotlib.pyplot as plot
class solution:
    def __init__(self, ti, Ai):

        self.l = 0
        self.r = pi/2

        self.ti = ti
        self.Ai = Ai


        self.n = len(self.ti)

        # self.ti = [-0.832497, -0.374541, 0, 0.374541, 0.832497]
        # self.Ai = [0.236927, 0.478629, 0.568889, 0.478629, 0.236927]

        self.la = 0.5

        self.a = np.zeros((self.n, self.n))
        self.b = np.zeros((self.n,))
        #init a, b
        for i in range(self.n):
            self.b[i] = self.get_bi(i)
            for j in range(self.n):
                self.a[i][j] = -self.get_aij(i, j)
                if i == j:
                    self.a[i][j] += 1


        self.x = np.linalg.solve(self.a, self.b)

        self.cur_x = list()

        self.steps = 10
        self.h = float(self.r - self.l)/float(self.steps)
        self.y = list()
        self.y_orig = list()
        for i in range(self.steps):
            cur_x = self.l + self.h * i
            self.cur_x.append(cur_x)
            self.y.append(self.get_x_approx(cur_x))
            self.y_orig.append(self.original(cur_x))

        print ( self.x )
        print (self.y_orig)
        print(self.y)

    def get_x_approx(self, x):
        res = 0
        for i in range(self.n):
            t = self.t_parami(i)
            res += self.Ai[i] * self.get_axt(x, t) * self.x_parami(i)
        res += self.get_bt(x)
        return res

    def x_parami(self, i):
        return self.x[i]

    def t_parami(self, i):
        t = self.ti[i]
        return (self.l + self.r + (self.r - self.l) * t)/2

    def get_axt(self, x, t):
        # return self.la/sqrt(x + t**2)
        return self.la  * cos(x - 3 * t)

    def get_bt(self, t):
        # return sqrt(t + 1)  - sqrt(t + 4) + t
        return exp(2 * t)

    def get_bi(self, i):
        t = self.t_parami(i)
        return self.get_bt(t)

    def get_aij(self, i, j):
        x = self.t_parami(i)
        t = self.t_parami(j)
        return self.get_axt(x, t) * self.Ai[i]

    def original(self, x):
        # return x
        return 0.5 * (-4.38764) * cos(x) + 0.5 * (-4.42616) * sin(x)  + exp(2 * x)

if __name__ == "__main__":
    # gauss_ti = [-0.577350, 0.577350]
    # gauss_Ai = [1, ]

    gauss_ti = [-0.906180, -0.538469, 0, 0.538469, 0.906180]
    gauss_Ai = [0.236927, 0.478629, 0.568889, 0.478629, 0.236927]
    g = solution(gauss_ti, gauss_Ai)

    chebyshev_ti = [-0.832497, -0.374541, 0, 0.374541, 0.832497]
    chebyshev_Ai = [0.4, 0.4, 0.4 , 0.4, 0.4]
    f = solution(chebyshev_ti, chebyshev_Ai)
    plot.plot(g.cur_x, g.y_orig, label = "original")
    plot.plot(g.cur_x, g.y, label = "gauss")
    plot.plot(f.cur_x, f.y, label = "chebyshev")
    plot.legend()
    plot.show()

