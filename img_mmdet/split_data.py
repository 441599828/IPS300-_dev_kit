import os
import random
from tqdm import tqdm
from shutil import copy
def randomsplit():
    Img_root = "IPS300+_detection/data"
    Img_dst="IPS300+_coco"
    Img = []
    for root, dirs, files in os.walk(Img_root):
        for file in files:
            if os.path.splitext(file)[1] == '.jpg':
                Img.append(os.path.join(root, file).replace(Img_root + '/', ''))
            else:
                print("None")
    Img.sort()

    # random split data in train:val:test=6:2:2
    random.shuffle(Img)
    train = Img[0:int(6 / 10 * len(Img))]
    val = Img[int(6 / 10 * len(Img)):int(8 / 10 * len(Img))]
    test = Img[int(8 / 10 * len(Img)):]

    for i in tqdm(train):
        copy(os.path.join(Img_root,i),os.path.join(Img_dst,'train',i.split('/')[-1]))
    for i in tqdm(val):
        copy(os.path.join(Img_root,i),os.path.join(Img_dst,'val',i.split('/')[-1]))
    for i in tqdm(test):
        copy(os.path.join(Img_root,i),os.path.join(Img_dst,'test',i.split('/')[-1]))


if __name__ == "__main__":
    randomsplit()