import os
import random
from shutil import copy
from tqdm import tqdm
from PIL import Image
import numpy as np
import json


def IPS2KITTI(labelpath, dst):
    with open(labelpath, 'r') as f:
        anno = json.load(f)
    f.close()

    with open(dst, "w") as file:
        for ann in anno['objects']:
            is_valid = 0
            category = ann['label']
            if 'Minibus' in category:
                ann_kitti_line = 'Car'
                is_valid = 1
            elif 'pedestrian' in category:
                ann_kitti_line = 'Pedestrian'
                is_valid = 1
            elif 'cyclist' in category:
                is_valid = 1
                ann_kitti_line = 'Cyclist'

            if is_valid:
                # truncation_attributes
                ann_kitti_line = ann_kitti_line + ' ' + '0.00'
                # occlusion_attributes
                ann_kitti_line = ann_kitti_line + ' ' + '0'
                # alpha
                ann_kitti_line = ann_kitti_line + ' ' + '0.00'
                # 2d box
                ann_kitti_line = ann_kitti_line + ' ' + str(ann['box2d']['camera1']['x']) + ' ' + str(ann['box2d']['camera1']['y'])+' '+str(
                    ann['box2d']['camera1']['x'] + ann['box2d']['camera1']['width'])+' '+str(ann['box2d']['camera1']['y'] + ann['box2d']['camera1']['height'])
                # 3d H_W_L
                ann_kitti_line = ann_kitti_line + ' ' + str(ann['dimensions']['height'])+' ' + str(
                    ann['dimensions']['width'])+' ' + str(ann['dimensions']['length'])
                # 3d center
                x_lidar = ann['center']['x']
                y_lidar = ann['center']['y']
                z_lidar = ann['center']['z'] - ann['dimensions']['height']/2
                x_cam = -y_lidar
                y_cam = -z_lidar
                z_cam = x_lidar
                ann_kitti_line = ann_kitti_line + ' ' + \
                    str(x_cam)+' ' + str(y_cam)+' '+str(z_cam)
                # r_y
                if ann['rotation']['z'] <= (0.5*np.pi):
                    ann_kitti_line = ann_kitti_line + ' ' + \
                        str((-0.5*np.pi - ann['rotation']['z']))
                else:
                    ann_kitti_line = ann_kitti_line + ' ' + \
                        str((1.5*np.pi - ann['rotation']['z']))
                ann_kitti_line = ann_kitti_line + '\n'
                file.write(ann_kitti_line)
    file.close()


def randomsplit():
    lidar_root = "/media/whn/新加卷/dataset/IPS300+/IPS300+_public/IPS300+_detection/data/bin_COM_ROI"
    os.mkdir('./training')
    os.mkdir('./testing')
    os.mkdir('./ImageSets')
    os.mkdir('./training/velodyne')
    os.mkdir('./training/label_2')
    os.mkdir('./training/image_2')
    os.mkdir('./training/calib')
    os.mkdir('./testing/velodyne')
    os.mkdir('./testing/label_2')
    os.mkdir('./testing/image_2')
    os.mkdir('./testing/calib')

    lidar = []
    for root, dirs, files in os.walk(lidar_root):
        for file in files:
            if os.path.splitext(file)[1] == '.bin':
                lidar.append(os.path.join(
                    root, file).replace(lidar_root + '/', '').replace('_COM_ROI.bin', ''))
            else:
                print("None")
    lidar.sort()

    # random split data in train:val:test=6:2:2
    random.shuffle(lidar)
    train = lidar[0:int(6 / 10 * len(lidar))]
    val = lidar[int(6 / 10 * len(lidar)):int(8 / 10 * len(lidar))]
    test = lidar[int(8 / 10 * len(lidar)):]
    trainval = lidar[0:int(8 / 10 * len(lidar))]
    f = open("./ImageSets/train.txt", "w")
    splitstr = '\n'
    f.write(splitstr.join(train))
    f.close()

    f = open("./ImageSets/val.txt", "w")
    f.write(splitstr.join(val))
    f.close()

    f = open("./ImageSets/trainval.txt", "w")
    f.write(splitstr.join(trainval))
    f.close()

    f = open("./ImageSets/test.txt", "w")
    f.write(splitstr.join(test))
    f.close()

    for i in tqdm(trainval, 'converting trainval data:'):
        img_path = os.path.join(
            '/media/whn/新加卷/dataset/IPS300+/IPS300+_public/IPS300+_detection/data/IPU1/IPU1_cam1_undistort', i+'_IPU1_CAM1_UNDISTORT.jpg')
        img_png = Image.open(img_path).convert('RGBA')
        img_png.save(os.path.join('./training/image_2', i+'.png'))
        calib = 'calib.txt'
        copy(calib, os.path.join('./training/calib', i+'.txt'))
        label = os.path.join(
            '/media/whn/新加卷/dataset/IPS300+/IPS300+_public/IPS300+_detection/label/json', i + '_LABEL.json')
        IPS2KITTI(label, os.path.join('./training/label_2', i+'.txt'))
        i = os.path.join(lidar_root, i + '.bin')
        copy(i.replace('.bin', '_COM_ROI.bin'),
             i.replace(lidar_root, "./training/velodyne"))
    for i in tqdm(test, 'converting test data:'):
        img_path = os.path.join(
            '/media/whn/新加卷/dataset/IPS300+/IPS300+_public/IPS300+_detection/data/IPU1/IPU1_cam1_undistort', i+'_IPU1_CAM1_UNDISTORT.jpg')
        img_png = Image.open(img_path).convert('RGBA')
        img_png.save(os.path.join('./testing/image_2', i+'.png'))
        calib = 'calib.txt'
        copy(calib, os.path.join('./testing/calib', i+'.txt'))
        label = os.path.join(
            '/media/whn/新加卷/dataset/IPS300+/IPS300+_public/IPS300+_detection/label/json', i + '_LABEL.json')
        IPS2KITTI(label, os.path.join('./testing/label_2', i+'.txt'))
        i = os.path.join(lidar_root, i + '.bin')
        copy(i.replace('.bin', '_COM_ROI.bin'),
             i.replace(lidar_root, "./testing/velodyne"))


if __name__ == "__main__":
    randomsplit()
