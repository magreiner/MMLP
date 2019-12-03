import json
from dataclasses import asdict
from falcon import Request, Response, falcon

from mmlp.data import Result
from mmlp.data.utils import DataclassJSONEncoder
from mmlp.manager import ResultManager


class ResultReplace:
    def __init__(self, result_manager: ResultManager):
        self._result_manager: ResultManager = result_manager

    def on_post(self, req: Request, resp: Response):
        result = Result.from_json(req.media['Result'])
        result = self._result_manager.replace(result)
        if isinstance(result, Exception):
            resp.body = json.dumps(dict(error=str(result)))
            resp.status = falcon.HTTP_500
        else:
            resp.body = json.dumps(asdict(result), cls=DataclassJSONEncoder)
            resp.status = falcon.HTTP_201
