#!/usr/bin/python3


import os
import pickle
import re
import signal
import time
from shutil import copy, rmtree

import nibabel as nib
import numpy as np
from miniutils.progress_bar import parallel_progbar

from utils import termination_handler


def combine_splits_worker(volume, existing_splits, meta_data, source_dir, output_dir, debug):
    # Keep track of runtime
    if debug:
        start = time.time()

    # Array for the full 3D image stack
    volume_image = np.zeros(meta_data['shape'])

    # add segmented splits
    for img_path, split_id in existing_splits:
        img_path = os.path.join(source_dir, img_path)

        volume_image[:, :, int(split_id)] = nib.load(img_path).get_fdata()[:, :, 0]

    affine = meta_data['affine']

    # Convert to nifty and store it
    nifty = nib.Nifti1Image(volume_image, affine)
    nifty.to_filename(os.path.join(output_dir, '{}_seg.nii.gz').format(volume))

    if debug:
        print('Volume finished: {}, duration: {}s'.format(
            '{}_seg.nii.gz'.format(volume),
            int(time.time() - start)))


def combine_splits(dataset_dir,
                   be_nice=True,
                   debug=False):
    # Paths
    source_dir = os.path.join(dataset_dir, 'predicted_segmentations_slices')
    output_dir = os.path.join(dataset_dir, 'predicted_segmentations')

    # Only use free resources on the machine (don't block the machine)
    if be_nice:
        os.nice(18)

    # Validate inputs and ensure output dir is empty (prevent mix with old files)
    rmtree(output_dir, ignore_errors=True)
    os.makedirs(output_dir)

    # Get all 3D volumes
    volumes = {}
    volume_metadata = {}
    filename_pattern = "^(.*)(_slice_)([0-9]*)"
    filename_prog = re.compile(filename_pattern)
    for v in os.listdir(source_dir):
        if v.endswith("nii.gz"):
            _, volume_name, _, slice_id, _ = filename_prog.split(v)

            if volume_name in volumes:
                volumes[volume_name] += [(v, slice_id)]
            else:
                # Copy the meta-data file for each volume to the new output dir
                meta_file = os.path.join(source_dir, "{}.pkl".format(volume_name))
                copy(meta_file, output_dir)

                with open(meta_file, 'rb') as f:
                    meta_data = pickle.load(f)

                # Create new volume entry
                volumes[volume_name] = [(v, slice_id)]
                volume_metadata[volume_name] = meta_data

    # Convert files in parallel
    params = []
    for volume_name in volumes.keys():
        params += [(volume_name, volumes[volume_name], volume_metadata[volume_name], source_dir, output_dir, debug)]

    parallel_progbar(combine_splits_worker, params, starmap=True)


if __name__ == "__main__":
    # Expects the following sub-dirs of base-dir:
    # Directory to read the nifti-slices from: 'predicted_segmentations_slices'
    # Directory to store the volumes (content will be deleted): 'predicted_segmentations'

    # Read input parameters
    dataset_dir = os.environ.get('DATASET_DIR', '/data/dataset')
    be_nice = os.environ.get('BE_NICE', True)
    debug = os.environ.get('DEBUG', False)

    # base_dir = "/data/datasets/Task03_Liver"
    # base_dir = "/data/datasets/Task06_Lung"
    # base_dir = "/data/datasets/Task07_Pancreas"
    # base_dir = "/data/datasets/Task31_KidneySegmentation"

    # Handle termination signal peacefully
    signal.signal(signal.SIGINT, termination_handler)

    # Start combination of nifti slices
    print("Welcome to the combination tool for nifti slices. Starting ...")
    combine_splits(dataset_dir, be_nice, debug)
