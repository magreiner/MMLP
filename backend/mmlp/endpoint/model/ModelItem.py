import json
from uuid import UUID

import falcon
from falcon import Request, Response

from mmlp.data import Model
from mmlp.manager import ModelManager


class ModelItem:
    def __init__(self, model_manager: ModelManager):
        self._model_manager = model_manager

    def on_get(self, _: Request, resp: Response, model_id: UUID):
        result = self._model_manager.get_model(model_id)
        if isinstance(result, Model):
            resp.body = result.json()
            resp.status = falcon.HTTP_202
        else:
            resp.body = json.dumps(dict(error=result))
            resp.status = falcon.HTTP_404

    def on_delete(self, _: Request, resp: Response, model_id: UUID):
        result = self._model_manager.delete_model(model_id)
        if isinstance(result, Model):
            resp.body = result.json()
            resp.status = falcon.HTTP_202
        else:
            resp.body = json.dumps(dict(error=str(result)))
            resp.status = falcon.HTTP_404
