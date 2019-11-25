#!/usr/bin/python3

import os
import pickle

import numpy as np
from miniutils.progress_bar import parallel_progbar

try:
    from .utils import get_volume_slices
except:
    from utils import get_volume_slices


def create_splits_worker(trainset_size, valset_size, testset_size, image_list):
    # Get new seed to prevent the creation of identical split_sets
    np.random.seed()

    # Split dataset into trainingsets
    trainset = np.random.choice(image_list, trainset_size, replace=False)
    for image in trainset:
        image_list.remove(image)

    valset = np.random.choice(image_list, valset_size, replace=False)
    for image in valset:
        image_list.remove(image)

    testset = np.random.choice(image_list, testset_size, replace=False)
    for image in testset:
        image_list.remove(image)

    split_dict = dict()
    split_dict['train'] = trainset
    split_dict['val'] = valset
    split_dict['test'] = testset

    # print(split_dict['train'])

    return split_dict


def create_splits(dataset_dir,
                  prediction_volume_numbers=None,
                  image_dir=None,
                  img_file_suffix=".npz",
                  num_splitsets=5):
    print("Welcome to the dataset split tool. It will split your data into training, validation, testing sets.")

    # Dataset with images to create the splits for
    if not image_dir:
        image_dir = os.path.join(dataset_dir, 'preprocessed')

    # Keep following volume numbers for prediction
    # only used if no separate, unlabeled image dir is available
    if prediction_volume_numbers is None:
        prediction_volume_numbers = [1]

    # Extract all available image files
    image_files = []
    for file in os.listdir(image_dir):
        if file.endswith(img_file_suffix):
            image_files += [file]

    dataset_size = len(image_files)
    dataset_size_remaining = dataset_size

    # Get prediction slices
    # check if separate testset is available
    unlabeled_testset_dir = os.path.join(dataset_dir, "predictionset_preprocessed")
    prediction_set = []
    if os.path.exists(unlabeled_testset_dir):
        print("Separate unlabeled image_dir found.")
        for file in os.listdir(unlabeled_testset_dir):
            if file.endswith(img_file_suffix):
                prediction_set += [file]

        prediction_set = np.asarray(prediction_set)
    else:
        prediction_set = get_volume_slices(image_files, volume_numbers_list=prediction_volume_numbers)

        # Remove prediction volume from dataset
        for image in prediction_set:
            image_files.remove(image)

        dataset_size_remaining -= len(prediction_set)

    trainset_size = int(dataset_size_remaining * 0.7)
    valset_size = int((dataset_size_remaining - trainset_size) / 2)
    testset_size = int((dataset_size_remaining - trainset_size - valset_size))

    # Manual dataset size definition:
    # trainset_size = 50
    # valset_size = 10
    # testset_size = 10

    print("Found {} labeled slices for learning".format(dataset_size))
    print("Added {} image-volumes to training set".format(trainset_size))
    print("Added {} image-volumes to validation set".format(valset_size))
    print("Added {} image-volumes to test set".format(testset_size))
    print("Added {} image-volumes to prediction set".format(len(prediction_set)))
    print()
    print("Creating dataset splits ...")
    splits = [(trainset_size, valset_size, testset_size, image_files.copy())] * num_splitsets

    # Extract the image shapes in parallel)
    splits_dict = parallel_progbar(create_splits_worker, splits, starmap=True)
    for i in range(len(splits_dict)):
        splits_dict[i]['prediction'] = prediction_set

    with open(os.path.join(dataset_dir, 'splits.pkl'), 'wb') as f:
        pickle.dump(splits_dict, f)

    print("Splitfile created")


if __name__ == "__main__":
    # create_splits("/data/datasets/Task07_Pancreas")
    create_splits("/data/datasets/Task06_Lung")
    # create_splits("/data/datasets/Task03_Liver")
    # create_splits("/data/datasets/carvana")
    # create_splits("/data/datasets/cifar_mnist")
    # create_splits("/data/datasets/Task31_KidneySegmentation")
