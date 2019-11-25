import os
import time

import numpy as np

base_dir = "/data/datasets/fake_512x512"
output_dir = os.path.join(base_dir, 'preprocessed')
number_of_files = 200

# Validate inputs
os.makedirs(output_dir, exist_ok=True)


def generate(i):
    output_file = os.path.join(output_dir, 'np_stack_{}.npz'.format(i))
    start = time.time()

    img = np.random.rand(2, 512, 512)
    label = np.zeros((2, 512, 512))

    stack = np.stack((img, label))

    # np.savez_compressed(output_file, stack)

    print('Finished: {}, duration: {}s'.format(
        output_file, int(time.time() - start)))

    # plt.imshow(img[0], 'gray')
    # plt.show()
    #
    # plt.imshow(label[0], 'gray')
    # plt.show()


if __name__ == "__main__":
    generate(12)
    # Parallel(n_jobs=8)(delayed(generate)(i)
    #                    for i in range(number_of_files))
    # create_splits(base_dir)
