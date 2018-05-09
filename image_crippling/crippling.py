import os
import cv2
import random
import numpy as np
import shutil




def get_mask_way(img, inverse = False):
    h,w,c = img.shape
    st1 = (random.randint(0, int(2 * h / 3 - 1) ), 0)
    st2 = (0, random.randint(0, int(2 * w / 3 - 1)))
    cur = st1
    mask_edges = np.zeros((h, w), dtype=np.uint8)
    # top to right
    while True:
        x, y = cur
        if x >= h or y >= w:
            break
        mask_edges[x][y] = 255
        sw = np.random.choice([0, 1, 2], p=[ 0.1, 0.4, 0.5])
        if sw == 0:
            cur = (x + 1, y)
        else:
            if sw == 1:
                cur = (x, y + 1)
            else:
                cur = (x + 1, y + 1)

    cur = st2
    # left to down
    while True:
        x, y = cur
        if x >= h or y >= w:
            break
        mask_edges[x][y] = 255
        sw = np.random.choice([0, 1, 2], p=[ 0.4, 0.1, 0.5])
        if sw == 0:
            cur = (x + 1, y)
        else:
            if sw == 1:
                cur = (x, y + 1)
            else:
                cur = (x + 1, y + 1)
    filled = mask_edges.copy()
    cv2.floodFill(filled, None, (0, w - 1), 255)
    cv2.floodFill(filled, None, (h - 1, 0), 255)
    if inverse:
        filled = filled.T
    return filled == 255

def get_mask_canny(img1):
    x,y,z = img1.shape
    edges = cv2.Canny(img1, 25, 225)
    cv2.floodFill(edges, None, (int(x / 2), int(y/2)), 255)
    return edges == 255
    # cv2.imshow('canny', edges)
    # cv2.waitKey()
    # exit()


def get_mask_binarize(img1):
    im = img1.copy()
    x,y,z = im.shape
    gray = np.zeros((x,y), dtype=np.uint8)
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    ret, thresh1 = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    return thresh1 == 255


get_mask = dict()
get_mask['canny'] = get_mask_canny
get_mask['way'] = get_mask_way
get_mask['binarize'] = get_mask_binarize

def combine_2_imgs(img, img2, mask):
    res = img.copy()
    res[mask] = img2[mask]
    return res

def combine_2_imgs_path(img1_path, img2_path, mode = 'canny'):
    img = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)
    mask = get_mask[mode](img)
    return combine_2_imgs(img, img2, mask), mask

if __name__ == "__main__":

    mode = 'binarize'
    dataset_folder = 'D:/rtsd/rtsd-r3/rtsd_classy_ok/train/'
    output_folder = 'D:/rtsd/rtsd-r3/rtsd_classy_ok/new_cripples_' + mode
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder)
    cl_list = os.listdir(dataset_folder)

    for i in range(len(cl_list)):
        for j in range(i + 1, len(cl_list)):
            folder1 = os.path.join(dataset_folder, cl_list[i])
            folder2 = os.path.join(dataset_folder, cl_list[j])
            name1 = random.sample(os.listdir(folder1), 1)[0]
            name2 = random.sample(os.listdir(folder2), 1)[0]
            res, mask = combine_2_imgs_path(os.path.join(folder1, name1), os.path.join(folder2, name2), mode)
            im1 = cv2.imread(os.path.join(folder1, name1))
            im2 = cv2.imread(os.path.join(folder2, name2))
            cv2.imwrite(os.path.join(output_folder, str(i * 10 + j) + '.png'), res)
            cv2.imwrite(os.path.join(output_folder, str(i * 10 + j) + '_img1.png'), im1)
            cv2.imwrite(os.path.join(output_folder, str(i * 10 + j) + '_img2.png'), im2)
            cv2.imwrite(os.path.join(output_folder, str(i * 10 + j) + '_mask.png'), mask * 255)





