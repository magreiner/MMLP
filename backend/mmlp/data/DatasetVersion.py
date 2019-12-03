from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from uuid import UUID

from mmlp.data.utils import AbstractEntity
from mmlp.utils import ensure_uuid


@dataclass
class DatasetVersion(AbstractEntity):
    id: UUID
    name: str
    parent_id: UUID
    description: str
    created: datetime
    storage_path: Path

    @staticmethod
    def from_dict(data: dict):
        return DatasetVersion(
            id=ensure_uuid(data['id']),
            name=data.get('name', 'no name provided'),
            parent_id=data['parent_id'] if type(data['parent_id']) == UUID else UUID(data['parent_id']),
            description=data['description'],
            created=datetime.fromisoformat(data['created']),
            storage_path=Path(data.get('storage_path', ''))
        )

    @staticmethod
    def from_json(data: dict):
        return DatasetVersion.from_dict(data)
