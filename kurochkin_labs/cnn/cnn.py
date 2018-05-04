import mxnet as mx
import shutil
import os
import numpy as np
import cv2
from collections import namedtuple
Batch = namedtuple('Batch', ['data'])

import argparse
import logging
logging.basicConfig(level=logging.DEBUG)
#
# def load_image_mxnet(fname, load_color = True):
#     if not load_color:
#         raise("grayscale not implemented")
#     img = cv2.imread(fname)
#     if img is None:
#         return None
#     # convert into format (batch, RGB, width, height)
#     img = cv2.resize(img, (32, 32))
#     img = np.swapaxes(img, 0, 2)
#     img = np.swapaxes(img, 1, 2)
#     tmp = np.zeros((3, 32, 32), np.float32)
#     cv2.normalize(img, tmp, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
#     img = tmp
#     img = img[np.newaxis, :]
#     return img


def train_net(init):
    data_iter = get_data_iter(init)
    from importlib import import_module
    net = import_module('symbols.lenet')
    out_layer = net.get_symbol(init.classes_cnt)
    model = mx.mod.Module(out_layer, context=mx.gpu())
    model.bind(data_shapes=data_iter[0].provide_data, label_shapes=data_iter[0].provide_label)
    model.init_params()

    model.fit(train_data=data_iter[0], eval_data=data_iter[1], optimizer='adam',
              optimizer_params={'learning_rate': 0.001},
              eval_metric='acc', num_epoch=30, begin_epoch=0
              )

    if os.path.join(init.output_netpath):
        shutil.rmtree(init.output_netpath)
    os.mkdir(init.output_netpath)
    prefix = init.output_netpath + 'mxnet'
    model.save_checkpoint(prefix, 0)

def run_im2rec(dataset_folderpath, output_folderpath, prefix_filename):
    im2rec_path = 'D:/incubator-mxnet/tools/im2rec.py'
    im2rec_f = output_folderpath + prefix_filename
    command1 = 'C:/Users/Denis/Anaconda3/python.exe ' + im2rec_path + ' --list --exts .png --train-ratio 1.0 --test-ratio 0.0 --recursive ' + \
                im2rec_f + " " + dataset_folderpath
    command2 = 'C:/Users/Denis/Anaconda3/python.exe ' + im2rec_path + ' --num-thread 4 --quality 9 --pack-label ' + im2rec_f + ' ' + dataset_folderpath
    print(command1)
    os.system(command1)
    print(command2)
    os.system(command2)


def get_data_iter(init):
    train_rec = 'D:/rtsd/rtsd-r3/rtsd_classy_ok/train.rec/'
    test_rec = 'D:/rtsd/rtsd-r3/rtsd_classy_ok/test.rec/'
    # run_im2rec(init.output_train_folder, train_rec, 'rec')
    # run_im2rec(init.testing_dataset_path, test_rec, 'rec')
    # train_lbl, train_img = read_data(init.output_train_folder, init.label_id)
    # from copy import copy
    # val_lbl, val_img = read_data(init.testing_dataset_path, init.label_id)
    # #
    # # train = mx.io.NDArrayIter(to4d(train_img), train_lbl, init.batch_size, shuffle=True)
    # # val = mx.io.NDArrayIter(to4d(val_img), val_lbl, init.batch_size)
    train_iter = mx.io.ImageRecordIter(
        path_imgrec=train_rec + 'rec.rec',
        data_shape=(3, 32, 32),  # output data shape.
        batch_size=32,  # number of samples per batch
        std_r = 255,
        std_g = 255,
        std_b = 255
    )
    test_iter = mx.io.ImageRecordIter(
        path_imgrec=test_rec + 'rec.rec',
        data_shape=(3, 32, 32),  # output data shape. An 227x227 region will be cropped from the original image.
        batch_size=32,  # number of samples per batch
        std_r = 255,
        std_g = 255,
        std_b = 255
    )
    return (train_iter, test_iter)

