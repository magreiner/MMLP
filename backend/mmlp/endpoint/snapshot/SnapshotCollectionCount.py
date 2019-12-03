from falcon import Request, Response, falcon
from pandas.io import json
from uuid import UUID

from mmlp.manager import SnapshotManager
from mmlp.utils import get_params_to_query

SORT_ATTRIBUTES = ['id', 'name', 'description', 'license', 'origin', 'maintainer', 'storage_path', 'created']


class SnapshotCollectionCount:
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
            resp.body = json.dumps(dict(count=self._snapshot_manager.snapshot_count()))
            resp.status = falcon.HTTP_201
