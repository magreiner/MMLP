#!/usr/bin/python3
import os
import time

import matplotlib as plt
import numpy as np
from cifar_mnist_generator import *
from joblib import Parallel, delayed
from skimage.color import rgb2gray

# from preprocessing.create_splits import create_splits
# Install: joblib python-mnist

base_dir = "/data/datasets/cifar_mnist/"
output_dir = os.path.join(base_dir, 'preprocessed')
dg = Datagen('/data/datasets/mnist', '/data/datasets/cifar')
num_pictures_start = 70
num_pictures_end = 10000

DEBUG_enable_write = True

os.makedirs(output_dir, exist_ok=True)


def toGrayNormalize(image):
    image += abs(image.min())
    image /= image.max()
    image = rgb2gray(image)

    return image


def save_image(image, filename):
    fig = plt.figure()
    fig.set_size_inches(image.shape)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.imshow(image, cmap='gray')

    if DEBUG_enable_write:
        plt.savefig(filename)
    # print()


def create_picture(picture_number):
    start = time.time()
    pictures, segmentations = dg.sample(1)
    processed_image = toGrayNormalize(pictures[0])
    # save_image(processed_image, os.path.join(output_dir, '{}_picture.png'.format(picture_number)))
    # save_image(segmentations[0], os.path.join(output_dir, '{}_segmmentation.png'.format(picture_number)))

    processed_image = processed_image.reshape(1, processed_image.shape[0], processed_image.shape[1])
    segmentations = segmentations[0].reshape(1, segmentations[0].shape[0], segmentations[0].shape[1])

    npy = np.stack((processed_image, segmentations))

    if DEBUG_enable_write:
        # np.save(os.path.join(output_dir, '{}.npy'.format(picture_number)), npy)
        np.savez_compressed(os.path.join(output_dir, '{}'.format(picture_number)), npy)
    print('Finished: Picture_{}, duration: {}s'.format(
        picture_number, int(time.time() - start)))


if __name__ == "__main__":
    # create_picture(1)
    Parallel(n_jobs=8)(delayed(create_picture)(i) for i in range(num_pictures_start, num_pictures_end))

    # create_splits(base_dir)
