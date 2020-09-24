import os
import pandas as pd
import cv2 as cv
from models.ct_image import CTImage
from voc.annotation import Annotation, Object
from voc.writer import VOCWriter

COLOR = (0,0,255)
path = './data'
output_path = './output'
output_folder = 'images'
xml_folder = 'xml'
database = 'LIDC-IDRI'
num_subset = 2
name = 'nodule'

def save_CT_images(ct_image, annotation):
    for s in range(ct_img.get_num_slice()):
        img = cv.normalize(ct_img.get_slice(s), None, alpha=0, beta=255, norm_type=cv.NORM_MINMAX)
        cv.imwrite(f'{output_path}/{output_folder}/{seriesuid}-{s}.jpeg', img)
        voc_writer.write(annotation, f'{output_path}/{xml_folder}/{seriesuid}-{s}.xml')
        
def annotate_image(filename, xy_min, xy_max):
    img = cv.imread(filename)
    cv.rectangle(img, xy_min, xy_max, COLOR)
    cv.imwrite(filename, img)
    

if __name__=='__main__':
    
    nodule_data = pd.read_csv('./data/annotations.csv')
    voc_writer = VOCWriter()
    
    if not os.path.exists(f'{output_path}/{output_folder}'): os.mkdir(f'{output_path}/{output_folder}')
    if not os.path.exists(f'{output_path}/{xml_folder}'): os.mkdir(f'{output_path}/{xml_folder}')
    
    for i in range(num_subset):
        print(f'Processing Subset {i}')
        input_files = list(filter(lambda filename: filename.endswith('.mhd'), os.listdir(f'./data/subset{i}')))

        for filename in input_files:
            print(f'Processsing File {filename}')
            seriesuid = filename[:-4]
            ct_img = CTImage(f'./data/subset{i}/{filename}')
            annotation = Annotation(output_folder, filename, output_path, database, ct_img.get_img_size())
            
            # Extract slices
            save_CT_images(ct_img, annotation)
            
            nodules = nodule_data[nodule_data['seriesuid'] == seriesuid]
            nodules_info = {}
            
            # Group nodules by slice
            for idx in nodules.index:
                coord_x, coord_y, coord_z = nodules.loc[idx, 'coordX'], nodules.loc[idx, 'coordY'], nodules.loc[idx, 'coordZ']
                diameter_mm = nodules.loc[idx, 'diameter_mm']
                dx, dy = (int(diameter_mm / ct_img.get_x_space()), int(diameter_mm / ct_img.get_y_space()) )
                x, y, z = ct_img.get_pxl_localtion((coord_x, coord_y, coord_z))
                
                if z not in nodules_info: nodules_info[z] = []
                nodules_info[z].append((x, y, dx, dy))
            
            if not nodules_info: continue
            
            print('Found nodules at : ', list(nodules_info.keys()))
            # Annotate image and Update VOC
            for slice_idx, nodules in nodules_info.items():
                img_file = f'{output_path}/{output_folder}/{seriesuid}-{slice_idx}.jpeg'
                for nodule in nodules:
                    x, y, dx, dy = nodule
                    annotate_image(img_file, (x - dx, y - dy), (x + dx, y + dy))
                    obj = Object(name, (x - dx, y - dy), (x + dx, y + dy))
                    annotation.add_object(obj)
                voc_writer.write(annotation, f'{output_path}/{xml_folder}/{seriesuid}-{slice_idx}.xml')
                
            
            