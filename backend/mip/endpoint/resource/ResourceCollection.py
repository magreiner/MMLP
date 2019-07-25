import json
from dataclasses import asdict
from uuid import UUID

import falcon
from falcon import Request, Response
from toolz import map

from mip import Config
from mip.manager import ResourceManager
from mip.utils import get_params_to_query

# TODO: Limit maximum items to 500
MAX_ITEMS = 500
SORT_ATTRIBUTES = ['id', 'name', 'description', 'license', 'origin', 'maintainer', 'storage_path', 'created']


class ResourceCollection:
    def __init__(self, resource_manager: ResourceManager):
        self._resource_manager: ResourceManager = resource_manager

    def on_get(self, req: Request, resp: Response):
        monitors = self._resource_manager.monitors()
        if isinstance(monitors, Exception):
            resp.body = json.dumps(dict(error=str(monitors)))
            resp.status = falcon.HTTP_500
        else:
            resp.body = json.dumps(monitors)
            resp.status = falcon.HTTP_201

    def on_post(self, req: Request, resp: Response, snap_id: UUID):
        result = self._resource_manager.create_monitor(req.media['id'])
        if isinstance(result, Exception):
            resp.body = json.dumps(dict(error=str(result)))
            resp.status = falcon.HTTP_500
        else:
            resp.body = result.json()
            resp.status = falcon.HTTP_201

    def on_delete(self, _: Request, resp: Response, snap_id: UUID):
        result = self._resource_manager.remove_monitor(snap_id)
        if isinstance(result, Exception):
            resp.body = json.dumps(dict(error=str(result)))
            resp.status = falcon.HTTP_404
        else:
            resp.body = result.json()
            resp.status = falcon.HTTP_202

    # @staticmethod
    # def get_payload(req):
    #     try:
    #         return req.context['doc']
    #     except Exception as ex:
    #         throw_exception("get_payload", "ERROR: {}".format(repr(ex)))
