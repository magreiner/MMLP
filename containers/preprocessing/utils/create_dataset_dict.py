import os
import pickle
import re


def get_files(path, directory, accepted_endings):
    filename_pattern = "\.([^\.]{1,})$"
    filename_prog = re.compile(filename_pattern)
    accepted_files = []
    for file in os.listdir(os.path.join(path, directory)):
        volume_name, ending, _ = filename_prog.split(file)

        if ending in accepted_endings:
            accepted_files += [os.path.join(directory, file)]

    return accepted_files


def get_annotated_files(dataset_dir, annotated_images_dir, annotations_dir, accepted_endings):
    images = get_files(dataset_dir, annotated_images_dir, accepted_endings)

    potential_labels = get_files(dataset_dir, annotations_dir, accepted_endings)

    filename_pattern = "\/([^\/]{1,})\.([^\.]{1,})$"
    filename_prog = re.compile(filename_pattern)
    potential_labels_dict = {}
    for x in potential_labels:
        _, volume_name, ending, _ = filename_prog.split(x)
        potential_labels_dict.setdefault(volume_name, x)

    dataset = []
    for file in images:
        _, volume_name, ending, _ = filename_prog.split(file)

        # Some files are renamed,
        if '_0000' in volume_name:
            # print('Info: Ignored _0000 from file {}'.format(volume_name))
            volume_name = volume_name.replace('_0000', '')

        if potential_labels_dict.get(volume_name, False):
            new_entry = {'image': file,
                         'label': potential_labels_dict[volume_name]}
            dataset += [new_entry]
        else:
            error = "No label found for image {}. Expected a file like {}" \
                    " (ending is not checked but must be present)".format(file,
                                                                          os.path.join(annotations_dir, volume_name))
            raise ValueError(error)

    return dataset


def create_dataset_dict(dataset_dir):
    print("Welcome to the dataset analyse tool. It will make a catalog of your training and prediction data")
    print("Analysing directory {}".format(dataset_dir))

    # Annotated Data
    # Training images will be split into training, validataion and test set later
    # Labels and training data have to be in the same order and have the same names:
    # e.g. image_1.dcm and image_1.nii.gz
    annotated_images_dir = "imagesTr"
    annotations_dir = "labelsTr"

    # Unannotated Data
    test_images_dir = "imagesTs"

    # Which image/label-formats should be added for training?
    # only checked till the first dot, from the right side
    # e.g. .nii.gz can only be checked as gz
    accepted_file_endings = ["dcm", "gz", "npy", "npz"]

    dataset_dict = {'training': get_annotated_files(dataset_dir,
                                                    annotated_images_dir,
                                                    annotations_dir,
                                                    accepted_file_endings),
                    'test': get_files(dataset_dir,
                                      test_images_dir,
                                      accepted_file_endings)}

    # Validate dataset
    train_size = len(dataset_dict['training'])
    print("Found {} images with annotations".format(train_size))
    if train_size < 1:
        raise ValueError("Could not find any training images. Please check your paths.")

    pred_size = len(dataset_dict['test'])
    print("Found {} images without annotations".format(pred_size))
    if pred_size < 1:
        print("Info: No data for prediction found.")

    # Store dataset information (location of training data, labels, test data, ...)
    with open(os.path.join(dataset_dir, 'dataset.pkl'), 'wb') as f:
        pickle.dump(dataset_dict, f)

    return dataset_dict


if __name__ == "__main__":
    datasets = ["/data/datasets/Task07_Pancreas",
                "/data/datasets/Task06_Lung",
                "/data/datasets/Task03_Liver",
                "/data/datasets/Task31_KidneySegmentation"]

    for d in datasets:
        create_dataset_dict(d)
