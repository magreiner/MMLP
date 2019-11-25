from uuid import UUID

from falcon import Request, Response, falcon
from pandas.io import json

from mmlp.data import ModelSnapshot
from mmlp.endpoint.compute.utils import transform_dataclass_to_dict
from mmlp.manager import SnapshotManager
from mmlp.utils import get_params_to_query

SORT_ATTRIBUTES = ['id', 'name', 'description', 'license', 'origin', 'maintainer', 'storage_path', 'created']


class SnapshotCollection:
    def __init__(self, snapshot_manager: SnapshotManager):
        self._snapshot_manager: SnapshotManager = snapshot_manager

    def on_get(self, req: Request, resp: Response, model_id: UUID = None, git_commit_id: str = None):
        query = get_params_to_query(req, SORT_ATTRIBUTES, 'created', 'desc')
        if model_id and git_commit_id:
            snapshots = self._snapshot_manager.list_snapshots_filtered(model_id=model_id,
                                                                       git_commit_id=git_commit_id,
                                                                       query=query)
        else:
            snapshots = self._snapshot_manager.list_snapshots(query=query)

        if isinstance(snapshots, Exception):
            resp.body = json.dumps(dict(error=str(snapshots)))
            resp.status = falcon.HTTP_500
        else:
            resp.body = f"[{','.join(map(lambda x: x.json(), snapshots))}]"
            resp.status = falcon.HTTP_201

    def on_post(self, req: Request, resp: Response):
        snap = ModelSnapshot.from_json(req.media['ModelSnapshot'])
        result = self._snapshot_manager.create_snapshot(snap)
        if isinstance(result, Exception):
            resp.body = json.dumps(dict(error=str(result)))
            resp.status = falcon.HTTP_500
        else:
            resp.body = result.json()
            resp.status = falcon.HTTP_201

    def on_delete(self, req: Request, resp: Response):
        result = self._snapshot_manager.get_snapshot(req.media['snapshot_id'])

        if not isinstance(result, Exception):
            result = self._snapshot_manager.remove_snapshot(result)

        if isinstance(result, Exception):
            resp.body = json.dumps(dict(error=str(result)))
            resp.status = falcon.HTTP_404
        else:
            resp.body = result.json()
            resp.status = falcon.HTTP_202
