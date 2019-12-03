import json
import shutil
from dataclasses import asdict
from datetime import datetime
from falcon import Request, Response, falcon
from pathlib import Path
from uuid import uuid4

from mmlp.Config import Config
from mmlp.data import Method, Result
from mmlp.data.utils import DataclassJSONEncoder
from mmlp.manager import ComputeManager, ResultManager, MethodManager


class ComputeMethodApplication:
    def __init__(self, config: Config, method_manager: MethodManager, compute_manager: ComputeManager,
                 result_manager: ResultManager):
        self._config: Config = config
        self._method_manager: MethodManager = method_manager
        self._compute_manager: ComputeManager = compute_manager
        self._result_manager: ResultManager = result_manager

    def on_post(self, req: Request, resp: Response):
        method: Method = self._method_manager.get_method(req.media['method_id'])

        # Validate input parameters
        if not type(method) == Method:
            resp.body = json.dumps(dict(error=str(method)))
            resp.status = falcon.HTTP_500

            return resp

        # Prepare result
        result_id = uuid4()
        storage_path = Path(self._config.platform_base_dir) / self._config.result_base_dir / str(result_id)
        patient_cohort_path = Path(req.media['patient_cohort_location']['current_dir'])
        # '/data/MMLP/datasets/8a3ed58a-28e8-4064-88be-1100f6bb56ad/1fd169e4-c988-4d0d-a803-a3c39d5aedd6')

        result = Result.from_dict(dict(
            id=result_id,
            method=method,
            storage_path=storage_path,
            input_data_path=storage_path / 'patient_cohort',
            container_name=f"result_{result_id}",
            success=False,
            running=False,
            issuer=req.media['issuer'],
            created=str(datetime.now()),
        ))

        result = self._result_manager.create_result(result)

        # move patient cohort to result path
        # shutil.copytree(patient_cohort_path, storage_path / 'patient_cohort')
        shutil.move(patient_cohort_path, str(result.input_data_path))

        # Start training from scratch or based on previous snapshot
        result = self._compute_manager.apply_method(result=result)

        resp.body = json.dumps(asdict(result), cls=DataclassJSONEncoder)
