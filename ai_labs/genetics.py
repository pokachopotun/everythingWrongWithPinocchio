import os
import numpy as np
import random
from copy import copy
from matplotlib import pyplot as plt
cities = np.asarray([[154, 185], [7, 266], [156, 52], [162, 223], [273, 174], [228, 282], [218, 75], [34, 87],
[124, 155], [279, 93], [201, 188], [101, 258], [266, 55], [106, 219], [230, 97], [176, 110],
[126, 167], [50, 223], [256, 289], [286, 227], [70, 263], [235, 84], [91, 131], [114, 17],
[131, 298], [229, 174], [46, 215], [76, 65], [57, 99], [71, 225], [16, 126], [112, 226],
[224, 161], [244, 154], [175, 9], [120, 291], [145, 41], [110, 265], [191, 42], [36, 213],
[45, 171], [281, 77], [155, 204], [82, 215], [269, 226], [71, 132], [135, 12], [41, 160],
[278, 131], [1, 81], [296, 244], [272, 168], [148, 64], [38, 202], [28, 2], [125, 283],
[229, 280], [156, 51], [51, 268], [107, 250], [48, 211], [227, 231], [257, 184], [171, 256],
[21, 273], [38, 89], [231, 105], [231, 211], [265, 273], [233, 258], [33, 290], [288, 131],
[146, 279], [59, 27], [141, 68], [170, 211], [293, 298], [21, 153], [17, 222], [152, 280],
[259, 57], [269, 279], [202, 23], [1, 208], [185, 9], [67, 79], [95, 291], [207, 130],
[190, 119], [198, 147], [54, 5], [19, 43], [48, 294], [290, 248], [90, 94], [76, 215],
[279, 132], [244, 88], [271, 4], [57, 164]])

def get_way_len(way):
    return sum([ np.linalg.norm(cities[way[i]] -  cities[way[i - 1]]) for i in range(1, len(way))])

def mutate_1(way):
    l = random.randint(0, len(way) - 10)
    r = random.randint(l+9, len(way) - 1)
    res = list(way[:l])
    sh = list(way[l : r])
    random.shuffle(sh)
    rest = way[r:]
    res.extend(sh)
    res.extend(rest)
    # assert len(res) != 100
    if len(res) != 100:
        raise Exception("No 100!")
    return ( get_way_len(res), res)

def mutate_2(way):
    res = copy(way)
    k = 15 #random.randint(1, 15)
    p = random.sample(list(way), k)
    random.shuffle(p)
    for i in range(len(p), 2):
        res[i], res[i + 1] = res[i + 1], res[i]
    # assert len(res) != 100
    if len(res) != 100:
        raise Exception("No 100!")
    return (get_way_len(res), res)

def mutate_3(way):
    l = random.randint(0, len(way) - 10)
    r = random.randint(l+9, len(way) - 1)
    res = list(way[:l])
    sh = list(way[l : r])
    sh.reverse()
    rest = list(way[r:])
    res.extend(sh)
    res.extend(rest)
    # assert len(res) != 100
    if len(res) != 100:
        raise Exception("No 100!")
    return (get_way_len(res), res)


def cross(w1, w2):
    pos = random.randint(0, len(w1) - 1)
    res = list()
    used = set()
    res.extend(w1[:pos])
    for x in res:
        used.add(x)
    res2 = list((w2[pos:]))
    for x in res2:
        if x not in used:
            res.append(x)
            used.add(x)
    all = set(range(len(w1)))
    all = all.difference(used)
    for x in all:
        res.append(x)

    return (get_way_len(res), res)

# def cross(w1, w2):
#     pos = random.randint(0, len(w1) - 1)
#     res1 = list()
#     res1.extend(w1[: pos])
#     res1.extend(w2[pos:])
#     ids = set(range(len(w1)))
#     res_ids = set()
#     for id in res1:
#         if id not in ids:
#             res_ids.add(id)
#         else:
#             ids.remove(id)
#     possible_pos = set( range(len(w1)) )
#     pos_ids = random.sample(range(len(w1)))
#     sorted(pos_ids)
#     for x in pos_ids:
#         if x in possible_pos:
#             possible_pos.remove(x)
#     possible_pos = list(possible_pos)
#     for i in range(pos_ids):
#         pos = pos_ids[i]
#

def main():
    n = len(cities)
    cur_way = list(range(n))
    random.shuffle(cur_way)
    # cur_way_len = get_way_len(cur_way)
    # print(cur_way_len)
    # print(n)
    generation = list()
    n_samples = 20
    for i in range(n_samples):
        new_way = list(range(n))
        random.shuffle(new_way)
        new_way = np.asarray(new_way)
        generation.append( ( get_way_len(new_way), new_way) )
    generation = sorted(generation)
    cur_way_len = generation[0][0]
    iter_id = 0
    while True:

        print("Iter id", iter_id, "cur way len", cur_way_len, [generation[i][0] for i in range(5)])
        if cur_way_len < 3000:
            x = [cities[id][0] for id in generation[0][1]]
            y = [cities[id][1] for id in generation[0][1]]
            plt.plot(x, y)
            plt.show()
            exit()
        for i in range(n):

            for j in range(1):
                generation.append(mutate_1(generation[i][1]))
                generation.append(mutate_2(generation[i][1]))
                # generation.append(mutate_2(generation[i][1]))
                # generation.append(mutate_2(generation[i][1]))
                generation.append(mutate_3(generation[i][1]))
                cur_way = list(range(n))
                random.shuffle(cur_way)
                generation.append((get_way_len(cur_way), cur_way))
        s = set(random.sample(range(n_samples), int(n_samples/2)))
        all = set(range(n_samples))
        all = all.difference(s)
        all = list(all)
        s = list(s)
        for i in range(len(s)):
            generation.append(cross(generation[s[i]][1], generation[all[i]][1]))


        ids = [ (generation[i][0], i) for i in range(len(generation))]
        ids.sort()
        generation = [ generation[i] for dst, i in ids]
        generation = generation[:n]
        cur_way_len = generation[0][0]
        iter_id += 1


if __name__ == "__main__":
    main()