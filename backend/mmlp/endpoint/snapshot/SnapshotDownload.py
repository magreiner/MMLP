import falcon
import io
import json
import os
from pathlib import Path
from uuid import UUID

from mmlp.manager import SnapshotManager


class SnapshotDownload:
    def __init__(self, snapshot_manager: SnapshotManager):
        self._snapshot_manager: SnapshotManager = snapshot_manager

    def on_get(self, req, resp, snapshot_id: UUID):
        snap = self._snapshot_manager.get_snapshot(snapshot_id)

        if isinstance(snap, Exception):
            resp.body = json.dumps(dict(error=str(snap)))
            resp.status = falcon.HTTP_500
        else:
            file_path = snap.archive_path
            if str(file_path) == str(Path("")):
                resp.body = json.dumps(dict(error=f"Archive for snapshot {snapshot_id} not available."))
                resp.status = falcon.HTTP_500
            else:
                # file_path = Path(__file__).parent.parent.parent.parent / 'tests' / 'resources' / 'Task04_Hippocampus.tar.gz'
                # file_path = Path(__file__).parent.parent.parent / 'tests' / 'resources' / 'Task04_Hippocampus.tar.gz'
                # This is a Falcon shortcut for the Content-Disposition header
                resp.content_type = 'application/gzip'
                resp.set_stream(io.open(str(file_path), 'rb'), os.path.getsize(str(file_path)))
                resp.downloadable_as = Path(file_path).name
                resp.status = falcon.HTTP_201
