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

    samples_cnt = len(y)
    classes_cnt = len(pts)
    dims = len(y[0]) # space size
    x = np.zeros( (samples_cnt,classes_cnt), dtype=np.float64)
    median = np.random.rand(classes_cnt, dims)
    cov = np.zeros((classes_cnt, dims, dims), dtype=np.float64)
    for i in range(len(cov)):
        cov[i] = np.eye(dims, dims, dtype=np.float64)


    # weights are the same
    w = np.ones((classes_cnt, ), dtype=np.float64)
    w = np.divide(w, classes_cnt)
    eps = 1e-6
    dst = np.zeros((samples_cnt, classes_cnt), dtype=np.float64)
    p = np.zeros_like(dst)
    llh = 0.0
    while True:

        DC = np.zeros_like(median)
        d_cov = np.zeros_like(cov)
        d_w = np.zeros_like(w)
        dllh  = 0.0
        for i in range(samples_cnt):
            sumpi = 0
            for j in range(classes_cnt):
                R_inv = cov[j]
                for pp in range(len(R_inv)):
                    R_inv[pp][pp] /= classes_cnt
                dst[i][j] = (y[i] - median[j]).T.dot(R_inv).dot(y[i] - median[j])
                p[i][j] = norm_p(dims, w[j], dst[i][j], np.linalg.norm(R_inv))
                sumpi += p[i][j]
            x[i] = np.divide(p[i], sumpi)
            dllh += math.log(sumpi)
            xit = x[i]
            xit = xit.reshape((1, len(xit)))
            yi = y[i]
            yi = yi.reshape((len(yi), 1))
            tmp2 =  yi.dot(xit).T

            for a in range(len(tmp2)):
                for b in range(len(tmp2[a])):
                    DC[a][b] += tmp2[a][b]
            for a in range(len(x[i])):
                d_w[a] += x[i][a]
        for j in range(classes_cnt):
            median[j] = DC[j]/d_w[j]
            for i in range(samples_cnt):
                d_cov[j] = np.add(d_cov[j], (y[i] - median[j]).dot(x[i][j]).dot((y[i] - median[j]).T))
            cov[j] = np.divide(d_cov[j], samples_cnt)
            w[j] = np.divide(d_w[j], samples_cnt)

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



