#!/usr/bin/python3


import os
import pickle
import re
import signal
import time
from shutil import rmtree

import nibabel as nib
import numpy as np
from miniutils.progress_bar import parallel_progbar
from utils.create_dataset_dict import create_dataset_dict
from utils.create_meta import create_meta
from utils.create_splits import create_splits
from utils.split_npz_into_slices import split_npz_into_slices
from utils.utils import termination_handler


def convert_to_np_worker(image, label, base_dir, output_file, debug):
    if debug:
        start = time.time()

    # Get image data
    img_path = os.path.join(base_dir, image)
    if os.path.exists(img_path):
        image = nib.load(img_path)
    else:
        img_path = img_path.replace('.nii.gz', '_0000.nii.gz')
        if os.path.exists(img_path):
            image = nib.load(img_path)
        else:
            raise ValueError('Could not find file: '.format(img_path))

    # Extract metadata
    meta_dict = {'affine': image.affine, 'shape': image.shape}
    image = image.get_fdata()

    # Normalize Image
    image = (image - image.min()) / (image.max() - image.min() + 1e-7)

    # Adjust shape of array
    # Old (x, y, amount of pictures)
    # New (amount of pictures, x, y)
    image = np.rollaxis(image, 2)

    # Get label
    if label:
        label = nib.load(os.path.join(base_dir, label)).get_fdata()
        label = np.rollaxis(label, 2)

        # only one label supported atm
        label[label > 1] = 1

        # Create stack with label
        if (image.shape == label.shape):
            stack = np.stack((image, label))
        else:
            error = "Error processing image '{}'. Image.shape {} does not match label.shape {}.".format(output_file,
                                                                                                        image.shape,
                                                                                                        label.shape)
            print(error)
            raise ValueError(error)
    else:
        stack = np.stack((image,))

    # DEBUG: Only select one image of the 3D Volume
    # if extract_only_one_slice:
    #     slide_to_extract = int(img.shape[0] / 2)
    #     img = img[slide_to_extract]
    #     label = label[slide_to_extract]
    #     img = img.reshape(1, img.shape[0], img.shape[1])
    #     label = label.reshape(1, label.shape[0], label.shape[1])
    #     img = ndimage.rotate(img, 90, reshape=False)
    #     label = ndimage.rotate(label, 90, reshape=False)

    np.savez_compressed(output_file, stack)

    with open("{}.pkl".format(output_file), 'wb') as meta_file:
        pickle.dump(meta_dict, meta_file)

    # Debugging .rotate(img, 90, reshape=False)
    # img = ndimage.rotate(stack[0, 57, :, :], 90, reshape=False)
    # label = ndimage.rotate(stack[1, 57, :, :], 90, reshape=False)
    #
    # plt.imshow(img[0], 'gray')
    # plt.show()
    #
    # plt.imshow([0], 'gray')
    # plt.show()

    if debug:
        filename_pattern = "\/([^\/]*)$"
        filename_prog = re.compile(filename_pattern)

        _, volume_name, _ = filename_prog.split(output_file)

        print('Finished nifti conversion for : {}, duration: {}s'.format(
            volume_name, int(time.time() - start)))


