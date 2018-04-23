import numpy as np
import math
from random import shuffle, sample
import importlib
import argparse
from copy import copy
from matplotlib import pyplot as plt
from matplotlib import cm
importlib.import_module("dataset_generator")

import dataset_generator as datagen

def sigma(x):
    return 1.0 / (1.0 + math.exp(-x))

def sigma_derivative(x):
    return sigma(x) * (1 - sigma(x))

class Perceptron:
    def __init__(self, layer_size):
        # print("initialize perceptron")
        self.layer_size = layer_size
        self.num_outputs = layer_size[-1]
        self.num_inputs = layer_size[0]
        self.layers_cnt = len(layer_size)

        #initialize biases
        # print("initialize biases")
        self.b = list()
        for sz in self.layer_size:
            self.b.append(np.random.rand(sz))

        # initialize activations
        # print("initialize activations")
        self.a = list()
        for sz in self.layer_size:
            self.a.append(np.random.rand(sz))

        # initialize summation functions
        # print("initialize summations")
        self.z = list()
        for sz in self.layer_size:
            self.z.append(np.random.rand(sz))


        #initialize weights
        # print("initialize weigths")
        self.w = list()
        self.w.append(np.random.rand(1,1))
        for i in range(1, self.layers_cnt):
            self.w.append(np.random.rand(self.layer_size[i], self.layer_size[i - 1]))
            #self.w.append(np.full((self.layer_size[i], self.layer_size[i - 1]), 1.0/self.layer_size[i - 1]))
        #print(self.w)

    def inception(self, x):
        #print("inception")
        self.z[0] = np.array(x[0])
        self.a[0] = np.array(x[0])
        for i in range(1, self.layers_cnt):
            self.z[i] = np.add( self.w[i].dot(self.a[i - 1]), self.b[i])
            for j in range(self.layer_size[i]):
                self.a[i][j] = sigma(self.z[i][j])
        return 0

    def accuracy(self, batch):
        ta = 0
        n_samples = len(batch)
        for elem_id in range(n_samples):
            x = batch[elem_id][0]
            y = batch[elem_id][1]
            p.inception(batch[elem_id])
            ans = p.a[-1].argmax()
            if ans == y:
                ta += 1
        return ta / n_samples

    def batch_loss(self, batch):
        ta = 0
        n_samples = len(batch)
        res = 0
        for elem_id in range(n_samples):
            x = batch[elem_id][0]
            y = batch[elem_id][1]
            expected = np.zeros(self.layer_size[-1])
            expected[y] = 1.0
            p.inception(batch[elem_id])
            res += np.linalg.norm((self.a[-1] - expected))
        return res / n_samples

def train(p, train_batch, test_batch, num_epochs = 30, learning_rate = 1.0, minibatch_size = 1):

    n_samples = len(train_batch)
    v_loss = list()
    for epoch_id in range(num_epochs):
        shuffle(train_batch)
        global_id = len(train_batch) - 1
        while(True):
            db = list()
            for sz in p.layer_size:
                db.append(np.full((sz), fill_value=0.0, dtype=np.float64))
            dw = list()
            for i in range(0, p.layers_cnt):
                dw.append(np.full((p.layer_size[i], p.layer_size[i - 1]), fill_value=0.0, dtype=np.float64))
            mini_batch = list()
            # delta = list()
            # for sz in p.layer_size:
            #     delta.append(np.zeros(sz))


            for elem_id in range(minibatch_size):
                if global_id < 0:
                    break
                mini_batch.append(copy(train_batch[global_id]))
                global_id -= 1
            if len(mini_batch) <= 0:
                break
            if global_id < 0:
                break

            cur_n_samples = len(mini_batch)
            for elem_id in range(cur_n_samples):
                x = mini_batch[elem_id][0]
                y = np.zeros(p.layer_size[-1])
                y[mini_batch[elem_id][1]] = 1.0
                delta = list()
                for sz in p.layer_size:
                    delta.append(np.zeros(sz))
                p.inception(mini_batch[elem_id])
                err = np.subtract(p.a[-1] , y)
                delta[-1] = np.multiply( np.multiply( np.subtract(p.a[-1] , y), p.a[-1]), np.subtract(np.ones(p.layer_size[-1], dtype=np.float64), p.a[-1]))
                #delta[-1] = np.multiply(1.0/cur_n_samples, delta[-1])
                for layer_id in range(p.layers_cnt - 1, 0, -1):
                    left = p.w[layer_id].T.dot(delta[layer_id])
                    right = np.multiply( p.a[layer_id-1], np.subtract(np.ones(p.layer_size[layer_id-1]), p.a[layer_id-1]))
                    delta[layer_id - 1] = np.multiply(left, right)
                for layer_id in range(1, len(db)):
                    db[layer_id] = np.multiply(-learning_rate/float(cur_n_samples), delta[layer_id] )
                for layer_id in range(1, len(dw)):
                     for x_i in range(len(p.a[layer_id - 1])):
                        for y_i in range(len(delta[layer_id])):
                            dw[layer_id][y_i][x_i] = -learning_rate/float(cur_n_samples) * p.a[layer_id - 1][x_i] * delta[layer_id][y_i]

            for layer_id in range(1, len(dw)):
                p.b[layer_id] = np.add(p.b[layer_id], db[layer_id])
                p.w[layer_id] = np.add(p.w[layer_id], dw[layer_id])

        train_loss = p.batch_loss(train_batch)
        test_loss = p.batch_loss(test_batch)
        acc = p.accuracy(train_batch)
        v_loss.append((acc, train_loss, test_loss))
        print("epoch_id", epoch_id, "TRAIN acc:", acc)
        if len(test_batch) > 0:
            acc = p.accuracy(test_batch)
            print("epoch_id", epoch_id, "TEST acc:", acc)
        print("epoch_id", epoch_id, "TRAIN loss:", train_loss)
        print("epoch_id", epoch_id, "TEST loss:", test_loss)
        #print(p.w)
    return v_loss

