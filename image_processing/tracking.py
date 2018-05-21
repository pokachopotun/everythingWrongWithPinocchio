import os
import cv2
import pickle
import numpy as np
from copy import copy

expected_img_size = (600, 400)

def get_imgs_pair_by_id(imgs, id):
    return imgs[2 * id], imgs[2 * id + 1]


# Parameters for lucas kanade optical flow
lk_params = dict( winSize  = (15,15),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))


def main():
    imgs_folderpath = os.path.relpath('./imgs/')
    imgs_files = os.listdir(imgs_folderpath)
    imgs_cnt = int(len(imgs_files) / 2)

    init_once = True
    num_objects = 1
    tracker = cv2.MultiTracker_create()

    mask_rois = list()
    img_rois = list()
    contours = list()

    for i in range(imgs_cnt):


        prev_mask_rois = copy(mask_rois)
        prev_img_rois = copy(img_rois)
        prev_contours = copy(contours)

        mask_rois = list()
        img_rois = list()
        contours = list()

        img_name, mask_name = get_imgs_pair_by_id(imgs_files, i)
        img_path = os.path.join(imgs_folderpath, img_name)
        mask_path = os.path.join(imgs_folderpath, mask_name)
        if not init_once:
            prev_img = copy(img)
            prev_mask = copy(mask)
            prev_img_gray = copy(img_gray)

        img = cv2.imread(img_path)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)

        img = cv2.resize(img, expected_img_size)
        mask = cv2.resize(mask, expected_img_size)
        img_gray = cv2.resize(img_gray, expected_img_size)

        if init_once:
            init_once = False
            for j in range(num_objects):
                bbox = cv2.selectROI("Tracking", img, False)
                tracker.add(cv2.TrackerMIL_create(), img, bbox)
                x, y, w, h = bbox

                mask_roi = mask[y:y + h, x:x + w]
                img_roi = img[y:y + h, x:x + w]

                mask_rois.append(mask_roi)
                img_rois.append(img_roi)

                hist = cv2.calcHist([mask_roi], [0], None, [256], [0, 256])
                hist[0] = 0
                thresh = hist.argmax()
                ret, obj_img = cv2.threshold(mask_roi, thresh - 1, 255, cv2.THRESH_BINARY)
                zero_mask = np.zeros_like(mask)
                zero_mask[y:y + h, x:x + w] = obj_img
                im2, ctrs, hierarchy = cv2.findContours(zero_mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
                contours.append(ctrs[0])
            demo = copy(img)
            for ctr_id in range(len(contours)):
                cv2.drawContours(demo, contours, ctr_id, (0, 255, 0), 3)
            cv2.imshow("Tracking", demo)
            cv2.waitKey()
            continue

        # params for ShiTomasi corner detection
        # feature_params = dict(maxCorners=100,
        #                       qualityLevel=0.3,
        #                       minDistance=7,
        #                       blockSize=7)
        # # Parameters for lucas kanade optical flow
        # lk_params = dict(winSize=(15, 15),
        #                  maxLevel=2,
        #                  criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
        # Create some random colors
        # color = np.random.randint(0, 255, (100, 3))
        # Take first frame and find corners in it
        # p0 = cv2.goodFeaturesToTrack(prev_img_gray, mask=None, **feature_params)

        ok, boxes = tracker.update(img)
        # calculate optical flow
        new_pts, st, err = cv2.calcOpticalFlowPyrLK(prev_img_gray, img_gray, prev_contours[0].astype(np.float32), None, **lk_params)

        good_pts = new_pts[st==1]
        # flow = cv2.calcOpticalFlowFarneback(prev_img_gray, img_gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        #
        # hsv = np.zeros_like(img)
        # hsv[..., 1] = 255
        #
        # mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        # hsv[..., 0] = ang * 180 / np.pi / 2
        # hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
        # bgr = np.zeros_like(img)
        # cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR, dst = bgr)
        # cv2.imshow('frame2', bgr)
        # cv2.waitKey()

        # prvs = next
        # contours.append(new_pts)
        # Select good points
        # good_new = p1[st == 1]
        # good_old = p0[st == 1]
        # draw the tracks
        # for i, (new, old) in enumerate(zip(good_new, good_old)):
        #     a, b = new.ravel()
        #     c, d = old.ravel()
        #     mask = cv2.line(mask, (a, b), (c, d), color[i].tolist(), 2)
        #     frame = cv2.circle(frame, (a, b), 5, color[i].tolist(), -1)
        demo = copy(img)
        ctr = list()
        for new_box in boxes:
            x,y,w,h = [int(e) for e in new_box]
            cv2.rectangle(demo, (x, y), (x + w, y + h), (0, 255, 0), 3)
        print(good_pts)
        for pt in good_pts:
            x,y = pt.ravel()
            ctr.append([[int(x), int(y)]])
            demo[int(y), int(x)] = (0,0,255)
        contours.append(np.asarray(ctr))
        cv2.imshow("Tracking", demo)
        cv2.waitKey()
        # for newbox in boxes:



    return


if __name__ == "__main__":
    main()