from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from mmlp.data.ModelSnapshot import ModelSnapshot
from mmlp.data.utils import AbstractEntity
from mmlp.utils import ensure_uuid


@dataclass
class Method(AbstractEntity):
    id: UUID
    name: str
    created: datetime
    description: str
    model_snapshot: ModelSnapshot
    pre_processing: dict
    post_processing: dict

    @staticmethod
    def from_dict(data: dict):
        return Method(
            id=ensure_uuid(data['id']),
            name=data['name'],
            created=datetime.fromisoformat(data['created']),
            description=data['description'],
            model_snapshot=data['model_snapshot'],
            pre_processing=data.get('pre_processing', {}),
            post_processing=data.get('pre_processing', {})
        )

    @staticmethod
    def from_json(data: dict):
        data['model_snapshot'] = ModelSnapshot.from_json(data['model_snapshot'])
        return Method.from_dict(data)
