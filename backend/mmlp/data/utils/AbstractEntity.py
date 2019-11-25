import json
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass

from mmlp.data.utils import DataclassJSONEncoder


@dataclass
class AbstractEntity(ABC):
    @staticmethod
    @abstractmethod
    def from_dict(data: dict):
        raise NotImplementedError

    def json(self):
        return json.dumps(asdict(self), cls=DataclassJSONEncoder)
