import falcon
import json
from falcon import Request, Response
from uuid import UUID

from mmlp.manager.DatasetManager import DatasetManager
from mmlp.utils import get_params_to_query

SORT_ATTRIBUTES = ['created']


class DatasetVersionCollection:
    def __init__(self, dataset_manager: DatasetManager):
        self._dataset_manager = dataset_manager

    def on_get(self, req: Request, resp: Response, dataset_id: UUID):
        query = get_params_to_query(req, SORT_ATTRIBUTES, 'created', 'desc')
        print(f'query: {query}')
        versions = self._dataset_manager.versions(dataset_id, query)
        resp.body = f"[{','.join(map(lambda v: v.json(), versions))}]"

    def on_post(self, req: Request, resp: Response, dataset_id: UUID):
        result = self._dataset_manager.add_version(req, str(dataset_id))
        if isinstance(result, Exception):
            resp.body = json.dumps(dict(error=str(result)))
            resp.status = falcon.HTTP_500
        elif isinstance(result, dict):
            resp.body = json.dumps(result)
            resp.status = falcon.HTTP_200
        else:
            resp.body = result.json()
            resp.status = falcon.HTTP_201
