import json
from uuid import UUID

import falcon
from falcon import Request, Response

from mmlp.manager.ModelManager import ModelManager


class ModelVersionParameters:
    def __init__(self, model_manager: ModelManager):
        self._model_manager = model_manager

    def on_get(self, _: Request, resp: Response, model_id: UUID, git_commit_id: str):
        result = self._model_manager.model_version_parameters(model_id, git_commit_id)
        if isinstance(result, Exception):
            resp.body = json.dumps(dict(error=str(result)))
            resp.status = falcon.HTTP_500
        else:
            resp.body = json.dumps(result)
            resp.status = falcon.HTTP_200
