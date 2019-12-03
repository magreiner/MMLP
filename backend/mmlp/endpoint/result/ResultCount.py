import json
from falcon import Request, Response

from mmlp.manager import ResultManager


class ResultCount:
    def __init__(self, result_manager: ResultManager):
        self._result_manager: ResultManager = result_manager

    def on_get(self, _: Request, resp: Response):
        resp.body = json.dumps(dict(count=self._result_manager.result_count()))
