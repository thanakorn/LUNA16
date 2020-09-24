import numpy as np
from utilites.utilities import load_itk

class CTImage:
    def __init__(self, filename):
        ct_image, origin, space = load_itk(filename)
        self.ct_image = ct_image
        self.origin = origin
        self.space = space
    
    def get_num_slice(self):
        return self.ct_image.shape[0]
    
    def get_img_size(self):
        return self.ct_image.shape[1], self.ct_image.shape[2], 1
    
    def get_x_space(self):
        return self.space[0]
    
    def get_y_space(self):
        return self.space[1]
    
    def get_pxl_localtion(self, xyz_coord):
        xyz_coord = np.array(xyz_coord)
        # pxl_pos = np.rint((xyz_coord / self.space) - self.origin)
        pxl_pos = np.rint((xyz_coord - self.origin) / self.space)
        return int(pxl_pos[0]), int(pxl_pos[1]), int(pxl_pos[2])
    
    def get_slice(self, slice_idx):
        return self.ct_image[slice_idx,:,:]
        