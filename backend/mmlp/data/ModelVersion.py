from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from mmlp.data import Model
from mmlp.data.utils import AbstractEntity
from mmlp.utils import ensure_uuid


@dataclass
class ModelVersion(AbstractEntity):
    id: UUID
    name: str
    git_commit_id: str
    model: Model
    author: str
    description: str
    created: datetime

    @staticmethod
    def from_dict(data: dict):
        return ModelVersion(
            id=ensure_uuid(data['id']),
            name=data['name'],
            git_commit_id=data['git_commit_id'],
            model=data['model'],
            author=data['author'],
            description=data['description'],
            created=datetime.fromisoformat(data['created'])
        )

    @staticmethod
    def from_model_version_id(id: UUID):
        pass

    @staticmethod
    def from_json(data: dict):
        return ModelVersion.from_dict(data)
