import os
import random
import argparse
from math import sqrt
import matplotlib.pyplot as plt
from scipy.spatial import distance


def pt_sum(a, b):
    #print(a,b)
    return [sum(x) for x in zip(a, b)]

class generator:
    def __init__(self, args):
        #print("init generator")
        self.args = args
        self.max_tries = 10000
    #
    def generate_point_sphere(self, r, center = None):
        if center is None:
            center = [0.0 for x in range(self.args.dims)]
        pt = list()
        r_sq = r * r
        for i in range(self.args.dims - 1):
            pt.append(random.uniform(-sqrt(r_sq), sqrt(r_sq)))
            r_sq -= pt[-1] * pt[-1]
        pt.append(sqrt(r_sq))
        random.shuffle(pt)
        return pt_sum(pt, center)

    def try_generate_point_sphere(self, r, d, cl, mass_centers, class_centers, center = None):
        tries = 0
        while True:
            tries += 1
            if tries > self.max_tries:
                print("algorithm could not find a point. Exitting...")
                for i in range(len(class_centers)):
                    a = [x[0] for x in class_centers[i]]
                    b = [x[1] for x in class_centers[i]]
                    plt.plot(a, b, '.')
                plt.show()
                exit(1)
            pt = self.generate_point_sphere(r, center)
            flag = 0
            for i in range(len(mass_centers)):
                p = mass_centers[i]
                dst = distance.euclidean(p, pt)
                if dst < d:
                    flag += 1
            if flag <= 0: # 1 + int(0.1 * len(class_centers)):
                return pt
            else:
                return None


    def generate_point_inner(self, r, center = None):
        if center is None:
            center = [0.0 for x in range(self.args.dims)]
        pt = list()
        r_sq = r * r
        for i in range(self.args.dims):
            pt.append(random.uniform(-sqrt(r_sq), sqrt(r_sq)))
            r_sq -= pt[-1] * pt[-1]
        random.shuffle(pt)
        #print(pt, center)
        return pt_sum(pt, center)

    def calc_mass_center(self, centers):
        cm = [0.0 for x in range(self.args.dims)]
        for e in centers:
            for i in range(self.args.dims):
                cm[i] += e[i]
        for i in range(self.args.dims):
            cm[i] /= self.args.dims
        return centers[0]

    def generate_centers(self):
        print("generating centers")
        centers = [list() for x in range(self.args.classes_cnt)]
        mass_centers = [0.0 for x in range(self.args.classes_cnt)]
        for i in range(self.args.classes_cnt):
            if i == 0:
                ct = self.try_generate_point_sphere(self.args.dist, self.args.dist, i, mass_centers, centers)
            else:
                while True:
                    r_cl = random.randint(0, i - 1)
                    r_cl_c = random.randint(3 * int((self.args.centers - 1) / 4), self.args.centers - 1)
                    ct = self.try_generate_point_sphere(self.args.dist, self.args.dist, i, mass_centers, centers, centers[r_cl][r_cl_c])
                    if ct is not None:
                        break

            centers[i].append(ct)
            mass_centers[i] = self.calc_mass_center(centers[i])
            # for j in range(1, self.args.centers):
            #     r_cl_c = random.randint(3 * int((len(centers[i]) - 1)/4), len(centers[i]) - 1)
            #     pt = self.try_generate_point_sphere(self.args.step, self.args.dist, i, mass_centers, centers, centers[i][r_cl_c])
            #     centers[i].append(pt)
            #     mass_centers[i] = self.calc_mass_center(centers[i])
        return centers

    def generate_crossings(self, cnt):
        print("generating crossings")
        cross = set()
        vars = list()
        for i in range(self.args.classes_cnt):
            for j in range(i + 1, self.args.classes_cnt):
                a = i
                b = j
                if a > b:
                    a, b = b, a
                vars.append((a,b))
        orig_len_vars = len(vars)
        while len(cross) < cnt and len(cross) < orig_len_vars:
            if len(cross) >= cnt:
                return cross
            random.shuffle(vars)
            i, j = vars.pop()
            cross.add((i, j))
        return cross

    # def generate_crossings_random(self, cnt, centers):
    #     cross = set()
    #     while len(cross) < cnt:
    #         if len(cross) >= cnt:
    #             return cross
    #         i = random.randint(0, len(centers) - 1)
    #         j = random.randint(0, len(centers) - 1)
    #         if j == i:
    #             continue
    #         if j < i:
    #             i, j = j, i
    #         cross.add((i, j))
    #     return cross

    def generate_by_radius(self):
        print("Dataset generating by Radius")

        centers = self.generate_centers()

        cross = self.generate_crossings(self.args.crossings)
        print("crossings", cross)


        pts = [list() for i in range(self.args.classes_cnt)]
        # for i in range(len(centers)):
        #     for j in range(len(centers[i])):
        #         pts[i].append(centers[i][j])
        # for i in range(len(centers)):
        #     for j in range(len(centers[i])):
        #         for k in range(self.args.N):
        #             pts[i].append(self.generate_point_inner(self.args.R, centers[i][j]))
        for class_id in range(len(centers)):
            print("drawing class " + str(class_id) + " points")
            corcnt = 0
            for center_id in range(len(centers[class_id])):
                for k in range(self.args.N):
                    pt = self.generate_point_inner(self.args.R, centers[class_id][center_id])
                    correct = True
                    crossing = False
                    for cl_id in range(self.args.classes_cnt):
                        if not correct:
                            break
                        for ce_id in range(self.args.centers):
                            if cl_id == class_id:
                                continue
                            dst = distance.euclidean(pt, centers[cl_id][ce_id])
                            a,b = class_id, cl_id
                            if a > b:
                                a,b = b,a
                            if (dst < self.args.R and (a, b) not in cross and class_id == a) \
                                    or (dst < self.args.R and (a, b) in cross) \
                                    or dst >= self.args.R:
                                if dst < self.args.R and (a,b) in cross:
                                    crossing = True
                            else:
                                correct = False
                                break
                            if correct and class_id == b and not (a,b) in cross and  dst >= self.args.R \
                                and dst <= self.args.R + self.args.delta:
                                correct = False
                                break


                    if correct and crossing and (corcnt < int(self.args.rate * self.args.N * len(centers[class_id]))):
                        corcnt += 1
                        pts[class_id].append(pt)
                        continue
                    if crossing:
                        continue
                    if correct:
                        pts[class_id].append(pt)

        for i in range(len(pts)):
           #print(pts[i])
            a = [x[0] for x in pts[i]]
            b = [x[1] for x in pts[i]]
            plt.plot(a, b, '.')
        # for i in range(len(centers)):
        #     a = [x[0] for x in centers[i]]
        #     b = [x[1] for x in centers[i]]
        #     plt.plot(a, b, '.')
        plt.show()
        return pts


def check_args(args):
    print("Checking arguments...")
    return args.N is not None \
           and args.dims is not None \
           and args.classes_cnt is not None \
           and args.crossings is not None \
           and args.dist is not None \
           and args.step is not None \
           and args.centers is not None \
           and args.R is not None \
           and args.delta is not None

def call_generator(args):
    if True or check_args(args):
        gen = generator(args)
        res = gen.generate_by_radius()
        print('Generator finished successfully')
        return res
    else:
        print("Generator Error: Some arguments are missing... Use  --help for description")
        exit(1)


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
    call_generator(args)


#run command
# py dataset_generator.py --N 1000 --dims 2 --classes_cnt 10 --dist 2.0 --R 1.5 --crossings 10 --step 0.5 --centers 10 --rate 0.5 --delta 0.2
