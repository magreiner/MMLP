import falcon
import json
from falcon import Request, Response
from uuid import UUID

from mmlp.data import DatasetVersion
from mmlp.manager.DatasetManager import DatasetManager


class DatasetVersionItem:
    def __init__(self, dataset_manager: DatasetManager):
        self._dataset_manager = dataset_manager

    def on_get(self, _: Request, resp: Response, dataset_id: UUID, version_id: UUID):
        result = self._dataset_manager.version(dataset_id, version_id)
        if isinstance(result, DatasetVersion):
            resp.body = result.json()
            resp.status = falcon.HTTP_200
        else:
            resp.body = json.dumps(dict(error=result))
            resp.status = falcon.HTTP_404

    def on_delete(self, _: Request, resp: Response, dataset_id: UUID, version_id: UUID):
        result = self._dataset_manager.delete_version(dataset_id, version_id)
        if isinstance(result, DatasetVersion):
            resp.body = result.json()
            resp.status = falcon.HTTP_200
        else:
            resp.body = json.dumps(dict(error=str(result)))
            resp.status = falcon.HTTP_404