def convert_to_np(dataset_dir,
                  be_nice,
                  create_new_dataset_dict,
                  create_metadata,
                  split_npz_to_slices,
                  create_dataset_splits,
                  debug):
    # PATHs
    output_dir = os.path.join(dataset_dir, 'preprocessed')
    output_dir_pred = os.path.join(dataset_dir, 'predictionset_preprocessed')

    # Validate inputs and ensure output dir is empty (prevent mix with old files)
    rmtree(output_dir, ignore_errors=True)
    rmtree(output_dir_pred, ignore_errors=True)
    os.makedirs(output_dir)
    os.makedirs(output_dir_pred)

    # Only use free resources on the machine (don't block the machine)
    if be_nice:
        os.nice(18)

    # Load dataset information (location of training data, labels, test data, ...)
    if create_new_dataset_dict:
        dataset_dict = create_dataset_dict(dataset_dir)
        print("Dataset dict created, continue with np-conversion")
    else:
        with open(os.path.join(dataset_dir, "dataset.pkl"), 'rb') as f:
            dataset_dict = pickle.load(f)

    # Prepare data for parallel processing
    params = []
    filename_pattern = "^(.+\/)*(.+)\.(.+)\.(.+)$"
    filename_prog = re.compile(filename_pattern)
    for i in range(len(dataset_dict['training'])):
        # Select image and corresponding label
        img = dataset_dict['training'][i]['image'].replace('./', '')
        lab = dataset_dict['training'][i]['label'].replace('./', '')
        _, image_path, image_filename, _, _, _ = filename_prog.split(img)
        output_file_path = os.path.join(output_dir, image_filename)

        params += [(img, lab, dataset_dir, output_file_path, debug)]

    for i in range(len(dataset_dict.get('test', ""))):
        pred = dataset_dict['test'][i].replace('./', '')
        _, image_path, image_filename, _, _, _ = filename_prog.split(pred)
        output_file_path = os.path.join(output_dir_pred, image_filename)

        params += [(pred, None, dataset_dir, output_file_path, debug)]

    # Convert files in parallel
    # convert_to_np_worker(params[0][0], params[0][1], params[0][2], params[0][3], params[0][4])
    parallel_progbar(convert_to_np_worker, params, starmap=True)

    # Execute next steps
    if create_metadata:
        create_meta(dataset_dir, debug=debug)

    if split_npz_to_slices:
        split_npz_into_slices(dataset_dir, debug=debug)

    if create_dataset_splits:
        create_splits(dataset_dir)


if __name__ == "__main__":
    # Expects a dataset.pkl containing the paths to the training-data and the labels
    # e.g for labeled data:
    #     dataset['training'] = [{'image': './imagesTr/kidney59.nii.gz', 'label': './labelsTr/kidney59.nii.gz'}]

    # Read input parameters
    dataset_dir = os.environ.get('DATASET_DIR', '/data/dataset')
    be_nice = os.environ.get('BE_NICE', True)
    create_new_dataset_dict = os.environ.get('CREATE_DATASET_DICT', True)
    create_metadata = os.environ.get('CREATE_METADATA', True)
    split_npz_to_slices = os.environ.get('SPLIT_NPZ_INTO_SLICES', True)
    create_dataset_splits = os.environ.get('CREATE_DATASET_SPLITS', True)
    debug = os.environ.get('DEBUG', False)

    # Handle termination signal peacefully
    signal.signal(signal.SIGINT, termination_handler)

    print("Welcome to the data pre-processing tool. It will prepare your nifti-files for training.")

    # Start nifti preprocessing
    if dataset_dir == "all":
        # For manual / debug run

        datasets = [
            "/data/datasets/Task02_Heart",
            "/data/datasets/Task03_Liver",
            "/data/datasets/Task04_Hippocampus",
            "/data/datasets/Task05_Prostate",
            "/data/datasets/Task06_Lung",
            "/data/datasets/Task07_Pancreas",
            "/data/datasets/Task09_Spleen",
            "/data/datasets/Task31_KidneySegmentation"]

        for d in datasets:
            convert_to_np(d,
                          be_nice,
                          create_new_dataset_dict,
                          create_metadata,
                          split_npz_to_slices,
                          create_dataset_splits,
                          debug)
    else:
        # Check input
        if not dataset_dir or not os.path.exists(dataset_dir):
            error = "Dataset directory '{}' is not valid. Please try again.".format(dataset_dir)
            raise ValueError(error)

        convert_to_np(dataset_dir,
                      be_nice,
                      create_new_dataset_dict,
                      create_metadata,
                      split_npz_to_slices,
                      create_dataset_splits,
                      debug)
