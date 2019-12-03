from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List
from uuid import UUID

from mmlp.data.Method import Method
from mmlp.data.utils import AbstractEntity
from mmlp.utils import ensure_uuid


@dataclass
class Result(AbstractEntity):
    id: UUID
    method: Method
    storage_path: Path
    archive_path: Path
    input_data_path: Path
    code_directory: Path
    pre_processing: dict
    post_processing: dict
    container_id: str
    container_name: str
    container_image_name: str
    container_pull_logs: dict
    container_pre_processing_logs: str
    container_performance_statistics: List
    container_run_logs: str
    container_info: dict
    container_mount_volumes: dict
    container_environment_variables: dict
    container_ports: dict
    container_archive_path: Path
    status: str
    success: bool
    running: bool
    issuer: str
    created: datetime
    finished: datetime
    runtime_logs: dict
    performance_metrics: dict

    @staticmethod
    def from_dict(data: dict):
        return Result(
            id=ensure_uuid(data['id']),
            method=data['method'],
            storage_path=Path(data['storage_path']),
            archive_path=data.get('archive_path', Path("")),
            input_data_path=Path(data['input_data_path']),
            code_directory=data.get('code_directory', Path(data['method'].model_snapshot.code_directory)),
            pre_processing=data.get('pre_processing', {}),
            post_processing=data.get('pre_processing', {}),
            container_id=data.get('container_id', None),
            container_name=data['container_name'],
            container_image_name=data['method'].model_snapshot.new_container_image_name,
            container_pull_logs=data.get('container_pull_logs', {}),
            container_performance_statistics=data.get('statistics', ''),
            container_pre_processing_logs=data.get('container_pre_processing_logs', ""),
            container_run_logs=data.get('container_run_logs', ''),
            container_info=data.get('container_info', dict()),
            container_ports=data.get('container_ports', {}),
            status=data.get('status', 'not started yet'),
            container_mount_volumes=data.get('container_mount_volumes', {}),
            container_environment_variables=data.get('container_environment_variables', {}),
            container_archive_path=Path(
                data.get('container_archive_path', Path(data['storage_path']) / 'container_archive.gz')),
            success=data['success'],
            running=data['running'],
            issuer=data['issuer'],
            created=datetime.fromisoformat(data['created']),
            finished=datetime.fromisoformat(data.get('finished', str(datetime(1, 1, 1, 1, 1, 1, 1)))),
            runtime_logs=data.get('runtime_logs', dict()),
            performance_metrics=data.get('performance_metrics', dict())
        )

    @staticmethod
    def from_json(data: dict):
        data['method'] = Method.from_json(data['method'])
        return Result.from_dict(data)
