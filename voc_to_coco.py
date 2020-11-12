import xml.etree.ElementTree as ET
import os
import argparse

from os import getcwd

argument_parser = argparse.ArgumentParser()
argument_parser.add_argument('--annotation')
argument_parser.add_argument('--data_dir')

def add_to_coco_annotation(fullname, classes, annotation_file):
    global filename, height, width
    bb = ""
    in_file = open(fullname)
    tree = ET.parse(in_file)
    root = tree.getroot()
    for _i, _obj in enumerate(root.iter('annotation')):
        filename = _obj.find('filename').text
        height = int(_obj.find('size').find('height').text)
        width = int(_obj.find('size').find('width').text)
        
    for i, obj in enumerate(root.iter('object')):
        difficult = obj.find('difficult').text
        if int(difficult) == 1:
            continue
        cls = obj.find('name').text
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        box_width = int(xmlbox.find('xmax').text) - int(xmlbox.find('xmin').text)
        box_height = int(xmlbox.find('ymax').text) - int(xmlbox.find('ymin').text)
        b = ( (float(xmlbox.find('xmin').text) + box_width / 2.) / width,   # x_center
              (float(xmlbox.find('ymin').text) + box_height / 2.) / height, # y_center
              float(box_width) / width,                                     # width
              float(box_height) / height)                                   # height
        bb += (" " + str(cls_id) + ' ' + ' '.join([str(a) for a in b]))

    # we need this because I don't know overlapping or something like that
    list_file = open(annotation_file, 'a')
    file_string = '../dataset/'+ filename + bb + '\n'
    list_file.write(file_string)
    list_file.close()

if __name__=='__main__':
    
    args = argument_parser.parse_args()
    annotation_file = './annotation.txt'
    data_dir =  f'./{args.data_dir}'
    
    if os.path.exists(annotation_file): os.remove(annotation_file)
    
    path_to_xml = [os.path.join(data_dir, f) for f in os.listdir(data_dir)]
    classes = open('./classes.txt', 'r')
    all_classes = classes.read().split('\n')
    for filename in path_to_xml:
        if not filename.endswith('.xml'): continue
        add_to_coco_annotation(filename, all_classes, annotation_file)