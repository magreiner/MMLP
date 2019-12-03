import falcon
import json
from falcon import Request, Response
from uuid import UUID

from mmlp.manager.ModelManager import ModelManager


class ModelVersionCount:
    def __init__(self, model_manager: ModelManager):
        self._model_manager = model_manager

    def on_get(self, _: Request, resp: Response, model_id: UUID):
        result = self._model_manager.model_version_count(model_id)
        if isinstance(result, Exception):
            resp.body = json.dumps(dict(error=str(result)))
            resp.status = falcon.HTTP_500
        else:
            resp.body = json.dumps(dict(count=result))
            resp.status = falcon.HTTP_200
