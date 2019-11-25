import json
from uuid import UUID

import falcon
from falcon import Request, Response

from mmlp.manager.DatasetManager import DatasetManager


class DatasetVersionCount:
    def __init__(self, dataset_manager: DatasetManager):
        self._dataset_manager = dataset_manager

    def on_get(self, _: Request, resp: Response, dataset_id: UUID):
        result = self._dataset_manager.dataset_version_count(dataset_id)
        if isinstance(result, Exception):
            resp.body = json.dumps(dict(error=str(result)))
            resp.status = falcon.HTTP_500
        else:
            resp.body = json.dumps(dict(count=result))
            resp.status = falcon.HTTP_200
