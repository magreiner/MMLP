import re
import sys

import numpy as np


# from SimpleITK import SimpleITK


# def load_dcm_image(dcm_dir):
#     reader = SimpleITK.ImageSeriesReader()
#     filenames_dicom = reader.GetGDCMSeriesFileNames(dcm_dir)
#     reader.SetFileNames(filenames_dicom)
#
#     image_dicom = reader.Execute()
#     image = SimpleITK.GetArrayFromImage(image_dicom)
#
#     spacing = image_dicom.GetSpacing()
#
#     return image, spacing
#
#
# def load_label(label_dir):
#     label_file = label_dir + '_mask_JW.nrrd'
#
#     # images are 512 by 512 pixels each
#     image_nrrd = SimpleITK.ReadImage(label_file)
#     label = SimpleITK.GetArrayFromImage(image_nrrd)
#
#     return label


def get_volume_slices(image_list, volume_numbers_list=None, volume_name_regexp=None, delimiter="_"):
    # Initialize parameters
    if volume_numbers_list is None:
        volume_numbers_list = [1, 2]

    if volume_name_regexp is None:
        # Default format, extracts dataset name
        # matches for e.g.: 'kidney2_slice_172.npz' (extracts "kidney")
        volume_name_regexp = "^([a-z-_.0]{1,})"

    filename_prog = re.compile(volume_name_regexp)
    files = []
    for file in image_list:
        for volume_numbers in volume_numbers_list:
            _, file_name, _ = filename_prog.split(file)
            if file.startswith("{}{}{}".format(file_name, volume_numbers, delimiter)):
                files += [file]

    return np.asarray(files)


def termination_handler(sig, frame):
    print('Why are you doing this to me?! Terminating now ... :(')
    sys.exit(0)
