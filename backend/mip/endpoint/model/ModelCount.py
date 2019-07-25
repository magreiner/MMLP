import json

from falcon import Request, Response

from mip.manager.ModelManager import ModelManager


class ModelCount:
    def __init__(self, model_manager: ModelManager):
        self._model_manager: ModelManager = model_manager

    def on_get(self, _: Request, resp: Response):
        resp.body = json.dumps(dict(count=self._model_manager.model_count()))
