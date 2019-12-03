import falcon
import json
from dataclasses import asdict
from falcon import Request, Response
from toolz import map

from mmlp.data import Dataset
from mmlp.data.utils import DataclassJSONEncoder
from mmlp.manager.DatasetManager import DatasetManager
from mmlp.utils import get_params_to_query

# TODO: Limit maximum items to 500
MAX_ITEMS = 500
SORT_ATTRIBUTES = ['id', 'name', 'description', 'license', 'origin', 'maintainer', 'storage_path', 'created']


class DatasetCollection:
    def __init__(self, dataset_manager: DatasetManager):
        self._dataset_manager: DatasetManager = dataset_manager

    @staticmethod
    def serialize_dataset(dataset: Dataset) -> str:
        return json.dumps(asdict(dataset), cls=DataclassJSONEncoder)

    def on_get(self, req: Request, resp: Response):
        # limit = safe_int(req.params.get('limit', 0))
        # offset = safe_int(req.params.get('offset', 0))
        # sortby = req.params.get('sortby') if req.params.get('sortby') in SORT_ATTRIBUTES else 'created'
        # order = True if req.params.get('order') == 'desc' else False
        # datasets = self._dataset_manager.datasets(limit=limit, offset=offset, sortby=sortby, order=order)
        query = get_params_to_query(req, SORT_ATTRIBUTES, 'created', 'desc')
        datasets = self._dataset_manager.datasets(query)
        resp.body = f"[{','.join(map(lambda ds: ds.json(), datasets))}]"

    def on_post(self, req: Request, resp: Response):
        result = self._dataset_manager.create_dataset(req)
        if isinstance(result, Exception):
            resp.body = json.dumps(dict(error=str(result)))
            resp.status = falcon.HTTP_500
        elif isinstance(result, dict):
            resp.body = json.dumps(result)
            resp.status = falcon.HTTP_200
        else:
            resp.body = result.json()
            resp.status = falcon.HTTP_201
