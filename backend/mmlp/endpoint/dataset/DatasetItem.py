import json
from uuid import UUID

import falcon
from falcon import Request, Response

from mmlp.data import Dataset
from mmlp.manager.DatasetManager import DatasetManager


class DatasetItem:
    def __init__(self, dataset_manager: DatasetManager):
        self._dataset_manager = dataset_manager

    def on_get(self, _: Request, resp: Response, dataset_id: UUID):
        result = self._dataset_manager.get_dataset(dataset_id)
        if isinstance(result, Dataset):
            resp.body = result.json()
            resp.status = falcon.HTTP_202
        else:
            resp.body = json.dumps(dict(error=result))
            resp.status = falcon.HTTP_404

    def on_delete(self, _: Request, resp: Response, dataset_id: UUID):
        result = self._dataset_manager.delete_dataset(dataset_id)
        if isinstance(result, Dataset):
            resp.body = result.json()
            resp.status = falcon.HTTP_202
        else:
            resp.body = json.dumps(dict(error=str(result)))
            resp.status = falcon.HTTP_404
