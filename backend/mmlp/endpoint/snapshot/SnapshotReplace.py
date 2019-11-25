import json
from dataclasses import asdict

from falcon import Request, Response, falcon

from mmlp.data import ModelSnapshot
from mmlp.data.utils import DataclassJSONEncoder
from mmlp.manager import SnapshotManager


class SnapshotReplace:
    def __init__(self, snapshot_manager: SnapshotManager):
        self._snapshot_manager: SnapshotManager = snapshot_manager

    def on_post(self, req: Request, resp: Response):
        snap = ModelSnapshot.from_json(req.media['ModelSnapshot'])
        result = self._snapshot_manager.replace(snap)
        if isinstance(result, Exception):
            resp.body = json.dumps(dict(error=str(result)))
            resp.status = falcon.HTTP_500
        else:
            resp.body = json.dumps(asdict(result), cls=DataclassJSONEncoder)
            resp.status = falcon.HTTP_201
