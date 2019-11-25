from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List
from uuid import UUID, uuid4

from mmlp import Config
from mmlp.data.DatasetVersion import DatasetVersion
from mmlp.data.Model import Model
from mmlp.data.utils import AbstractEntity
from mmlp.utils import ensure_uuid


@dataclass
class ModelSnapshot(AbstractEntity):
    id: UUID
    model: Model
    model_git_commit: str
    parent_id: ModelSnapshot
    dataset_version: DatasetVersion
    input_data_path: Path
    parameters: dict
    code_directory: Path
    pre_processing: dict
    post_processing: dict
    storage_path: Path
    archive_path: Path
    container_id: str
    container_name: str
    container_image_id: str
    container_image_name: str
    container_mount_volumes: dict
    container_environment_variables: dict
    container_ports: dict
    container_build_logs: dict
    container_pre_processing_logs: str
    container_pull_logs: dict
    container_push_logs: dict
    container_run_logs: str
    container_archive_path: Path
    container_performance_statistics: List
    container_info: dict
    new_container_image_name: str
    success: bool
    status: str
    created: datetime
    finished: datetime
    runtime_logs: dict
    performance_metrics: dict

    @staticmethod
    def from_json(data: dict):
        data['model'] = Model.from_json(data['model'])
        # if data.get('parent_id', False):
        #     data['parent_id'] = ModelSnapshot.from_json(data['parent_id'])
        data['dataset_version'] = DatasetVersion.from_json(data['dataset_version'])

        return ModelSnapshot.from_dict(data)

    @staticmethod
    def from_dict(data: dict):
        config = Config.Config.from_dict()
        return ModelSnapshot(
            id=ensure_uuid(data.get('id', uuid4())),
            model=data['model'],
            model_git_commit=data['model_git_commit'],
            parent_id=data.get('parent_id', None),
            dataset_version=data['dataset_version'],
            input_data_path=data['dataset_version'].storage_path,
            parameters=data['parameters'],
            code_directory=data.get('code_directory', Path(data['storage_path']) / "source_code"),
            pre_processing=data.get('pre_processing', {}),
            post_processing=data.get('pre_processing', {}),
            storage_path=Path(data['storage_path']),
            archive_path=data.get('archive_path', Path("")),
            container_id=data.get('container_id', None),
            container_name=data['container_name'],
            container_image_id=data.get('container_image_id', None),
            container_image_name=data.get('container_image_name',
                                          f"{config.docker_registry}model_{data['model_git_commit']}"),
            container_mount_volumes=data.get('container_mount_volumes', {}),
            container_environment_variables=data.get('container_environment_variables', {}),
            container_ports=data.get('container_ports', {}),
            container_build_logs=data.get('container_build_logs', {"info": "no build required."}),
            container_pre_processing_logs=data.get('container_pre_processing_logs', ""),
            container_pull_logs=data.get('container_pull_logs', {}),
            container_push_logs=data.get('container_push_logs', {}),
            container_run_logs=data.get('container_run_logs', ''),
            container_archive_path=Path(data.get('container_archive_path', Path(data['storage_path']) / 'container_archive.tar.gz')),
            container_performance_statistics=data.get('statistics', ''),
            container_info=data.get('container_info', dict()),
            new_container_image_name=data.get('new_container_image_name', ''),
            success=data.get('success', 'not finished'),
            status=data.get('status', 'not started yet'),
            created=datetime.fromisoformat(data['created']),
            finished=datetime.fromisoformat(data.get('finished', str(datetime(1, 1, 1, 1, 1, 1, 1)))),
            runtime_logs=data.get('runtime_logs', 'not set yet'),
            performance_metrics=data.get('performance_metrics', 'not set yet')
        )
