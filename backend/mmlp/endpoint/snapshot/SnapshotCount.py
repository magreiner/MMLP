import json
from falcon import Request, Response, falcon

from mmlp.manager import SnapshotManager


class SnapshotCount:
    def __init__(self, snapshot_manager: SnapshotManager):
        self._snapshot_manager: SnapshotManager = snapshot_manager

    def on_get(self, _: Request, resp: Response):
        resp.body = json.dumps(dict(count=self._snapshot_manager.snapshot_count()))
        resp.status = falcon.HTTP_201
