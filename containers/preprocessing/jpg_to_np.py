#!/usr/bin/python3

import os
import time

import numpy as np
import scipy.ndimage
from joblib import Parallel, delayed
from preprocessing.common.preprocessing.create_meta import create_meta
from preprocessing.common.preprocessing.create_splits import create_splits
from skimage.transform import rescale

dataset_dir = "/data/datasets/carvana"

base_dir_train = os.path.join(dataset_dir, 'train')
image_dir = os.path.join(dataset_dir, base_dir_train)

label_dir = os.path.join(dataset_dir, 'train_masks')
output_dir = os.path.join(dataset_dir, 'preprocessed')

os.makedirs(output_dir, exist_ok=True)


def convert_jpg(filename):
    start = time.time()
    if os.path.isfile(os.path.join(output_dir, filename) + '.npz'):
        print('already exists...continue...')
        return

    # Get and rescale images
    image = scipy.ndimage.imread(os.path.join(image_dir, filename), flatten=True).astype(np.float32)
    image = (image - image.min()) / (image.max() - image.min() + 1e-7)
    image = rescale(image, 0.1, anti_aliasing=False)
    image_reshaped = image.reshape(1, image.shape[0], image.shape[1])

    # Get and rescale labels
    label = scipy.ndimage.imread(os.path.join(label_dir, filename.replace(".jpg", "_mask.gif")), flatten=True).astype(
        np.float32)
    label = rescale(label / 255.0, 0.1, anti_aliasing=False)
    label_reshaped = label.reshape(1, image.shape[0], image.shape[1])

    result = np.stack((image_reshaped, label_reshaped))

    # if False:
    #     plt.imshow(image_reshaped[0], 'gray')
    #     plt.show()
    #     plt.imshow(label_reshaped[0], 'gray')
    #     plt.show()

    # Create the np file
    # np.save(os.path.join(output_dir, filename.replace(".jpg", "") + '.npy'), result)
    np.savez_compressed(os.path.join(output_dir, filename.replace(".jpg", "")), result)
    print('Finished: {}, duration: {}s'.format(
        os.path.join(filename), int(time.time() - start)))


if __name__ == "__main__":
    # convert_jpg(1)
    files = os.listdir(base_dir_train)

    Parallel(n_jobs=8)(delayed(convert_jpg)(filename)
                       for filename in files)

    create_splits(dataset_dir)
    create_meta(dataset_dir)

# Quick and dirty fix for file-name issues
# for file in os.listdir(output_dir):
#     print("Renaming: ", file)
#     pre, ext = os.path.splitext(os.path.join(output_dir, file))
#     if ext == ".npz":
#         os.rename(os.path.join(output_dir, file), os.path.join(output_dir, pre))
