from falcon import Request, Response, falcon
from pandas.io import json

from mip.data import ModelSnapshot, Method
from mip.manager import MethodManager, SnapshotManager
from mip.utils import get_params_to_query

SORT_ATTRIBUTES = ['id', 'name', 'description', 'license', 'origin', 'maintainer', 'storage_path', 'created']


class MethodCollection:
    def __init__(self, method_manager: MethodManager, snapshot_manager: SnapshotManager):
        self._method_manager: MethodManager = method_manager
        self._snapshot_manager: SnapshotManager = snapshot_manager

    def on_get(self, req: Request, resp: Response):
        query = get_params_to_query(req, SORT_ATTRIBUTES, 'created', 'desc')
        methods = self._method_manager.list_methods(query=query)
        if isinstance(methods, Exception):
            resp.body = json.dumps(dict(error=str(methods)))
            resp.status = falcon.HTTP_500
        else:
            resp.body = f"[{','.join(map(lambda x: x.json(), methods))}]"
            resp.status = falcon.HTTP_201

    def on_post(self, req: Request, resp: Response):
        snapshot = self._snapshot_manager.get_snapshot(req.media['model_snapshot_id'])

        if not type(snapshot) == ModelSnapshot:
            resp.body = json.dumps(dict(error=str(snapshot)))
            resp.status = falcon.HTTP_500

            return resp

        result = self._method_manager.create_method(name=req.media['name'],
                                                    description=req.media['description'],
                                                    snap=snapshot)
        if isinstance(result, Exception):
            resp.body = json.dumps(dict(error=str(result)))
            resp.status = falcon.HTTP_500
        else:
            resp.body = result.json()
            resp.status = falcon.HTTP_201

    def on_delete(self, req: Request, resp: Response):
        result = self._method_manager.get_method(req.media['method_id'])

        if not type(result) == Method:
            resp.body = json.dumps(dict(error=str(result)))
            resp.status = falcon.HTTP_500

            return resp

        result = self._method_manager.remove_method(result)
        if isinstance(result, Exception):
            resp.body = json.dumps(dict(error=str(result)))
            resp.status = falcon.HTTP_404
        else:
            resp.body = result.json()
            resp.status = falcon.HTTP_202
