from falcon import Request, Response, falcon
from pandas.io import json

from mmlp.manager import MethodManager


class MethodCount:
    def __init__(self, method_manager: MethodManager):
        self._method_manager: MethodManager = method_manager

    def on_get(self, req: Request, resp: Response):
        result = self._method_manager.count_methods()
        if isinstance(result, Exception):
            resp.body = json.dumps(dict(error=str(result)))
            resp.status = falcon.HTTP_500
        else:
            resp.body = json.dumps(dict(count=result))
            resp.status = falcon.HTTP_201
