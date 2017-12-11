from math import cos, sin, exp, pi, sqrt
import numpy as mp
import matplotlib.pyplot as plot



def f(t):
    # return t ** 2 - 1.0 / t
    return cos(t) * (t ** 4 - pi ** 4)/4 + sin(t) * (t**3 - pi**3)/3


def df(t):
    # return 2 * t + 1 / t ** 2
    return -sin(t) * (t**4 - pi**4)/4 + (t**3) * cos(t) + cos(t) * (t ** 3 - pi**3)/3 + sin(t) * (t ** 2)


def qf(t, s):
    # return t**2 + s**2 + 1.0
    return sin(t) + s * cos(t)

def original(t):
    # return  1/t**2
    return t ** 2

class solve_trapezium:
    def __init__(self, l, r, h):
        self.l = l
        self.r = r
        self.h = h
        self.n = int((self.r - self.l) / self.h)
        self.xi = list()

        self.ti = list()
        for i in range(self.n + 1):
            self.ti.append(self.l + i * self.h)


        for i in range(len(self.ti)):
            self.xi.append(self.get_xi(i))

        print(self.xi)

    def qij(self, i, j):
        return qf(self.ti[i], self.ti[j])

    def get_xi(self, i):
        if i == 0:
            return df(self.ti[i])/self.qij(i, i)
        else:
            q_sum = 0
            for j in range(1, i):
                q_sum += self.qij(i, j) * self.xi[j]
            return (f(self.ti[i]) - (self.h/2) * self.qij(i, 0) * self.xi[0] - self.h * q_sum)/( (self.h/2) * self.qij(i, i))


class solve_square:
    def __init__(self, l, r, h):
        self.l = l
        self.r = r
        self.h = h
        self.n = int((self.r - self.l) / self.h)
        self.xi = list()
        self.si = list()
        self.ti = list()
        for i in range(1, self.n + 2):
            self.ti.append(self.l + i * self.h)
            self.si.append(self.ti[-1] - self.h/2)

        for i in range(len(self.ti)):
            self.xi.append(self.get_xi(i))

        print(self.xi)

    def qij(self, i, j):
        sj = self.ti[j] - self.h/2
        return qf(self.ti[i], sj)

    def get_xi(self, i):
        ##  if i == 0:
        #     return df(self.ti[i]) / self.qij(i, i)
        # else:
        #     q_sum = 0
        #     for j in range(1, i):
        #         q_sum += self.qij(i, j) * self.xi[j]
        #     return (f(self.ti[i]) - (self.h / 2) * self.qij(i, 0) * self.xi[0] - self.h * q_sum) / ((self.h / 2) * self.qij(i, i))
        if i == 0:
            return f(self.ti[i])/(self.h * self.qij(i, i))
        else:
            q_sum = 0
            for j in range(i):
                q_sum += self.qij(i, j) * self.xi[j]
            return ( f(self.ti[i]) - self.h * q_sum )/ (self.h * self.qij(i, i))


if __name__ == "__main__":
    trap = solve_trapezium(pi, pi + 0.5, 0.1)
    sq = solve_square(pi, pi + 0.5, 0.1)
    orig_t = [original(t) for t in trap.ti]
    orig_s = [original(t) for t in sq.si]
    orig = list()
    orig_ti = list()
    for i in range(len(orig_s) + len(orig_t)):
        if i % 2 == 0:
            orig.append(orig_t[int(i/2)])
            orig_ti.append(trap.ti[int(i/2)])
        else:
            orig.append(orig_s[int(i/2)])
            orig_ti.append(sq.si[int(i / 2)])

    plot.plot(trap.ti, trap.xi, label = "trapezium")
    plot.plot(sq.si, sq.xi, label="square")
    plot.plot(orig_ti, orig, label="original")

    plot.grid()
    plot.legend()
    plot.show()