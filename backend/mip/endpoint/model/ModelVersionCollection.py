from uuid import UUID

from falcon import Request, Response

from mip.manager.ModelManager import ModelManager
from mip.utils import get_params_to_query

SORT_ATTRIBUTES = ['created', 'author']


class ModelVersionCollection:
    def __init__(self, model_manager: ModelManager):
        self._model_manager = model_manager

    def on_get(self, req: Request, resp: Response, model_id: UUID):
        query = get_params_to_query(req, SORT_ATTRIBUTES, 'created', 'desc')
        versions = self._model_manager.versions(model_id, query)
        resp.body = f"[{','.join(map(lambda v: v.json(), versions))}]"
