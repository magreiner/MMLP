from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from uuid import UUID
from mip.data.utils import AbstractEntity
from mip.utils import ensure_uuid


@dataclass
class Dataset(AbstractEntity):
    id: UUID
    name: str
    description: str
    license: str
    origin: str
    maintainer: str
    storage_path: str
    created: datetime

    @staticmethod
    def from_dict(data: dict):
        return Dataset(
            id=ensure_uuid(data['id']),
            name=data['name'],
            description=data['description'],
            license=data['license'],
            origin=data['origin'],
            maintainer=data['maintainer'],
            storage_path=str(Path(data.get('storage_path', ''))),
            created=datetime.fromisoformat(data['created'])
        )

    @staticmethod
    def from_json(data: dict):
        return Dataset.from_dict(data)
