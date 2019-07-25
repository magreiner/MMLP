from dataclasses import asdict

from falcon import Request, Response, falcon
import json

from mip.data import Result
from mip.data.utils import DataclassJSONEncoder
from mip.endpoint.compute.utils import transform_dataclass_to_dict
from mip.manager import ResultManager
from mip.utils import get_params_to_query

SORT_ATTRIBUTES = ['id', 'name', 'description', 'license', 'origin', 'maintainer', 'storage_path', 'created']


class ResultCollection:
    def __init__(self, result_manager: ResultManager):
        self._result_manager: ResultManager = result_manager

    def on_get(self, req: Request, resp: Response):
        query = get_params_to_query(req, SORT_ATTRIBUTES, 'created', 'desc')
        methods = self._result_manager.list_results(query=query)
        if isinstance(methods, Exception):
            resp.body = json.dumps(dict(error=str(methods)))
            resp.status = falcon.HTTP_500
        else:
            resp.body = f"[{','.join(map(lambda x: x.json(), methods))}]"
            resp.status = falcon.HTTP_201

    def on_post(self, req: Request, resp: Response):
        result = Result.from_json(req.media['Result'])
        result = self._result_manager.create_result(result)
        if isinstance(result, Exception):
            resp.body = json.dumps(dict(error=str(result)))
            resp.status = falcon.HTTP_500
        else:
            resp.body = json.dumps(asdict(result), cls=DataclassJSONEncoder)
            resp.status = falcon.HTTP_201

    def on_delete(self, req: Request, resp: Response):
        result = self._result_manager.get_result(req.media['result_id'])

        if not isinstance(result, Exception):
            result = self._result_manager.remove_result(result)

        if isinstance(result, Exception):
            resp.body = json.dumps(dict(error=str(result)))
            resp.status = falcon.HTTP_404
        else:
            resp.body = json.dumps(asdict(result), cls=DataclassJSONEncoder)
            resp.status = falcon.HTTP_202
