import json

import falcon
from falcon import Request, Response

from mip.manager.ModelManager import ModelManager
from mip.utils import get_params_to_query

SORT_ATTRIBUTES = ['id', 'name', 'created']


class ModelCollection:
    def __init__(self, model_manager: ModelManager):
        self._model_manager: ModelManager = model_manager

    def on_get(self, req: Request, resp: Response):
        # limit = safe_int(req.params.get('limit', 0))
        # offset = safe_int(req.params.get('offset', 0))
        # sortby = req.params.get('sortby') if req.params.get('sortby') in SORT_ATTRIBUTES else 'created'
        # order = True if req.params.get('order') == 'desc' else False
        # models = self._model_manager.models(limit=limit, offset=offset, sortby=sortby, order=order)
        query = get_params_to_query(req, SORT_ATTRIBUTES, 'created', 'desc')
        models = self._model_manager.models(query)
        resp.body = f"[{','.join(map(lambda ds: ds.json(), models))}]"

    def on_post(self, req: Request, resp: Response):
        result = self._model_manager.import_model(req)
        if isinstance(result, Exception):
            resp.body = json.dumps(dict(error=str(result)))
            resp.status = falcon.HTTP_500
        else:
            resp.body = result.json()
            resp.status = falcon.HTTP_201
