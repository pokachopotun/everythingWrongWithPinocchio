from kurochkin_labs.dataset_generator import call_generator
import pickle
import numpy as np
import math
from matplotlib import  pyplot as plt

class myargs:
    def __init__(self):
        self.N = 10
        self.dims = 2
        self.classes_cnt = 5
        self.crossings = 0
        self.dist = 3.0
        self.R = 1.0
        self.step = 0.5
        self.centers = 1
        self.delta = 0.0


def norm_p(q, w, d, r_norm):
    den = pow(2 * math.pi, q/2) * pow(r_norm, 0.5)
    return (w/den) * math.exp(-0.5 * d)

def sem(pts):
    y = list()
    for elem in pts:
        for x in elem:
            y.append(x)
    y = np.asarray(y)

    n = len(y) # cnt samples
    k = len(pts) # classes
    q = len(y[0]) # space size
    x = np.zeros( (n,k), dtype=np.float64)
    C = np.random.rand(k, q)
    R = np.zeros((k, q, q), dtype=np.float64)
    for i in range(len(R)):
        R[i] = np.eye(q, q, dtype=np.float64)

    W = np.ones((k, ), dtype=np.float64)
    W = np.divide(W, k)
    eps = 1e-3
    dst = np.zeros((n, k), dtype=np.float64)
    p = np.zeros_like(dst)
    llh = 0.0
    while True:

        DC = np.zeros_like(C)
        DR = np.zeros_like(R)
        DW = np.zeros_like(W)
        dllh  = 0.0
        for i in range(n):
            sumpi = 0
            for j in range(k):
                R_inv = R[j]
                for pp in range(len(R_inv)):
                    R_inv[pp][pp] /= k
                tmp = (y[i] - C[j]).T.dot(R_inv)
                dst[i][j] = tmp.dot(y[i] - C[j])
                p[i][j] = norm_p(q, W[j], dst[i][j], np.linalg.norm(R_inv))
                sumpi += p[i][j]
            x[i] = np.divide(p[i], sumpi)
            dllh += math.log(sumpi)
            xit = x[i]
            xit = xit.reshape((1, len(xit)))
            yi = y[i]
            yi = yi.reshape((len(yi), 1))
            tmp =  yi.dot(xit).T
            for a in range(len(tmp)):
                for b in range(len(tmp[a])):
                    DC[a][b] += tmp[a][b]
            for a in range(len(x[i])):
                DW[a] += x[i][a]
        for j in range(k):
            C[j] = DC[j]/DW[j]
            for i in range(n):
                tl = y[i] - C[j]
                tm = x[i][j]
                tr = (y[i] - C[j]).T
                tmp = tl.dot(tm).dot(tr)
                DR[j] = np.add(DR[j], tmp)
            R[j] = np.divide(DR[j], n)
            W[j] = np.divide(DW[j], n)

        if abs(dllh - llh) >= eps:
            llh = dllh
            continue
        else:
            break

    return ([a[0] for a  in y], [a[1] for a in y], [a.argmax() for a in x])


if __name__ == "__main__":
    args = myargs()
    generate_data = False
    if generate_data:
        pts = call_generator(args)
        pickle.dump(pts, open( 'sep.my', 'wb'))
        exit()
    else:
        pts = pickle.load(open('sep.my', 'rb'))

    x,y,z = sem(pts)
    plts = [( list(), list()) for _ in range(len(pts))]
    for i in range(len(x)):
        c = z[i]
        plts[c][0].append(x[i])
        plts[c][1].append(y[i])

    for i in range(len(pts)):
        plt.scatter(plts[i][0], plts[i][1])

    plt.show()



