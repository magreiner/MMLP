#!/usr/bin/python3

import os
import pickle
import re
import time

import numpy as np
from miniutils.progress_bar import parallel_progbar


def extract_shape_from_image(npz_file, debug):
    if debug:
        start = time.time()

    numpy_array = np.load(npz_file, mmap_mode="r")

    # Extract file
    if len(numpy_array.files) != 1:
        raise ValueError("Only one file per npz is supported. Please fix: {}".format(npz_file))

    # Extract volume-name
    filename_pattern = "\/([^\/]*)$"
    filename_prog = re.compile(filename_pattern)
    _, volume_name, _ = filename_prog.split(npz_file)

    if debug:
        print('Finished metadata collection for {}, duration: {}s'.format(
            volume_name, int(time.time() - start)))

    return volume_name, numpy_array[numpy_array.files[0]].shape


# Extract needed image file metadata
def create_meta_dirs(image_dir, img_file_suffix, be_nice, debug):
    # Only use free resources on the machine (don't block the machine)
    if be_nice:
        os.nice(18)

    print("Extracting meta-data from images in {}".format(image_dir))

    # Create a list of images to process
    image_files = dict()
    files = []
    for f in os.listdir(image_dir):
        if f.endswith(img_file_suffix):
            files += [(os.path.join(image_dir, f), debug)]

    # Extract the image shapes in parallel
    image_shapes = parallel_progbar(extract_shape_from_image, files, starmap=True)

    # Store the results in format:
    # image_files[file] = shape
    for img in image_shapes:
        npz_file, npz_file_shape = img
        image_files[npz_file] = npz_file_shape

    dataset_size = len(image_files.keys())

    print("Found {} images for meta collection".format(dataset_size))

    with open(os.path.join(image_dir, 'image_meta.pkl'), 'wb') as f:
        pickle.dump(image_files, f)


def create_meta(dataset_dir,
                img_file_suffix=".npz",
                be_nice=True,
                debug=False):
    print("Welcome to the meta-data tool. It will extract important meta-data for training now.")

    # Locate the images
    image_dir = os.path.join(dataset_dir, 'preprocessed')
    create_meta_dirs(image_dir, img_file_suffix, be_nice, debug)

    # Check separate unlabeled image dir
    testset_dir = os.path.join(dataset_dir, "predictionset_preprocessed")
    if os.path.exists(testset_dir):
        create_meta_dirs(testset_dir, img_file_suffix, be_nice, debug)


if __name__ == "__main__":
    # create_meta("/data/datasets/Task07_Pancreas")
    create_meta("/data/datasets/Task06_Lung")
    # create_meta("/data/datasets/Task03_Liver")
    # create_meta("/data/datasets/Task31_KidneySegmentation")
