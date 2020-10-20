import os
import pandas as pd
import cv2 as cv
import concurrent.futures
import argparse
from tqdm import tqdm
from models.ct_image import CTImage
from writer.annotation import Annotation, Object
from writer.coco_writer import COCOWriter
from concurrent.futures import ThreadPoolExecutor

image_folder = 'images'
image_list = 'images.txt'
label_folder = 'labels'
database = 'LIDC-IDRI'
name = 'nodule'
nodules_log = './nodules_log.csv'
default_size = 416

argument_parser = argparse.ArgumentParser()
argument_parser.add_argument('--classes')
argument_parser.add_argument('--data')
argument_parser.add_argument('--output')
argument_parser.add_argument('--num_processes')
argument_parser.add_argument('--resize')

args = argument_parser.parse_args()
data_path = args.data
output_path = args.output
resize = args.resize if args.resize else default_size
num_processes = int(args.num_processes)

classes = open(args.classes, 'r').read().split('\n')

def save_CT_images(ct_filename):
    file = open(f'{args.output}/images.txt', 'a')
    seriesuid = ct_filename.split('/')[-1][:-4]
    ct_img = CTImage(ct_filename)
    for s in range(ct_img.get_num_slice()):
        img_filename = f'{seriesuid}-{s}.jpeg'
        full_filename = f'{output_path}/{image_folder}/{img_filename}'
        img = cv.normalize(ct_img.get_slice(s), None, alpha=0, beta=255, norm_type=cv.NORM_MINMAX)
        img = cv.resize(img, (resize, resize), interpolation = cv.INTER_CUBIC)
        cv.imwrite(full_filename, img)
        file.write(os.path.abspath(args.output) + '/' + image_folder + '/' + img_filename + '\n')

def annotate_image(filename, xy_min, xy_max):
    img = cv.imread(filename)
    cv.rectangle(img, xy_min, xy_max, (0,0,255))
    cv.imwrite(filename, img)
    
def process_CT_image(filename, nodule_data, log=None):
    writer = COCOWriter()
    seriesuid = filename.split('/')[-1][:-4]
    ct_img = CTImage(filename)
    nodules = {}
    
    # Group nodules by slice
    for idx in nodule_data.index:
        coord_x, coord_y, coord_z = nodule_data.loc[idx, 'coordX'], nodule_data.loc[idx, 'coordY'], nodule_data.loc[idx, 'coordZ']
        diameter_mm = nodule_data.loc[idx, 'diameter_mm']
        dx, dy = (int(diameter_mm / ct_img.get_x_space()), int(diameter_mm / ct_img.get_y_space()) )
        x, y, z = ct_img.get_pxl_localtion((coord_x, coord_y, coord_z))
        
        if z not in nodules: nodules[z] = []
        nodules[z].append((x, y, dx, dy))

    # Annotate image and create label file
    for slice_idx, nodules in nodules.items():
        img_filename = f'{seriesuid}-{slice_idx}.jpeg'
        label_filename = f'{seriesuid}-{slice_idx}.txt'
        full_filename = f'{output_path}/{image_folder}/{seriesuid}-{slice_idx}.jpeg'
        annotation = Annotation(image_folder, img_filename, full_filename, database, ct_img.get_img_size())
        for nodule in nodules:
            x, y, dx, dy = nodule
            # annotate_image(full_filename, (x - dx, y - dy), (x + dx, y + dy))
            obj = Object(name, (x - dx, y - dy), (x + dx, y + dy))
            annotation.add_object(obj)
        writer.write(annotation, f'{output_path}/{label_folder}/{label_filename}', classes)
        if log : log.write(f'{seriesuid},{slice_idx}\n')

if __name__=='__main__':

    thread_pool = ThreadPoolExecutor(num_processes)
    annotation = pd.read_csv(f'{data_path}/annotations.csv')
    nodules_log = open(nodules_log, 'w')
    nodules_log.write('seriesuid,slice\n')
    
    if not os.path.exists(f'{output_path}'): os.mkdir(f'{output_path}')
    if not os.path.exists(f'{output_path}/{image_folder}'): os.mkdir(f'{output_path}/{image_folder}')
    if not os.path.exists(f'{output_path}/{label_folder}'): os.mkdir(f'{output_path}/{label_folder}')

    for folder in os.walk(data_path).__next__()[1]:
        print(f'Processing folder {folder}')
        
        input_files = list(filter(lambda filename: filename.endswith('.mhd'), os.listdir(f'{data_path}/{folder}')))
        full_input_files = [f'{data_path}/{folder}/{file}' for file in input_files]
        
        # Save all slices
        with tqdm(total=len(full_input_files), desc=f'Extract images') as pbar:
            for _ in thread_pool.map(save_CT_images, full_input_files): pbar.update()
            
        # Annotate nodules
        for file in tqdm(full_input_files, desc=f'Annoate images'):
            nodule_data = annotation[annotation['seriesuid'] == file.split('/')[-1][:-4]]
            if not nodule_data.empty: process_CT_image(file, nodule_data, nodules_log)
