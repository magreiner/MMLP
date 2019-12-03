# To use the instance return type from static methods
from __future__ import annotations

import dataclasses
import shutil
from falcon import Request
from pathlib import Path
from toolz import get, partition_all, curry, assoc, map, valfilter, dissoc, do
from typing import Iterator, Mapping, Union
from uuid import UUID

from mmlp.Config import Config
from mmlp.data import Dataset
from mmlp.data import DatasetVersion
from mmlp.manager.utils.datasetUtils import move_to_storage, \
    create_initial_version, partition_versions
from mmlp.manager.utils.utils import load_objects_from_storage, create_object_from_archive
from mmlp.utils import excepting_pipe, extract_tarball_to_temp_dir, \
    ensure_no_metadata_files_present, ensure_uuid, process_multi_part_upload


class DatasetManager:
    def __init__(self, config: Config, datasets: Mapping[UUID, Dataset], versions: Mapping[UUID, DatasetVersion]):
        self._config = config
        self._datasets: Mapping[UUID, Dataset] = datasets
        self._versions: Mapping[UUID, DatasetVersion] = versions

        if hasattr(self._datasets, "keys"):
            print(f'DatasetManager:  Loaded {len(self._datasets.keys())} data sets')
        else:
            print("FATAL DatasetManager: Could not load data sets, sorry :(")

        if hasattr(self._versions, "keys"):
            print(f'DatasetManager:  Loaded {len(self._versions.keys())} data set versions')
        else:
            print("FATAL DatasetManager: Could not load data set versions, sorry :(")

    @staticmethod
    def load(config: Config) -> DatasetManager:

        print(f'DatasetManager:  Loading datasets from: {config.dataset_base_dir}')

        return DatasetManager(config=config,
                              datasets=load_objects_from_storage(metadata_filename=config.dataset_filename,
                                                                 class_factory=Dataset,
                                                                 root_directory=config.dataset_base_dir),
                              versions=load_objects_from_storage(metadata_filename=config.version_filename,
                                                                 class_factory=DatasetVersion,
                                                                 root_directory=config.dataset_base_dir))

    @curry
    def store_dataset(self, dataset_filename: str, version_filename: str, context: dict) -> Dataset:
        # Get dataset info from context
        dataset = context['dataset']
        version = context['datasetversion']

        # Serialize dataset
        with open(str(Path(dataset.storage_path) / dataset_filename), 'w') as fp:
            fp.write(dataset.json())

        # Serialize version
        with open(str(Path(version.storage_path) / version_filename), 'w') as fp:
            fp.write(version.json())

        # Add objects to the dataset manager
        self._datasets = assoc(self._datasets, dataset.id, dataset)
        self._versions = assoc(self._versions, version.id, version)

        return dataset

    @curry
    def store_version(self, version_filename: str, context: dict) -> DatasetVersion:
        version = context['datasetversion']

        # get the name of the parent dataset
        version = dataclasses.replace(version, name=self.get_dataset(version.parent_id).name)

        # Serialize version
        with open(str(Path(version.storage_path) / version_filename), 'w') as fp:
            fp.write(version.json())

        # Add these objects to the dataset manager
        self._versions = assoc(self._versions, version.id, version)

        # return dict(version=version)
        return version

    # -------------------------------------------------------------------------
    # Access methods
    # -------------------------------------------------------------------------
    # Returns a list of Dataset objects
    def datasets(self, query: dict) -> Iterator[Dataset]:
        """
        List all datasets
        :param query:
        :return:
        """
        # TODO: Not completely pure pipeline
        return excepting_pipe(
            self._datasets.values(),
            curry(sorted, key=lambda ds: getattr(ds, query['sortby']), reverse=query['order']),
            curry(partition_all)(query['limit'] if query['limit'] > 0 else len(self._datasets.values())),
            list,
            curry(get, default=[])(query['offset'])
        )

    # Return all versions of a dataset
    def versions(self, dataset_id: UUID, query: dict) -> Iterator[DatasetVersion]:
        """
        Lists all versions of a given dataset
        :param dataset_id:
        :param query:
        :return:
        """
        # TODO: Not completely pure pipeline
        return excepting_pipe(
            self._versions.values(),
            curry(filter)(lambda v: v.parent_id == ensure_uuid(dataset_id)),
            curry(sorted, key=lambda ds: getattr(ds, query['sortby']), reverse=query['order']),
            partition_versions(query),
            list,
            curry(get, default=[])(query['offset'])
        )

    # Return version to a given dataset
    def version(self, dataset_id: UUID, version_id: UUID) -> Union[str, DatasetVersion]:
        dataset_versions = valfilter(lambda _: _.parent_id == ensure_uuid(dataset_id), self._versions)
        if not len(dataset_versions):
            return f'dataset: {dataset_id} not found'
        print(dataset_versions.keys())
        print(f'version id: {version_id}')
        version = dataset_versions.get(ensure_uuid(version_id))
        return version if version else f'version {version_id} not found in dataset {dataset_id}'

    # Create a new dataset
    def create_dataset(self, req: Request) -> Union[Exception, dict, Dataset]:
        file = process_multi_part_upload(req)

        if file.get('temp_dir', False):
            return excepting_pipe(
                file,
                extract_tarball_to_temp_dir,
                create_object_from_archive(None,
                                           self._config.dataset_filename,
                                           Dataset,
                                           self._config.dataset_base_dir,
                                           self._config.dataset_meta_attributes),
                create_initial_version,
                ensure_no_metadata_files_present(self._config.metadata_file_list),
                move_to_storage,
                DatasetManager.store_dataset(self, self._config.dataset_filename, self._config.version_filename)
            )
        else:
            # Return feedback on current progress
            return file

    def add_version(self, req: Request, dataset_id: str) -> Union[Exception, DatasetVersion]:
        file = process_multi_part_upload(req)

        if file.get('temp_dir', False):
            return excepting_pipe(
                file,
                extract_tarball_to_temp_dir,
                create_object_from_archive(dataset_id,
                                           self._config.dataset_filename,
                                           DatasetVersion,
                                           self._config.dataset_base_dir,
                                           self._config.version_meta_attributes),
                ensure_no_metadata_files_present(self._config.metadata_file_list),
                move_to_storage,
                DatasetManager.store_version(self, self._config.version_filename)
            )
        else:
            # Return feedback on current progress
            return file

    # Returns a dataset by id
    def get_dataset(self, dataset_id: UUID) -> Union[Exception, Dataset]:
        dataset = self._datasets.get(ensure_uuid(dataset_id))
        return dataset if dataset else Exception(f'dataset: {dataset_id} not found')

    @curry
    def get_version(self, dataset_id: UUID, version_id: UUID) -> Union[Exception, DatasetVersion]:
        version = self._versions.get(ensure_uuid(version_id))
        if dataset_id != version.parent_id:
            return Exception(f'version {version_id} does not belong to dataset {dataset_id}')
        return version if version else Exception(f'version: {version_id} of dataset {dataset_id} not found')

    @curry
    def get_dataset_version(self, version_id: UUID) -> DatasetVersion:
        dataset_version = self._versions.get(ensure_uuid(version_id))
        return dataset_version if dataset_version else Exception(f'Dataset Version: {version_id} not found')

    # Remove one version
    def unload_version(self, version: DatasetVersion) -> DatasetVersion:
        self._versions = dissoc(self._versions, version.id)
        return version

    # List all versions of a particular dataset
    def list_dataset_versions(self, dataset: Dataset) -> Iterator[str]:
        return excepting_pipe(
            self._versions.values(),
            curry(filter)(lambda v: v.parent_id == dataset.id),
            curry(map)(lambda ds: ds.id)
        )

    # Unload all versions for this particular dataset
    def unload_dataset_versions(self, dataset: Dataset) -> Dataset:
        # version_ids = filter(lambda version: version.parent_id == dataset.id, self._versions.values())
        version_ids = self.list_dataset_versions(dataset)
        self._versions = dissoc(self._versions, *version_ids)
        return dataset

    # Unload dataset from data manager
    def unload_dataset(self, dataset: Dataset) -> Dataset:
        self._datasets = dissoc(self._datasets, dataset.id)
        return dataset

    def delete_dataset(self, dataset_id: UUID) -> Union[Exception, Dataset]:
        return excepting_pipe(
            ensure_uuid(dataset_id),
            self.get_dataset,
            # Remove complete dataset directory
            curry(do)(lambda ds: shutil.rmtree(ds.storage_path)),
            # Unload dataset from data manager
            self.unload_dataset,
            # Unload all dataset versions from data manager
            self.unload_dataset_versions
        )

    # Check if dataset has more than one version
    def check_version_delete(self, version: DatasetVersion) -> Union[Exception, DatasetVersion]:
        dataset = self.get_dataset(version.parent_id)
        version_ids = list(self.list_dataset_versions(dataset))
        return version if len(version_ids) > 1 else Exception(
            f'version {version.id} is the only version of dataset {version.parent_id}')

    # Delete a version of a dataset
    def delete_version(self, dataset_id: UUID, version_id: UUID) -> Union[Exception, DatasetVersion]:
        return excepting_pipe(
            version_id,
            self.get_version(ensure_uuid(dataset_id)),
            self.check_version_delete,
            # Remove the version directory
            curry(do)(lambda v: shutil.rmtree(v.storage_path)),
            self.unload_version
        )

    # Count the data sets available to the platform
    def dataset_count(self):
        return len(self._datasets)

    # Count the versions of a specific data set
    def dataset_version_count(self, dataset_id: UUID) -> Union[Exception, int]:
        return excepting_pipe(
            self._versions.values(),
            curry(filter)(lambda version: version.parent_id == ensure_uuid(dataset_id)),
            list,
            len
        )
