from kurochkin_labs.dataset_generator import call_generator
import pickle
import numpy as np
import math
from matplotlib import  pyplot as plt
import random
from copy import copy



def norm_p(q, d, r_norm):
    den = pow(2 * math.pi, q/2) * pow(r_norm, 0.5)
    return math.exp(-0.5 * d) / den

def sem(pts):
    y = list()
    max_dim = [-1e9 for _ in range(len(pts[0]))]
    min_dim = [1e9 for _ in range(len(pts[0]))]
    for elem in pts:
        for x in elem:
            y.append(x)
            for dd in range(len(x)):
                if x[dd] < min_dim[dd]:
                    min_dim[dd] = x[dd]
                if x[dd] > max_dim[dd]:
                    max_dim[dd] = x[dd]
    y = np.asarray(y)

    samples_cnt = len(y)
    classes_cnt = len(pts)
    dims = len(y[0]) # space size
    x = np.ones( (samples_cnt,classes_cnt), dtype=np.float64)
    x = np.divide(x, classes_cnt)

    # r = random.random()
    median = np.random.rand(classes_cnt, dims)
    for i in range(dims):
        median[:,i] = np.multiply(median[:,i], (max_dim[i] - min_dim[i]))

    cov = np.zeros((classes_cnt, dims, dims), dtype=np.float64)
    for i in range(len(cov)):
        cov[i] = np.eye(dims, dims, dtype=np.float64)


    # weights are the same
    w = np.ones((classes_cnt, ), dtype=np.float64)
    w = np.divide(w, classes_cnt)
    eps = 1e-6
    # dst = np.zeros((samples_cnt, classes_cnt), dtype=np.float64)
    p = np.zeros((samples_cnt, classes_cnt), dtype=np.float64)
    llh = 0.0
    max_iter = 20
    iter_done = 0
    while True:

        d_median = np.zeros_like(median)
        d_cov = np.zeros_like(cov)
        # d_w = np.zeros_like(w)
        dllh  = 0.0

        # Stochastic step
        cluster_size = np.zeros((classes_cnt, ), dtype=np.uint32)
        cl_ids = list()
        modeled_clusters = [list() for _ in range(classes_cnt)]
        for i in range(len(x)):
            cl_id = np.random.multinomial(1, x[i])
            cl_id = cl_id.argmax()
            cl_ids.append(cl_id)
            modeled_clusters[cl_id].append(i)
            cluster_size[cl_id] += 1

        for i in range(classes_cnt):
            if cluster_size[i] == 0:
                print("zero class on modeling")
                # print(x)
                return ([a[0] for a in y], [a[1] for a in y], [a.argmax() for a in x])

        # Expectation step
        for i in range(samples_cnt):
            sumpi = 0
            for j in range(classes_cnt):
                R_inv = np.linalg.pinv(cov[j])
                # for pp in range(len(R_inv)):
                #     R_inv[pp][pp] /= classes_cnt
                dij = (y[i] - median[j]).T.dot(R_inv).dot(y[i] - median[j])
                p[i][j] = w[j] * norm_p(dims, dij, np.linalg.norm(R_inv))
                sumpi += p[i][j]
            # print(sumpi)
            # if sumpi == 0:
            #     return ([a[0] for a in y], [a[1] for a in y], [a.argmax() for a in x])
            x[i] = np.divide(p[i], sumpi)

            dllh += math.log(sumpi)
            # xit = x[i]
            # xit = xit.reshape((1, len(xit)))
            # yi = y[i]
            # yi = yi.reshape((len(yi), 1))
            # tmp2 = yi.dot(xit).T

            cl_id = cl_ids[i]
            for b in range(dims):
                d_median[cl_id][b] += y[i][b]/cluster_size[cl_id]
            # for a in range(len(x[i])):
            #     d_w[a] += x[i][a]

        # Modification step (non stochastic)
        # for j in range(classes_cnt):
        #     median[j] = DC[j]/d_w[j]
        #     for i in range(samples_cnt):
        #         d_cov[j] = np.add(d_cov[j], (y[i] - median[j]).dot(x[i][j]).dot((y[i] - median[j]).T))
        #     cov[j] = np.divide(d_cov[j], samples_cnt)
        #     w[j] = np.divide(d_w[j], samples_cnt)

        # Modification step (Stochastic)
        w = np.divide(cluster_size, samples_cnt)
        for j in range(classes_cnt):
            median[j] = d_median[j] / w[j]
            for i in modeled_clusters[j]:
                # d_cov[j] = np.add(d_cov[j], (y[i] - median[j]).dot(x[i][j]).dot((y[i] - median[j]).T))
                d_cov[j] = np.add(d_cov[j], (y[i] - median[j]).dot((y[i] - median[j]).T))
            cov[j] = np.divide(d_cov[j], samples_cnt)
            cov[j] = np.divide(cov[j], w[j])

        iter_done += 1
        if abs(dllh - llh) >= eps and iter_done < max_iter:
            # print(abs(dllh - llh))
            llh = dllh
            continue
        else:
            print("iter done", iter_done)
            break

    return ([a[0] for a  in y], [a[1] for a in y], [a.argmax() for a in x])


class myargs:
    def __init__(self):
        self.N = 10
        self.dims = 2
        self.classes_cnt = 5
        self.crossings = 0
        self.dist = 5.0
        self.R = 1.0
        self.step = 0.5
        self.centers = 1
        self.delta = 0.0

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



