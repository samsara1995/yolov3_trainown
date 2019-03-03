import xml.etree.ElementTree as ET
import pickle
import string
import os
import shutil
from os import listdir, getcwd
from os.path import join
import cv2

sets = [('2012', 'train')]

classes = ["person", "laptop", "phone"]


def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)


def convert_annotation(image_id, flag, savepath):
    if flag == 0:
        in_file = open(savepath + '/xml/trainImageXML/%s.xml' % (os.path.splitext(image_id)[0]))
        out_file = open(savepath + '/label/trainImage/%s.txt' % (os.path.splitext(image_id)[0]), 'w')
        tree = ET.parse(in_file)
        root = tree.getroot()
        size = root.find('size')

        img = cv2.imread('/nfs/tmp/pycharm_project_350/sucai/image/trainImage/' + str(image_id))
        print("read",image_id)
        h = img.shape[0]
        w = img.shape[1]

    elif flag == 1:
        in_file = open(savepath + '/xml/validateImageXML/%s.xml' % (os.path.splitext(image_id)[0]))
        out_file = open(savepath + '/label/validateImage/%s.txt' % (os.path.splitext(image_id)[0]), 'w')

        tree = ET.parse(in_file)
        root = tree.getroot()
        size = root.find('size')
        img = cv2.imread('/nfs/tmp/pycharm_project_350/sucai/image/validateImage/' + str(image_id))

        print('read',image_id)
        h = img.shape[0]
        #print(h)
        w = img.shape[1]
        #print(w)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


wd = getcwd()

for year, image_set in sets:
    savepath ="/nfs/tmp/pycharm_project_350/sucai"   #os.getcwd();
    idtxt = savepath + "/image/validateImageId.txt";
    pathtxt = savepath + "/image/validateImagePath.txt";
    image_ids = open(idtxt).read().strip().split()
    list_file = open(pathtxt, 'w')
    s = '\xef\xbb\xbf'
    for image_id in image_ids:
        nPos = image_id.find(s)
        if nPos >= 0:
            image_id = image_id[3:]
        list_file.write('/nfs/tmp/pycharm_project_350/sucai/image/validateImage/%s\n' % (image_id))
        print(image_id)
        type =['jpeg','bmp','jpg','png']
        '''
        letters = ['A','B','C','D','E','F','G']
        if 'A' in letters:
           print('A'+' exists')
        '''
        find_str='.'
        id_num=image_id.find(find_str)
        image_id_1=image_id[id_num+1:len(image_id)]
        #print(image_id_1)
        if image_id_1 in type:
            convert_annotation(image_id, 1, savepath)
            print("save\n")
    list_file.close()

    idtxt = savepath + "/image/trainImageId.txt";
    pathtxt = savepath + "/image/trainImagePath.txt";
    image_ids = open(idtxt).read().strip().split()
    list_file = open(pathtxt, 'w')
    s = '\xef\xbb\xbf'
    for image_id in image_ids:
        nPos = image_id.find(s)
        if nPos >= 0:
            image_id = image_id[3:]
        list_file.write('/nfs/tmp/pycharm_project_350/sucai/image/trainImage/%s\n' % (image_id))
        print(image_id)
        type =['jpeg','bmp','jpg','png']
        find_str='.'
        id_num=image_id.find(find_str)
        image_id_1=image_id[id_num+1:len(image_id)]
        #print(image_id_1)
        if image_id_1 in type:
            convert_annotation(image_id, 0, savepath)
            print("save\n")
    list_file.close()