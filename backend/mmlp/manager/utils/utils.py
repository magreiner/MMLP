import json
from datetime import datetime
from pathlib import Path
from typing import List, TypeVar
from uuid import UUID, uuid4

from toolz import curry, merge

from mmlp.utils import excepting_pipe, list_files, load_json

GenericObject = TypeVar('GenericObject')


# def load_objects_from_storage(metadata_filename: str, class_factory: GenericObject, root_directory: Path) -> Mapping[UUID, GenericObject]:
def load_objects_from_storage(metadata_filename: str, class_factory: GenericObject, root_directory: Path) -> dict:
    return excepting_pipe(
        list_files(root_directory, metadata_filename),
        curry(map)(load_json),
        curry(map)(class_factory.from_json),
        curry(map)(lambda _: (_.id, _)),
        dict
    )


@curry
def create_object_from_archive(parent_id: UUID, metadata_filename: str, class_factory: GenericObject, root_directory: Path, keys: List[str], context: dict) -> dict:
    # Generate new ID for the object
    object_id = uuid4()

    # The tar file is mostly created in two ways:
    # a) Adding a single parent directory to the archive
    # b) All image directories are in the root of the tar archive

    # Extract all dirs of the archive
    sub_dirs = list(filter(lambda p: p.is_dir() and not str(p).startswith('.'), context['current_dir'].iterdir()))

    # If there is only one directory, assume it contains all the important data and use it as new root
    archive_root = context['current_dir']
    if len(sub_dirs) == 1:
        archive_root = archive_root / sub_dirs[0]

    # Create object description
    object_dict = dict(archive_root=archive_root)

    # Read the metadata
    with open(str(archive_root / metadata_filename), 'r') as fp:
        metadata = json.load(fp)

    # Store the new object in the new location
    # Save the parent_id
    if parent_id:
        object_dict['parent_id'] = parent_id
        storage_path = root_directory / str(parent_id) / str(object_id)
    else:
        storage_path = root_directory / str(object_id)

    # Save metadata for this object
    object_meta_new = dict(id=object_id,
                           storage_path=storage_path,
                           created=datetime.now().isoformat())

    # Add parent_id to meta
    if parent_id:
        object_meta_new['parent_id'] = parent_id

    # Extract attributes from the metadata file (missing values are filled by empty strings)
    object_meta_from_file = merge(map(lambda k: {k: metadata.get(k, '')}, keys))

    # Merge metadata from system and file
    object_meta_final = merge(object_meta_new, object_meta_from_file)

    # Generate the new object
    object_dict[class_factory.__name__.lower()] = class_factory.from_dict(object_meta_final)

    return merge(context, object_dict)


def slimline_dict(dictionary):
    new_dict = dict()

    for k, v in dictionary.items():
        if type(v) == dict:
            new_dict2 = slimline_dict(v)
            new_dict = merge(new_dict, new_dict2)
        else:
            new_dict[k] = v

    return new_dict
