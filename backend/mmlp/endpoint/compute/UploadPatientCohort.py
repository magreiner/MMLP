import json

import falcon
from falcon import Request, Response

from mmlp.Config import Config
from mmlp.data.utils import DataclassJSONEncoder
from mmlp.utils import extract_tarball_to_temp_dir, excepting_pipe, process_multi_part_upload


class UploadPatientCohort:
    def __init__(self, config: Config):
        self._config: Config = config

    def on_post(self, req: Request, resp: Response):
        result = process_multi_part_upload(req)

        if isinstance(result, Exception):
            resp.body = json.dumps(dict(error=str(result)))
            resp.status = falcon.HTTP_500
        elif isinstance(result, dict):
            if result.get('temp_dir', False):
                result = excepting_pipe(
                    result,
                    extract_tarball_to_temp_dir
                )
                if isinstance(result, Exception):
                    resp.body = json.dumps(dict(error=str(result)))
                    resp.status = falcon.HTTP_500
                else:
                    resp.body = json.dumps(result, cls=DataclassJSONEncoder)
                    resp.status = falcon.HTTP_201
            else:
                resp.body = json.dumps(result)
                resp.status = falcon.HTTP_200


