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

    init_once = 0
    num_objects = 2


    mask_rois = list()
    img_rois = list()
    contours = list()
    tracking_colors = [0 for i in range(num_objects)]

    init_step = 10

    for frame_id in range(imgs_cnt):


        prev_mask_rois = copy(mask_rois)
        prev_img_rois = copy(img_rois)
        prev_contours = copy(contours)

        mask_rois = list()
        img_rois = list()
        contours = list()

        img_name, mask_name = get_imgs_pair_by_id(imgs_files, frame_id)
        img_path = os.path.join(imgs_folderpath, img_name)
        mask_path = os.path.join(imgs_folderpath, mask_name)
        if not frame_id % init_step == 0:
            prev_img = copy(img)
            prev_mask = copy(mask)
            prev_img_gray = copy(img_gray)

        img = cv2.imread(img_path)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)

        img = cv2.resize(img, expected_img_size)
        mask = cv2.resize(mask, expected_img_size)
        img_gray = cv2.resize(img_gray, expected_img_size)

        if frame_id % init_step == 0:
            # init_once = False
            tracker = cv2.MultiTracker_create()
            for j in range(num_objects):

                bbox = cv2.selectROI("Tracking", img, False)
                # tracker.add(cv2.TrackerMIL_create(), img, bbox)
                x, y, w, h = bbox

                mask_roi = mask[y:y + h, x:x + w]
                kernel = np.ones((5, 5), np.uint8)
                # mask_roi = cv2.erode(mask_roi, kernel, iterations=1)
                img_roi = img[y:y + h, x:x + w]

                mask_rois.append(mask_roi)
                img_rois.append(img_roi)

                hist = cv2.calcHist([mask_roi], [0], None, [256], [0, 256])
                hist[0] = 0
                thresh = hist.argmax()
                tracking_colors[j] = thresh
                ret, obj_img = cv2.threshold(mask_roi, thresh - 1, 255, cv2.THRESH_BINARY)
                zero_mask = np.zeros_like(mask)
                zero_mask[y:y + h, x:x + w] = obj_img
                im2, ctrs, hierarchy = cv2.findContours(zero_mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
                contours.append(ctrs[0])
                ctr_bbox = cv2.boundingRect(ctrs[0])
                tracker.add(cv2.TrackerMIL_create(), img, ctr_bbox)
            demo = copy(img)
            for ctr_id in range(len(contours)):
                cv2.drawContours(demo, contours, ctr_id, (0, 255, 0), 3)
            cv2.imshow("Tracking", demo)
            cv2.waitKey()
            continue


        ok, boxes = tracker.update(img)
        demo = copy(img)
        for j in range(num_objects):

            # print(len(prev_contours))
            new_pts, st, err = cv2.calcOpticalFlowPyrLK(prev_img_gray, img_gray, prev_contours[j].astype(np.float32), None, **lk_params)
            good_pts = new_pts[st==1]


            ctr = list()
            tracker_box = boxes[j]
            x,y,w,h = [int(e) for e in tracker_box]
            cv2.rectangle(demo, (x, y), (x + w, y + h), (0, 0, 255), 3)
            # print(good_pts)
            contour_box = cv2.boundingRect(good_pts)
            x,y,w,h = contour_box
            cv2.rectangle(demo, (x,y ), (x + w, y + h), (0, 255, 0), 3)

            for pt in good_pts:
                try:
                    x,y = pt.ravel()
                    ctr.append([[int(x), int(y)]])
                except Exception as e:
                    print("oops")
            contours.append(np.asarray(ctr))
            cv2.drawContours(demo, contours, j, (0, 255, 0), 3)

            color = tracking_colors[j]
            area_true = (mask == color).astype(np.uint8)*255
            x, y, w, h = [int(e) for e in tracker_box]
            area_contour = np.zeros_like(area_true)
            cv2.drawContours(area_contour, contours, j, 255, cv2.FILLED)
            area_true = area_true[y:y + h, x:x + w]
            area_contour = area_contour[y:y + h, x:x + w]
            # cv2.imshow("Tracking", area_contour)
            # cv2.waitKey()
            area_tp = cv2.bitwise_and(area_true, area_contour)
            area_fn = cv2.bitwise_and(area_true, cv2.bitwise_not(area_contour))
            area_fp = cv2.bitwise_and(cv2.bitwise_not(area_true), area_contour)
            area_tn = cv2.bitwise_and(cv2.bitwise_not(area_true), cv2.bitwise_not(area_contour))

            # cv2.imshow("Tracking", area_tp)
            # cv2.waitKey()
            tp = cv2.countNonZero(area_tp)
            fn = cv2.countNonZero(area_fn)
            fp = cv2.countNonZero(area_fp)
            tn = cv2.countNonZero(area_tn)

            precision = tp/(tp + fp)
            recall = tp/(tp + fn)

            print("Object", j)
            print("precision", precision)
            print("recall", recall)


        cv2.imshow("Tracking", demo)
        cv2.waitKey()
        # for newbox in boxes:
        # cv.DrawContours(image3, contourmov, cv.CV_RGB(0, 255, 0), cv.CV_RGB(0, 255, 0), 1, cv.CV_FILLED)
if __name__ == "__main__":
    main()