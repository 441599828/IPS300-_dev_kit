# -*- coding: utf-8 -*-
import os
import cv2
import numpy as np
from tqdm import tqdm
from PIL import Image


def calcu_mean_var(tr_img_pth, tr_img_files):
    totalRGB = np.asarray([0, 0, 0], dtype=np.longlong)
    totalVar = np.asarray([0, 0, 0], dtype=np.float64)
    meanRGB = np.asarray([0, 0, 0], dtype=np.float64)
    varRGB = np.asarray([0, 0, 0], dtype=np.float64)
    for img_file in tqdm(tr_img_files, desc="calculating mean", mininterval=0.1):
        img_file = os.path.join(tr_img_pth, img_file)
        img = cv2.imread(img_file, -1)
        totalRGB[0] += np.sum(img[:, :, 0])
        totalRGB[1] += np.sum(img[:, :, 1])
        totalRGB[2] += np.sum(img[:, :, 2])
    img_size = img.shape[:2]
    total_pixels = img_size[0] * img_size[1] * len(tr_img_files)
    meanRGB[0] = totalRGB[0] / total_pixels
    meanRGB[1] = totalRGB[1] / total_pixels
    meanRGB[2] = totalRGB[2] / total_pixels
    for img_file in tqdm(tr_img_files, desc="calculating var", mininterval=0.1):
        img_file = os.path.join(tr_img_pth, img_file)
        img = cv2.imread(img_file, -1)
        totalVar[0] += np.sum((img[:, :, 0] - meanRGB[0]) ** 2)
        totalVar[1] += np.sum((img[:, :, 1] - meanRGB[1]) ** 2)
        totalVar[2] += np.sum((img[:, :, 2] - meanRGB[2]) ** 2)
    varRGB[0] = np.sqrt(totalVar[0] / total_pixels)
    varRGB[1] = np.sqrt(totalVar[1] / total_pixels)
    varRGB[2] = np.sqrt(totalVar[2] / total_pixels)
    print("img_size:{}x{}".format(img_size[1], img_size[0]))
    print("meanRGB:{}".format(meanRGB))
    print("stdRGB:{}".format(varRGB))


if __name__=='__main__':
    tr_img_pth = "/home/whn/data/IPS300+_Image/111"
    tr_img_files = os.listdir(tr_img_pth)
    # tr_img_files = []
    # for root, dirs, files in os.walk(tr_img_pth):
    #     for file in files:
    #         # if os.path.splitext(file)[1] == '.png':
    #         if '.jpg' in file:
    #             tr_img_files.append(os.path.join(root, file).replace(tr_img_pth + '/', ''))
    tr_img_files.sort()
    calcu_mean_var(tr_img_pth, tr_img_files)
    
# img_size:1920x1080
# meanRGB:[42.86279973 46.89367239 65.62468819]
# stdRGB:[23.86178607 21.95576749 24.78731827]