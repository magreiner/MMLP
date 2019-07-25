import shutil
from pathlib import Path
from typing import List
from uuid import uuid4

from toolz import curry, assoc, partition_all

from mip.data import DatasetVersion


def create_initial_version(context: dict) -> dict:
    version_id = uuid4()
    dataset = context['dataset']
    version_path = Path(dataset.storage_path) / str(version_id)
    version = DatasetVersion.from_dict(dict(id=version_id,
                                            name=dataset.name,
                                            parent_id=dataset.id,
                                            description=dataset.description,
                                            created=str(dataset.created),
                                            storage_path=version_path))
    return assoc(context, 'datasetversion', version)


def move_to_storage(context: dict) -> dict:
    version = context['datasetversion']
    shutil.move(str(context['archive_root']), str(version.storage_path))
    shutil.rmtree(context['temp_dir'])
    return assoc(context, 'datasetversion', version)


@curry
# Note that the versions have been converted to a list by the sorted function already
# TODO: This function seems to be duplicated in different managers, move to utils
def partition_versions(query: dict, versions: List[DatasetVersion]) -> List[DatasetVersion]:
    limit = query['limit']
    return list(partition_all(limit if limit > 0 else len(versions), versions))
