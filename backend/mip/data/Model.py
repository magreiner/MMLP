from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from uuid import UUID

from mip.data.utils import AbstractEntity
from mip.utils import ensure_uuid


@dataclass
class Model(AbstractEntity):
    id: UUID
    source_url: str
    name: str
    description: str
    license: str
    origin: str
    maintainer: str
    storage_path: Path
    code_path: Path
    created: datetime

    @staticmethod
    def from_json(data: dict):
        return Model.from_dict(data)

    @staticmethod
    def from_dict(data: dict):
        return Model(
            id=ensure_uuid(data['id']),
            source_url=data['source_url'],
            name=data.get('name', "No name provided."),
            description=data.get('description', "No description provided."),
            license=data.get('license', "No license provided."),
            origin=data.get('origin', "No origin provided."),
            maintainer=data.get('maintainer', "No maintainer provided."),
            storage_path=Path(data['storage_path']),
            code_path=Path(data['code_path']),
            created=datetime.fromisoformat(data['created'])
        )


