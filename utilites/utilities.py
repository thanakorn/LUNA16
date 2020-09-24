import SimpleITK as sitk
import numpy as np

# Reads the image using SimpleITK
def load_itk(filename):
    itkimage = sitk.ReadImage(filename)
    ct_scan = sitk.GetArrayFromImage(itkimage)
    # Read the origin of the ct_scan, will be used to convert the coordinates from world to voxel and vice versa.
    origin = np.array(itkimage.GetOrigin())
    # Read the spacing along each dimension
    spacing = np.array(itkimage.GetSpacing())

    return ct_scan, origin, spacing