def convert_gen_to_batch(pts):
    batch = list()
    for i in range(len(pts)):
        for x in pts[i]:
            batch.append((x, i))
    return batch

def get_test(pts, args):
    test = [list() for i in range(len(pts))]
    for i in range(len(pts)):
        total_cnt = len(pts[i])
        test_cnt = int(args.test_perc * total_cnt)
        for j in range(test_cnt):
            test[i].append(pts[i].pop())
    return test

def normalize_data(pts):
    normed_pts = [list() for _ in range(len(pts))]
    mean  = np.zeros((2,), dtype=np.float64)
    cnt = 0
    for i in range(len(pts)):
        for pt in pts[i]:
            mean += np.asarray(pt)
            cnt+=1
    mean /= cnt
    st_d = 0.0
    for i in range(len(pts)):
        for pt in pts[i]:
            st_d += np.linalg.norm(np.asarray(pt) - mean)
    st_d /= cnt - 1
    for i in range(len(pts)):
        for pt in pts[i]:
            normed_pts[i].append( (np.asarray(pt) - mean) / st_d)
    return normed_pts

def plot_decision_boundary(p, train):
    # Set min and max values and give it some padding
    train_dots = np.asarray([x[0] for x in train])
    gt = np.asarray([x[1] for x in train])
    x_min, x_max = train_dots[:,0].min() - .5, train_dots[:, 0].max() + .5
    y_min, y_max = train_dots[:,1].min() - .5, train_dots[:, 1].max() + .5
    h = 0.01

    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    z = list()
    for i in range(len(xx)):
        for j in range(len(xx[i])):
            elem = ([xx[i][j], yy[i][j]], -1)
            p.inception(elem)
            ans = p.a[-1].argmax()
            z.append(ans)
    z = np.asarray(z).reshape(xx.shape)
    # Plot the contour and training examples
    plt.spectral()
    plt.contourf(xx, yy, z)
    plt.scatter(train_dots[:, 0], train_dots[:, 1], color = 'r')
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Dataset generator for Neural Networks course in MISIS')
    parser.add_argument('--N', type=int,
                        help='number of samples per class')
    parser.add_argument('--dims', type=int,
                        help='number of space dimensions')
    parser.add_argument('--classes_cnt', type=int,
                        help='number of classes')
    parser.add_argument('--dist', type=float,
                        help='distance between class centers')
    parser.add_argument('--R', type=float,
                        help='maximal distance from center to element')
    parser.add_argument('--crossings', type=int,
                        help='expected (but not guaranteed ) number of intersections')
    parser.add_argument('--step', type=float,
                        help='distance between core points of the class')
    parser.add_argument('--centers', type=int,
                        help='quantity of core points')
    parser.add_argument('--rate', type=float,
                        help='float in [0 : 1] spicifying maxumum proportion of element of a single class crossing another class')
    parser.add_argument('--delta', type=float,
                        help='delta')

    args = parser.parse_args()
    args.test_perc = 0.2

    layer_size = np.array([args.dims, 2, 2, args.classes_cnt])
    p = Perceptron(layer_size)
    pts = datagen.call_generator(args)
    normed_pts = normalize_data(pts)
    #normed_pts = pts

    test_pts = get_test(normed_pts, args)

    train_batch = convert_gen_to_batch(normed_pts)
    test_batch = convert_gen_to_batch(test_pts)
    # if len(test_batch) > 0:
    #     print("initial TEST accuracy", p.accuracy(test_batch))
    # else:
    #     print("initial TRAIN accuracy", p.accuracy(train_batch))
    num_epochs = 100
    mb_size =  1 #int(0.01 * len(train_batch))
    v_loss = train(p, train_batch, test_batch, num_epochs, 1.0, mb_size)

    plot_decision_boundary(p, train_batch)

    ep_x = list(range(1, num_epochs + 1))
    plt.plot(ep_x, [v_loss[i][0] for i in range(len(v_loss))], label = 'accuracy')
    plt.plot(ep_x, [v_loss[i][1] for i in range(len(v_loss))], label='train_loss')
    plt.plot(ep_x, [v_loss[i][2] for i in range(len(v_loss))], label='test_loss')
    plt.legend()
    total = len(train_batch) + len(test_batch)
    best = (p, p.accuracy(test_batch), 1.0, mb_size)
    print(best)
    plt.show()
    exit()
    for i in range(1):
        for j in range(2, 10):
            p = Perceptron(layer_size)
            lr = 1.0
            mb_size =  int( total / j )
            train(p, train_batch, test_batch, 500, lr, mb_size)
            acc = p.accuracy(test_batch)
            print(lr, mb_size, acc)
            if acc > best[1]:
                best = (p, acc, lr, mb_size)
    print(best)



#py perceptron.py --N 100 --dims 2 --classes_cnt 5 --dist 1.5 --R 1.0 --crossings 0 --step 0.5 --centers 1 --rate 0.0 --delta 0.2