class trainValIndividualConfig():
    def __init__(self):
        num_to_classes_csv = 'D:/rtsd/rtsd-r3/rtsd-r3/numbers_to_classes.csv'

        self.anaconda3_path =

        with open('labels.txt', 'r') as file:
            self.labels = [x.strip() for x in file]

        # self.test_folder = '/media/denis/Data/article/iterations/datasets/mnist.original.test/'
        #
        # self.train_folder = '/media/denis/Data/article/iterations/datasets/train.100.random/'

        self.output_netpath = 'D:/rtsd/rtsd-r3/rtsd_classy_ok/trained_net/'



        # self.dataset_size = 10 * 100

        self.batch_size = 64

        self.classes_cnt = 10

        # self.pattern_netpath = '/media/denis/Data/article/iterations/networks/lenet_pattern/'

        # self.labels_filepath = '/media/denis/Linux/article/rejector_mapping.txt'


        # ----------USER CONFIG END-----------------------


def cv_resize_tree(path):
    for cl in os.listdir(path):
        cl_path = os.path.join(path, cl)
        if not os.path.isdir(cl_path):
            continue
        for img in os.listdir(cl_path):
            impath =  os.path.join(cl_path, img)
            img = cv2.imread(impath)
            img = cv2.resize(img, (32, 32))
            cv2.imwrite(impath, img)


def load_image_mxnet(fname, load_color = True):
    if not load_color:
        raise("grayscale not implemented")
    img = cv2.imread(fname)
    if img is None:
        return None
    # convert into format (batch, RGB, width, height)
    img = cv2.resize(img, (32, 32))
    img = np.swapaxes(img, 0, 2)
    img = np.swapaxes(img, 1, 2)
    tmp = np.zeros((3, 32, 32), np.float32)
    cv2.normalize(img, tmp, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
    img = tmp
    img = img[np.newaxis, :]
    return img


def to4d(img):
    return img.reshape(img.shape[0], 3, 32, 32).astype(np.float32)

def test_signle_image(init, image_filepath):
    input_shape = (1, 3, 32, 32)
    ctx = mx.gpu()
    sym, arg_params, aux_params = mx.model.load_checkpoint(init.output_netpath + 'mxnet', 0)
    mod = mx.mod.Module(symbol=sym, context=ctx, label_names=None)
    mod.bind(for_training=False, data_shapes=[('data', input_shape)],
             label_shapes=mod._label_shapes)
    mod.set_params(arg_params, aux_params, allow_missing=True)
    load_color = input_shape[1] == 3

    img = to4d(load_image_mxnet(image_filepath, load_color))
    mod.forward(Batch([mx.nd.array(img)]))
    res = mod.get_outputs()[0].asnumpy()

    print('answer is', init.labels[ res.argmax() ])

if __name__ == "__main__":
    # init = trainValIndividualConfig()
    #
    # cv_resize_tree('D:/rtsd/rtsd-r3/rtsd_classy_ok/train/')
    # cv_resize_tree('D:/rtsd/rtsd-r3/rtsd_classy_ok/test/')
    #
    # train_rec = 'D:/rtsd/rtsd-r3/rtsd_classy_ok/train.rec/'
    # test_rec = 'D:/rtsd/rtsd-r3/rtsd_classy_ok/test.rec/'
    # run_im2rec('D:/rtsd/rtsd-r3/rtsd_classy_ok/train/', train_rec, 'rec')
    # run_im2rec('D:/rtsd/rtsd-r3/rtsd_classy_ok/test/', test_rec, 'rec')

    # with open('labels.txt', 'w') as file:
    #     path = 'D:/rtsd/rtsd-r3/rtsd_classy_ok/test'
    #     for x in os.listdir(path):
    #         file.write(x + os.linesep)
    # exit()

    init = trainValIndividualConfig()

    if False:
        train_net(init)
    else:
        image_filepath = 'D:/rtsd/rtsd-r3/rtsd_classy_ok/train/1_22/000685.png'
        test_signle_image(init, image_filepath)


