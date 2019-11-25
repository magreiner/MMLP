#!/usr/bin/python3

import os
import pickle
import time
from shutil import copyfile, rmtree

import numpy as np
from miniutils.progress_bar import parallel_progbar


def split_npz_worker(image_dir, volume_name, output_dir, debug):
    if debug:
        start = time.time()

    volume_path = os.path.join(image_dir, volume_name)
    volume_name = volume_name.replace(".npz", "")

    volume = np.load(volume_path, mmap_mode="r")
    if len(volume.files) != 1:
        raise ValueError("Only one file per npz is supported. Please fix: {}".format(volume_path))
    volume = volume[volume.files[0]]

    # if image contains more then one slice, split it
    empty_slices_counter = 0
    empty_label_ids = []
    for i in range(volume.shape[1]):
        curr_slide_stack = volume[:, i, :, :]

        curr_slide_stack = curr_slide_stack.reshape(volume.shape[0], 1, volume.shape[2], volume.shape[3])

        # Mark images with nothing marked in the label
        # (To be able to learn on slices with interesting content)
        if curr_slide_stack.shape[0] > 1 > curr_slide_stack[1].max():
            empty_label_ids += [i]
            empty_slices_counter += 1

        output_file = os.path.join(output_dir, "{}_slice_{}".format(volume_name, i))
        np.savez_compressed(output_file, curr_slide_stack)

    # Copy the meta-data file for each volume to the new output dir
    copyfile(volume_path.replace(".npz", ".pkl"), os.path.join(output_dir, "{}.pkl".format(volume_name)))

    # Print some output to keep the user busy and interested
    if debug:
        if empty_slices_counter:
            print('Split finished: {} (Skipped {} slices: label zero, nothing to learn), duration: {}s'.format(
                volume_name,
                empty_slices_counter,
                int(time.time() - start)))
        else:
            print('Split finished for {}, duration: {}s'.format(
                volume_name,
                int(time.time() - start)))

    return volume_name, empty_label_ids


def split_npz_into_slices_dirs(be_nice, image_dir, output_dir, debug):
    # Validate inputs and ensure output dir is empty (prevent mix with old files)
    rmtree(output_dir, ignore_errors=True)
    os.makedirs(output_dir)

    print("Splitting npz files in {}".format(image_dir))

    # Copy the meta-data file from the dataset to the new output dir
    copyfile(os.path.join(image_dir, "image_meta.pkl"), os.path.join(output_dir, "image_meta.pkl"))

    # Only use free resources on the machine (don't block the machine)
    if be_nice:
        os.nice(18)

    # Create a list of images to process
    images = []
    for image in os.listdir(image_dir):
        if image.endswith(".npz"):
            images += [(image_dir, image, output_dir, debug)]

    # Split the image slices in parallel
    empty_slices = parallel_progbar(split_npz_worker, images, starmap=True)

    empty_slices_dict = {}
    for volume_name, slice_ids in empty_slices:
        empty_slices_dict[volume_name] = slice_ids

    with open("{}".format(os.path.join(image_dir, "empty_labels.pkl")), 'wb') as empty_slices_file:
        pickle.dump(empty_slices_dict, empty_slices_file)


def split_npz_into_slices(dataset_dir, be_nice=True, debug=False):
    print("Welcome to the npz-split tool. It will split npz volumes into single npz-slices.")

    image_dir = os.path.join(dataset_dir, 'preprocessed')
    output_dir = os.path.join(dataset_dir, 'preprocessed_slices')

    split_npz_into_slices_dirs(be_nice, image_dir, output_dir, debug)

    # Check separate unlabeled image dir
    image_dir = os.path.join(dataset_dir, 'predictionset_preprocessed')

    if os.path.exists(image_dir):
        output_dir = os.path.join(dataset_dir, 'predictionset_preprocessed_slices')

        split_npz_into_slices_dirs(be_nice, image_dir, output_dir, debug)


if __name__ == "__main__":
    # split_npz_into_slices("/data/datasets/Task07_Pancreas")
    split_npz_into_slices("/data/datasets/Task06_Lung")
    # split_npz_into_slices("/data/datasets/Task03_Liver")
    # split_npz_into_slices("/data/datasets/carvana")
    # split_npz_into_slices("/data/datasets/cifar_mnist")
    # split_npz_into_slices("/data/datasets/Task31_KidneySegmentation")
