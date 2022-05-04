import json
import os
from tqdm import tqdm


def get_coco_id(category):
    if category == 'Minibus':
        return 1
    elif category == 'cyclist':
        return 2
    elif category == 'pedestrian':
        return 3
    else:
        return 0


def in_ipu1imgfov(obj):
    bbox2d = [float(i) for i in obj.split()[4:8]]
    bbox3d = [float(i) for i in obj.split()[15:18]]
    if 0 < bbox2d[0] < 1920 and 0 < bbox2d[2] < 1920 and 0 < bbox2d[1] < 1080 and 0 < bbox2d[3] < 1080 and bbox3d[0] > 0:
        # if 0 < bbox2d[0] < 1920 and 0 < bbox2d[2] < 1920 and 0 < bbox2d[1] < 1080 and 0 < bbox2d[3] < 1080:
        return 1
    else:
        return 0


def in_ipu2imgfov(obj):
    bbox2d = [float(i) for i in obj.split()[8:12]]
    bbox3d = [float(i) for i in obj.split()[15:18]]
    if 0 < bbox2d[0] < 1920 and 0 < bbox2d[2] < 1920 and 0 < bbox2d[1] < 1080 and 0 < bbox2d[3] < 1080 and bbox3d[0] < 90:
        return 1
    else:
        return 0


def main():
    save_file = 'IPS300+_coco/annotations/val.json'
    img_path = 'IPS300+_coco/val'
    anno_path = 'IPS300+_detection/label/txt'
    imgs = sorted(os.listdir(img_path))
    annotationid = 0

    # coco
    coco_json = {}
    coco_json['images'] = []
    coco_json['annotations'] = []
    coco_json['categories'] = []

    # coco_categories
    category = {}
    category['name'] = 'car'
    category['id'] = 1
    coco_json['categories'].append(category)
    category = {}
    category['name'] = 'cyclist'
    category['id'] = 2
    coco_json['categories'].append(category)
    category = {}
    category['name'] = 'pedestrian'
    category['id'] = 3
    coco_json['categories'].append(category)
    category = {}

    for img in tqdm(imgs):
        is_ipu1 = "IPU1" in img
        if is_ipu1:
            label = img.replace('_IPU1_CAM1_UNDISTORT.jpg', '_LABEL.txt')
        else:
            label = img.replace('_IPU2_CAM1_UNDISTORT.jpg', '_LABEL.txt')
        labelpath = os.path.join(anno_path, label)
        with open(labelpath, 'r') as f:
            anno = f.readlines()

        # coco_images
        if is_ipu1:
            # ipu1cam1
            image = {}
            image['id'] = int(img[0:6])
            image['width'] = 1920
            image['height'] = 1080
            image['file_name'] = img
            coco_json['images'].append(image)
        else:
            # ipu2cam1
            image = {}
            image['id'] = int(1e6 + int(img[0:6]))
            image['width'] = 1920
            image['height'] = 1080
            image['file_name'] = img
            coco_json['images'].append(image)

        # coco_annotations
        for obj in anno:
            # ipu1cam1
            if in_ipu1imgfov(obj) and get_coco_id(obj.split()[0]) and is_ipu1:
                # if 1:
                annotation = {}
                annotation['id'] = annotationid
                annotationid += 1
                annotation['image_id'] = int(img[0:6])
                annotation['iscrowd'] = 0
                annotation['bbox'] = [float(i) for i in obj.split()[4:8]]
                annotation['bbox'][2] = annotation['bbox'][2] - \
                    annotation['bbox'][0]
                annotation['bbox'][3] = annotation['bbox'][3] - \
                    annotation['bbox'][1]
                annotation['area'] = annotation['bbox'][2] * \
                    annotation['bbox'][3]
                annotation['segmentation'] = None
                annotation['category_id'] = get_coco_id(obj.split()[0])
                coco_json['annotations'].append(annotation)
            # ipu2cam1
            if in_ipu2imgfov(obj) and get_coco_id(obj.split()[0]) and (not is_ipu1):
                # if 1:
                annotation = {}
                annotation['id'] = annotationid
                annotationid += 1
                annotation['image_id'] = int(1e6 + int(img[0:6]))
                annotation['iscrowd'] = 0
                annotation['bbox'] = [float(i) for i in obj.split()[8:12]]
                annotation['bbox'][2] = annotation['bbox'][2] - \
                    annotation['bbox'][0]
                annotation['bbox'][3] = annotation['bbox'][3] - \
                    annotation['bbox'][1]
                annotation['area'] = annotation['bbox'][2] * \
                    annotation['bbox'][3]
                annotation['segmentation'] = None
                annotation['category_id'] = get_coco_id(obj.split()[0])
                coco_json['annotations'].append(annotation)
    with open(save_file, 'w') as fp:
        json.dump(coco_json, fp)


if __name__ == "__main__":
    main()
