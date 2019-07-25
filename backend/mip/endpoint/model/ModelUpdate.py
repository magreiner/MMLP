import json
from uuid import UUID

import falcon
from falcon import Request, Response

from mip.data.utils import DataclassJSONEncoder
from mip.manager.ModelManager import ModelManager


class ModelUpdate:

    def __init__(self, model_manager: ModelManager):
        self._model_manager: ModelManager = model_manager

    def on_get(self, _: Request, resp: Response, model_id: UUID):
        result = self._model_manager.update_model(model_id)
        if isinstance(result, Exception):
            resp.body = json.dumps(dict(error=str(result)))
            resp.status = falcon.HTTP_500
        else:
            resp.body = json.dumps(dict(result), cls=DataclassJSONEncoder)
            resp.status = falcon.HTTP_201
