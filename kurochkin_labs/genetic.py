import random
from math import *

bits_num = 31

h = 1e-7

lower_bound = -512.00001
upper_bound = 512.00001

def check_arg(x):
    return x >= lower_bound and x <= upper_bound

def ackley(x, y):
    return -20 * exp(-0.2 * sqrt(0.5 * (x ** 2 + y ** 2))) - exp(0.5 * (cos(2 * pi * x) + cos(2 * pi * y))) + e + 20

def eggholder(x, y):
    if not ( check_arg(x) and check_arg(y) ):
        return 1e18
    return -(y + 47)* sin(sqrt(abs(x/2.0 + (y + 47)))) - x * sin(sqrt(abs(x - (y + 47))))

def square_sum(x, y):
    return x * x + y * y

def target_function(pt):
    #return square_sum(pt[0], pt[1])
    #return  ackley(pt[0], pt[1])
    return eggholder(pt[0], pt[1])

def manhattan_distance(a, b):
    c = a ^ b
    cnt = 0
    for i in range(bits_num):
        if c & 1 != 0:
            cnt += 1
        c >>= 1
    return cnt

def manhattan_distance_list(a,b):
    ans = 0
    for i in range(len(a)):
        ans += manhattan_distance(a[i], b[i])
    return ans

def combine_2(a, b):
    aa = list()
    bb = list()
    for i in range(len(a)):
        c,d = combine(a[i],b[i])
        aa.append(c)
        bb.append(d)
    return aa, bb

def combine(a, b):
    c = a
    d = b
    lst = list()
    for i in range(bits_num):
        t = 1 << i
        l = c & t
        r = d & t
        if l != r:
            lst.append(i)
    random.shuffle(lst)
    lst = random.sample(lst, int( len(lst) / 2 ))
    for i in lst:
        t = 1 << i
        c ^= t
        d ^= t
    return c, d
    # for i in range(bits_num):
    #     if i > 0:
    #         c <<= 1
    #         d <<= 1
    #     if 0 == random.randint(0, 1):
    #         c |= a & 1
    #         d |= b & 1
    #     else:
    #         d |= a & 1
    #         c |= b & 1
    #     a >>=1
    #     b >>=1
    # return c, d

def gray_decode(g):
    ans = int(0)
    while g > 0:
        ans ^= g
        g >>= 1
    return ans

def mutate(a):
    ans = a
    cnt = 0
    thresh = 0.2
    for i in range(bits_num):
        r = random.uniform(0, 1)
        if r > thresh:
            continue
        cnt += 1
        ans ^= (1 << i)
    #print("Mutation", cnt / bits_num)
    return ans

def mutate_list(a):
    ans = list()
    for i in range(len(a)):
        ans.append(mutate(a[i]))
    return ans

def grayencode(g):
    return g ^ (g >> 1)

def get_real(a):
    return lower_bound + h * a

def get_real_list(a):
    ans = list()
    for i in range(len(a)):
        ans.append(get_real(a[i]))
    return ans

if __name__ == "__main__":
    n = 200
    threshold = 2
    n_iter = 10000
    val = int(1024 / h)
    cnt = 0
    # while val > 0:
    #     cnt+=1
    #     val >>= 1
    # print(cnt, get_real(1 << cnt))
    # exit()
    # g = grayencode(2)
    #-1909.1332554120117 [1090.7895238, 973.2847511
    # print(target_function([1090.7895238, 973.2847511]))
    # exit()
    # target_function([1, 2])
    assert n % 2 == 0
    generation = list()

    while(True):
        elem = [int(random.uniform(0, upper_bound - lower_bound) / h), int(random.uniform(0, upper_bound - lower_bound) / h)]
        generation.append(elem)
        if len(generation) == n:
            break
    generation_real = [get_real_list(e) for e in generation]
    for iter_id in range(n_iter):
        generation_real = [get_real_list(e) for e in generation]
        random.shuffle(generation)
        #make pairs
        ids = set(range(n))
        id1 = random.sample(range(n), int(n/2))
        for x in id1:
            ids.remove(x)
        id2 = list(ids)
        random.shuffle(id2)
        dst = [manhattan_distance_list(generation[id1[i]], generation[id2[i]]) for i in range(len(id1))]

        for i in range(len(dst)):
            if dst[i] <= threshold:
                continue
            a = generation[id1[i]]
            b = generation[id2[i]]
            c,d = combine_2(a, b)
            generation.append(c)
            generation.append(d)

        best = list()
        for i in range(len(generation)):
            pt = generation[i]
            best.append([target_function(get_real_list(pt)), generation[i]])
        best = sorted(best)
        print("iter", iter_id, "best", best[0][0], get_real_list(best[0][1]))
        new_generation = list()
        new_generation.append(best[0][1])
        for i in range(1, n):
            new_generation.append(mutate_list(best[i][1]))

        generation = new_generation