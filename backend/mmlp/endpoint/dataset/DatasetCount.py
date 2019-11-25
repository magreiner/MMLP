import json

from falcon import Request, Response

from mmlp.manager.DatasetManager import DatasetManager


class DatasetCount:
    def __init__(self, dataset_manager: DatasetManager):
        self._dataset_manager: DatasetManager = dataset_manager

    def on_get(self, _: Request, resp: Response):
        resp.body = json.dumps(dict(count=self._dataset_manager.dataset_count()))
