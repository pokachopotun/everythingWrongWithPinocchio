import os
import random
import argparse
from math import sqrt
import matplotlib.pyplot as plt
from scipy.spatial import distance


def pt_sum(a, b):
    return [sum(x) for x in zip(a, b)]

class generator:
    def __init__(self, args):
        print("init generator")
        self.args = args

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

    def generate_point_inner(self, r, center = None):
        if center is None:
            center = [0.0 for x in range(self.args.dims)]
        pt = list()
        r_sq = r * r
        for i in range(self.args.dims):
            pt.append(random.uniform(-sqrt(r_sq), sqrt(r_sq)))
            r_sq -= pt[-1] * pt[-1]
        random.shuffle(pt)
        return pt_sum(pt, center)

    def generate_centers(self):
        centers = list()
        centers.append(self.generate_point_inner(self.args.dist))
        while len(centers) < self.args.classes_cnt:
            r_id = random.randint(0, len(centers) - 1)
            pt = self.generate_point_sphere(self.args.dist, centers[r_id])
            correct = True
            # for i in range(len(centers)):
            #     dst = distance.euclidean(centers[i], pt)
            #     if dst < self.args.dist:
            #         correct = False
            #         break
            if correct:
                centers.append(pt)
        return centers

    def generate_crossings(self, cnt, centers):
        cross = set()
        less = 0
        while len(cross) < cnt:
            if len(cross) >= cnt:
                return cross
            i = random.randint(0, len(centers) - 1)
            j = random.randint(0, len(centers) - 1)
            if j == i:
                continue
            if j < i:
                i, j = j, i
            dst = distance.euclidean(centers[i], centers[j])
            if dst < 2 * self.args.R:
                cross.add((i, j))
        return cross

    def generate_crossings_random(self, cnt, centers):
        cross = set()
        while len(cross) < cnt:
            if len(cross) >= cnt:
                return cross
            i = random.randint(0, len(centers) - 1)
            j = random.randint(0, len(centers) - 1)
            if j == i:
                continue
            if j < i:
                i, j = j, i
            cross.add((i, j))
        return cross

    def generate_by_density(self):
        print("Dataset generating by Density")

        centers = self.generate_centers()

        cross = self.generate_crossings_random(self.args.crossings, centers)

        pts = [list() for i in range(self.args.classes_cnt)]
        for i in range(len(centers)):
            pts[i].append(centers[i])
        for i in range(self.args.N):
            for class_id in range(self.args.classes_cnt):
                while True:
                    r_id = random.randint(0, len(pts[class_id]) - 1)
                    pt = self.generate_point_sphere(self.args.density, pts[class_id][r_id])
                    correct = True
                    for cl_id in range(self.args.classes_cnt):
                        if cl_id == class_id:
                            continue
                        dst = distance.euclidean(pt, centers[cl_id])
                        a,b = class_id, cl_id
                        if a > b:
                            a,b = b,a
                        if (dst < self.args.R and (a, b) not in cross and class_id == a) or (dst < self.args.R and (a, b) in cross) or dst >= self.args.R:
                            correct = True
                        else:
                            correct = False
                            break
                    if correct:
                        pts[class_id].append(pt)
                        break
                    else:
                        continue

        for cpt in pts:
            a = [x[0] for x in cpt]
            b = [x[1] for x in cpt]
            plt.plot(a, b, 'o')

        plt.show()

    def generate_by_radius(self):
        print("Dataset generating by Radius")

        centers = self.generate_centers()
        cross = self.generate_crossings(self.args.crossings, centers)

        pts = [list() for i in range(self.args.classes_cnt)]
        for i in range(len(centers)):
            pts[i].append(centers[i])
        for i in range(self.args.N):
            for class_id in range(self.args.classes_cnt):
                while True:
                    pt = self.generate_point_inner(self.args.R, centers[class_id])
                    correct = True
                    for cl_id in range(self.args.classes_cnt):
                        if cl_id == class_id:
                            continue
                        dst = distance.euclidean(pt, centers[cl_id])
                        a,b = class_id, cl_id
                        if a > b:
                            a,b = b,a
                        if (dst < self.args.R and (a, b) not in cross and class_id == a) or (dst < self.args.R and (a, b) in cross) or dst >= self.args.R:
                            correct = True
                        else:
                            correct = False
                            break
                    if correct:
                        pts[class_id].append(pt)
                        break
                    else:
                        continue
        for i in range(len(pts)):
            a = [x[0] for x in pts[i]]
            b = [x[1] for x in pts[i]]
            plt.plot(a, b, '.')

        plt.show()



def check_args(args):
    print("Checking arguments...")
    return args.N is not None \
           and args.dims is not None \
           and args.classes_cnt is not None \
           and args.crossings is not None \
           and args.dist is not None
#           and args.R is not None \
#           and args.density is not None

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
    parser.add_argument('--density', type=float,
                        help='density of points, expressed as maximal distance from one point of the class to another')
    parser.add_argument('--density_uniform', action='store_true',
                        help='')
    parser.add_argument('--crossings', type=int,
                        help='expected (but not guaranteed ) number of intersections')

    args = parser.parse_args()
    if True or check_args(args):
        gen = generator(args)
        if args.density is not None:
            gen.generate_by_density()
        else:
            gen.generate_by_radius()
    else:
        print("Error: Some arguments are missing... Use  --help for description")
    print('program finished successfully')