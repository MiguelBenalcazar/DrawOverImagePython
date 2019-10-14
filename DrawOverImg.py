# ______________________________________________________________________________________________________________________#
# INSERT PATH TO READ THE WHOLE IMAGES IN img_path
# KEYBOARD OPTIONS
# p to draw over the mask and mark the defect
# q to draw a square over the original image
# e to delete part of the mask
# s to save the mask in the same path
# o to save the original image in the same path (it will overwrite the original file)
# esc to close
# ______________________________________________________________________________________________________________________
# written by mabh

import cv2
import numpy as np
import os

img_path = 'C:/Users/Miguel/Desktop/img/'

drawing = False  # true if mouse is pressed
mode = True
square = False
eraser_mode = False
ix, iy = -1, -1
k = 'p'


# mouse callback function
def draw_event(event, x, y, flags, param):
    global ix, iy, drawing, mode, square, eraser_mode
    size = 10
    pencil = (25, 25, 25)
    eraser = (0, 0, 0)

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            if mode:
                cv2.line(img, (ix, iy), (x, y), pencil, size)
                ix = x
                iy = y
            elif square:
                cv2.rectangle(img, (ix, iy), (x, y), (0, 0, 0), -1)
            elif eraser_mode:
                cv2.line(img, (ix, iy), (x, y), eraser, size)
                ix = x
                iy = y

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        if mode:
            cv2.circle(img, (x, y), size, pencil, -1)
        elif square:
            cv2.rectangle(img, (ix, iy), (x, y), (0, 0, 0), -1)
        elif eraser_mode:
            cv2.circle(img, (x, y), size, eraser, -1)


entries = os.scandir(img_path)
for i in entries:
    if i.name.find("mask") == -1 and i.name.find("LabelMask") == -1:
        img_original = img_path + i.name
        img_mask = img_path + i.name.split('.')[0] + '_mask.png'
        print(img_original)
        imgOriginal = cv2.imread(img_original)
        w, h, d = tuple(imgOriginal.shape)
        img = imgMask = np.zeros((w, h, d), np.uint8)
        cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('image', 1200, 900)
        cv2.setMouseCallback('image', draw_event)

        while 1:
            imgShow = cv2.addWeighted(imgOriginal, 0.8, imgMask, 0.9, 0)
            cv2.imshow('image', imgShow)
            k = cv2.waitKey(1) & 0xFF
            if k == ord('p'):  # pencil
                mode = True
                square = False
                eraser_mode = False
                print('Function to draw over the mask')
                img = imgMask
            elif k == ord('q'):
                mode = False
                square = True
                eraser_mode = False
                print('Function to draw an square over the original image')
                img = imgOriginal
            elif k == ord('e'):
                mode = False
                square = False
                eraser_mode = True
                print('Function to delete part of the mask')
                img = imgMask
            elif k == ord('s'):  # save mask
                cv2.imwrite(img_mask, imgMask)
            elif k == ord('o'):  # save original image
                cv2.imwrite(img_original, imgOriginal)

            elif k == 27:
                break

        cv2.destroyAllWindows()
