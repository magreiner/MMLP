import json
import io
import os
from uuid import UUID
import tempfile
from pathlib import Path

import falcon

from mmlp.manager import ResultManager


class ResultDownload:
    def __init__(self, result_manager: ResultManager):
        self._result_manager: ResultManager = result_manager

    def on_get(self, req, resp, result_id: UUID):
        result = self._result_manager.get_result(result_id)

        if isinstance(result, Exception):
            resp.body = json.dumps(dict(error=str(result)))
            resp.status = falcon.HTTP_500
        else:
            file_path = result.archive_path
            if str(file_path) == str(Path("")):
                resp.body = json.dumps(dict(error=f"Archive for result {result_id} not available."))
                resp.status = falcon.HTTP_500
            else:
                # file_path = Path(__file__).parent.parent.parent.parent / 'tests' / 'resources' / 'Task04_Hippocampus.tar.gz'
                # file_path = Path(__file__).parent.parent.parent / 'tests' / 'resources' / 'Task04_Hippocampus.tar.gz'
                # This is a Falcon shortcut for the Content-Disposition header
                resp.content_type = 'application/gzip'
                resp.set_stream(io.open(str(file_path), 'rb'), os.path.getsize(str(file_path)))
                resp.downloadable_as = Path(file_path).name
                resp.status = falcon.HTTP_201
