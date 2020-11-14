import os
import argparse

from shutil import copyfile

annotation_folder = 'Annotations'
img_folder = 'JPEGImages'
imgset_folder = 'ImageSets'

argument_parser = argparse.ArgumentParser()
argument_parser.add_argument('--img_src')
argument_parser.add_argument('--xml_src')
argument_parser.add_argument('--img_set')
argument_parser.add_argument('--output')

args = argument_parser.parse_args()
img_src = args.img_src
xml_src = args.xml_src
img_set = args.img_set
output_folder = args.output

if __name__=='__main__':
    if not os.path.exists(f'{output_folder}'): os.mkdir(f'{output_folder}')
    
    img_files = [f for f in os.listdir(img_src) if f.endswith(('jpg', 'jpeg', 'png'))]
    xml_files = [f for f in os.listdir(xml_src) if f.endswith('xml')]

    if not os.path.exists(f'{output_folder}/{annotation_folder}'): os.mkdir(f'{output_folder}/{annotation_folder}')
    if not os.path.exists(f'{output_folder}/{img_folder}'): os.mkdir(f'{output_folder}/{img_folder}')
    if not os.path.exists(f'{output_folder}/{imgset_folder}'): os.mkdir(f'{output_folder}/{imgset_folder}')
    
    for f in img_files: copyfile(f'{img_src}/{f}', f'{output_folder}/{img_folder}/{f}')
    for f in xml_files: copyfile(f'{xml_src}/{f}', f'{output_folder}/{annotation_folder}/{f}')
    
    f = open(f'{output_folder}/{imgset_folder}/{img_set}.txt', 'w')
    for img in img_files: f.write(f'{img}\n')