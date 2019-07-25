# To use the instance return type from static methods
from __future__ import annotations

from pathlib import Path
from typing import Mapping, Union, Iterator
from uuid import UUID

from shutil import rmtree

import docker
from toolz import curry, partition_all, get, excepts

from mip.Config import Config
from mip.data import ModelSnapshot
from mip.endpoint.compute.utils import transform_dataclass_to_dict
from mip.manager.utils.utils import load_objects_from_storage
from mip.utils import ensure_uuid, excepting_pipe
from mip.utils.utils import write_json_file


class SnapshotManager:
    def __init__(self, config: Config, snapshots: Mapping[UUID, ModelSnapshot]):
        self._config: Config = config
        self._snapshots: Mapping[UUID, ModelSnapshot] = snapshots
        # Todo: use docker manager for that
        self._d = docker.from_env()

        if hasattr(self._snapshots, "keys"):
            print(f'SnapshotManager: Loaded {len(self._snapshots.keys())} snapshots')
        else:
            print("FATAL SnapshotManager: Could not load model snapshots, sorry :(")

    @staticmethod
    def load(config: Config) -> SnapshotManager:
        # print(f'SnapshotManager: Loading snapshots from: {config.model_base_dir}')
        return SnapshotManager(config=config,
                               snapshots=load_objects_from_storage(metadata_filename=config.model_snapshot_filename,
                                                                   class_factory=ModelSnapshot,
                                                                   root_directory=config.model_base_dir))

    def create_snapshot(self, snap: ModelSnapshot) -> Union[Exception, ModelSnapshot]:
        if self._snapshots.get(snap.id, None):
            raise Exception("create_snapshot", f"Snapshot with ID {snap.id} is already known")

        # Create snapshot on filesystem
        Path(snap.storage_path).mkdir(parents=True)

        write_json_file(str(Path(snap.storage_path) / self._config.model_snapshot_filename), transform_dataclass_to_dict(snap))

        # add snap object
        self._snapshots[snap.id] = snap

        return snap

    def replace(self, snap):
        if not self._snapshots.get(snap.id, None):
            raise Exception("replace_snapshot", f"Snapshot with ID {snap.id} is not known")

        # Update snapshot file
        write_json_file(str(Path(snap.storage_path) / self._config.model_snapshot_filename), transform_dataclass_to_dict(snap))

        # Replace snapshot object
        self._snapshots.pop(snap.id)
        self._snapshots[snap.id] = snap

        return snap

    def remove_snapshot(self, snap: ModelSnapshot) -> Union[Exception, ModelSnapshot]:
        if not self._snapshots.get(snap.id, None):
            raise Exception("remove_snapshot", f"Snapshot {snap.id} is not known")

        # remove container image
        # Todo: Fix issue with depending child images
        i = excepts(Exception, lambda image: self._d.images.get(image), lambda _: -1)(snap.new_container_image_name)
        excepts(Exception, lambda image: self._d.images.remove(image.id, force=True), lambda _: -1)(i)

        # Remove the method file from filesystem
        rmtree(str(snap.storage_path))

        # Remove object from collection
        self._snapshots.pop(snap.id)

        return snap

    def get_snapshot(self, snap_id: UUID) -> Union[Exception, ModelSnapshot]:

        snap = self._snapshots.get(ensure_uuid(snap_id))
        return snap if snap else Exception(f'Model Snapshot: {snap_id} not found')

    def list_snapshots_filtered(self, model_id: UUID, git_commit_id: str, query: dict) -> Mapping[UUID, ModelSnapshot]:
        return excepting_pipe(
            self._snapshots.values(),
            curry(filter)(lambda v: v.model.id == ensure_uuid(model_id)),
            curry(filter)(lambda v: v.model_git_commit == git_commit_id),
            curry(sorted, key=lambda snap: getattr(snap, query['sortby']), reverse=query['order']),
            curry(partition_all)(query['limit'] if query['limit'] > 0 else len(self._snapshots.values())),
            list,
            curry(get, default=[])(query['offset'])
        )

    def list_snapshots(self, query: dict) -> Iterator[ModelSnapshot]:
        """
        List all datasets
        :param query:
        :return:
        """
        # TODO: Not completely pure pipeline
        return excepting_pipe(
            self._snapshots.values(),
            curry(sorted, key=lambda snap: getattr(snap, query['sortby']), reverse=query['order']),
            curry(partition_all)(query['limit'] if query['limit'] > 0 else len(self._snapshots.values())),
            list,
            curry(get, default=[])(query['offset'])
        )

    def list_running_snapshots(self, query: dict) -> Iterator[ModelSnapshot]:
        """
        List all datasets
        :param query:
        :return:
        """
        # TODO: Not completely pure pipeline
        return excepting_pipe(
            self._snapshots.values(),
            curry(sorted, key=lambda snap: getattr(snap, query['sortby']), reverse=query['order']),
            curry(filter)(lambda s: s.status != 'finished'),
            curry(partition_all)(query['limit'] if query['limit'] > 0 else len(self._snapshots.values())),
            list,
            curry(get, default=[])(query['offset'])
        )

    def snapshot_count(self):
        return len(self._snapshots)
