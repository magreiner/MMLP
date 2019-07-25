import dataclasses
import json
from dataclasses import asdict
from datetime import datetime

from falcon import Request, Response, falcon
from uuid import uuid4

from pathlib import Path

from mip import Config
from mip.data import ModelSnapshot, Model, DatasetVersion
from mip.data.utils import DataclassJSONEncoder
from mip.endpoint.compute.utils import transform_parameter_dict
from mip.manager import ComputeManager, SnapshotManager
from mip.manager import DatasetManager
from mip.manager import ModelManager


class ComputeModelTraining:
    def __init__(self, config: Config, dataset_manager: DatasetManager, model_manager: ModelManager, compute_manager: ComputeManager, snapshot_manager: SnapshotManager):
        self._config: Config = config
        self._dataset_manager: DatasetManager = dataset_manager
        self._model_manager: ModelManager = model_manager
        self._compute_manager: ComputeManager = compute_manager
        self._snapshot_manager: SnapshotManager = snapshot_manager

    def on_post(self, req: Request, resp: Response):
        model: Model = self._model_manager.get_model(req.media['modelId'])
        dataset_version: DatasetVersion = self._dataset_manager.get_dataset_version(req.media['datasetVersionId'])

        # Validate input parameters
        if not type(model) == Model:
            resp.body = json.dumps(dict(error=str(model)))
            resp.status = falcon.HTTP_500

            return resp
        elif not type(dataset_version) == DatasetVersion:
            resp.body = json.dumps(dict(error=str(dataset_version)))
            resp.status = falcon.HTTP_500

            return resp

        snapshot_id = uuid4()
        storage_path = Path(model.storage_path) / self._config.model_snapshot_dirname / str(snapshot_id)

        parent_id = req.media.get('snapshotId', None)

        # Create snapshot
        # Start training from scratch or based on previous snapshot
        new_model_snapshot = ModelSnapshot.from_dict(dict(
            id=snapshot_id,
            model=model,
            model_git_commit=req.media['modelGitCommit'],
            dataset_version=dataset_version,
            storage_path=storage_path,
            container_name=f"snap_{snapshot_id}",
            parent_id=parent_id,
            container_archive_path=storage_path / f"container_snap_{snapshot_id}.tar.gz",
            parameters=transform_parameter_dict(req.media['parameters']['value']),
            created=str(datetime.now())
        ))

        if parent_id:
            print("Using previously trained model snapshot")
            parent_snap = self._snapshot_manager.get_snapshot(parent_id)

            # Validate user input
            if not type(parent_snap) == ModelSnapshot:
                resp.body = json.dumps(dict(error=str(parent_snap)))
                resp.status = falcon.HTTP_500

                return resp

            new_model_snapshot = dataclasses.replace(new_model_snapshot,  container_image_name=parent_snap.new_container_image_name)

        self._snapshot_manager.create_snapshot(new_model_snapshot)
        new_model_snapshot = self._compute_manager.train_model(new_model_snapshot)

        resp.body = json.dumps(asdict(new_model_snapshot), cls=DataclassJSONEncoder)
