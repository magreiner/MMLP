# append mmlp component source dir
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Falcon imports
import ssl
from wsgiref import simple_server
import falcon
from mmlp.middleware import HandleCORS

# Config
from mmlp.Config import Config
from mmlp.SSLConfig import SSLConfig

# Managers
from mmlp.manager import DatasetManager
from mmlp.manager import SnapshotManager
from mmlp.manager import MethodManager
from mmlp.manager import ResultManager
from mmlp.manager import ModelManager
from mmlp.manager import ComputeManager
from mmlp.manager import ResourceManager

# Endpoints
###############################################################################
# Data Sets
from mmlp.endpoint.dataset import DatasetCollection
from mmlp.endpoint.dataset import DatasetCount
from mmlp.endpoint.dataset import DatasetItem
from mmlp.endpoint.dataset import DatasetVersionCollection
from mmlp.endpoint.dataset import DatasetVersionCount
from mmlp.endpoint.dataset import DatasetVersionItem

# Models
from mmlp.endpoint.model import ModelCollection
from mmlp.endpoint.model import ModelCount
from mmlp.endpoint.model import ModelItem
from mmlp.endpoint.model import ModelUpdate
from mmlp.endpoint.model import ModelVersionCollection
from mmlp.endpoint.model import ModelVersionCount
from mmlp.endpoint.model import ModelVersionParameters

# Snapshots
from mmlp.endpoint.snapshot import SnapshotCollection, SnapshotReplace, SnapshotDownload, SnapshotCollectionCount
from mmlp.endpoint.snapshot import SnapshotCount

# Methods
from mmlp.endpoint.methods import MethodCollection
from mmlp.endpoint.methods import MethodCount

# Compute
from mmlp.endpoint.compute import ComputeModelTraining, UploadPatientCohort
from mmlp.endpoint.compute import ComputeMethodApplication

# Results
from mmlp.endpoint.result import ResultCollection, ResultReplace
from mmlp.endpoint.result import ResultDownload
from mmlp.endpoint.result import ResultCount

# Resources
from mmlp.endpoint.resource import ResourceCollection


# Useful for debugging problems in your API; works with pdb.set_trace(). You
# can also use Gunicorn to host your app. Gunicorn can be configured to
# auto-restart workers when it detects a code change, and it also works
# with pdb.

def create_api(config: Config):
    # Configure WSGI server to load "api.app" (app is a WSGI callable)
    api = falcon.API(middleware=[
        HandleCORS(),
        # CustomMiddleware(),
    ])

    # Datasets
    dataset_manager = DatasetManager.load(config=config)
    api.add_route('/datasets', DatasetCollection(dataset_manager=dataset_manager))
    api.add_route('/datasets/count', DatasetCount(dataset_manager=dataset_manager))
    api.add_route('/datasets/{dataset_id:uuid}', DatasetItem(dataset_manager=dataset_manager))
    api.add_route('/datasets/{dataset_id:uuid}/versions', DatasetVersionCollection(dataset_manager=dataset_manager))
    api.add_route('/datasets/{dataset_id:uuid}/versions/count', DatasetVersionCount(dataset_manager=dataset_manager))
    api.add_route('/datasets/{dataset_id:uuid}/versions/{version_id:uuid}', DatasetVersionItem(dataset_manager=dataset_manager))

    # Models
    model_manager = ModelManager.load(config=config)
    api.add_route('/models', ModelCollection(model_manager=model_manager))
    api.add_route('/models/count', ModelCount(model_manager=model_manager))
    api.add_route('/models/{model_id:uuid}', ModelItem(model_manager=model_manager))
    api.add_route('/models/{model_id:uuid}/update', ModelUpdate(model_manager=model_manager))
    api.add_route('/models/{model_id:uuid}/versions', ModelVersionCollection(model_manager=model_manager))
    api.add_route('/models/{model_id:uuid}/versions/count', ModelVersionCount(model_manager=model_manager))
    api.add_route('/models/{model_id:uuid}/versions/{git_commit_id}/parameters', ModelVersionParameters(model_manager=model_manager))

    # Model Snapshots
    snapshot_manager = SnapshotManager.load(config=config)
    api.add_route('/snapshots', SnapshotCollection(snapshot_manager=snapshot_manager))
    api.add_route('/snapshots/count', SnapshotCount(snapshot_manager=snapshot_manager))
    api.add_route('/snapshots/replace', SnapshotReplace(snapshot_manager=snapshot_manager))
    api.add_route('/snapshots/{model_id:uuid}/commit/{git_commit_id}', SnapshotCollection(snapshot_manager=snapshot_manager))
    api.add_route('/snapshots/{model_id:uuid}/commit/{git_commit_id}/count', SnapshotCollectionCount(snapshot_manager=snapshot_manager))
    # api.add_route('/snapshots/{snapshot_id:uuid}/download', SnapshotDownload(snapshot_manager=snapshot_manager))
    api.add_route('/snapshot/{snapshot_id:uuid}/download', SnapshotDownload(snapshot_manager=snapshot_manager))

    # Methods
    method_manager = MethodManager.load(config=config)
    api.add_route('/methods', MethodCollection(method_manager=method_manager,
                                               snapshot_manager=snapshot_manager))
    api.add_route('/methods/count', MethodCount(method_manager=method_manager))

    # Results
    result_manager = ResultManager.load(config)
    api.add_route('/results', ResultCollection(result_manager=result_manager))
    api.add_route('/results/count', ResultCount(result_manager=result_manager))
    api.add_route('/results/replace', ResultReplace(result_manager=result_manager))
    api.add_route('/results/{result_id:uuid}/download', ResultDownload(result_manager=result_manager))

    # Compute Environment
    compute_manager = ComputeManager.load(config=config, snapshot_manager=snapshot_manager, result_manager=result_manager)
    api.add_route('/compute/train', ComputeModelTraining(config=config,
                                                         dataset_manager=dataset_manager,
                                                         model_manager=model_manager,
                                                         compute_manager=compute_manager,
                                                         snapshot_manager=snapshot_manager))
    api.add_route('/compute/apply', ComputeMethodApplication(config=config,
                                                             method_manager=method_manager,
                                                             compute_manager=compute_manager,
                                                             result_manager=result_manager))
    api.add_route('/compute/uploadPatientCohort', UploadPatientCohort(config=config))

    # Resource Monitor
    resource_manager = ResourceManager(config)
    api.add_route('/resources', ResourceCollection(resource_manager=resource_manager))

    return api


def main(server_address: str = '0.0.0.0',
         server_port: int = 8000,
         https: bool = True,
         ssl_config: SSLConfig = SSLConfig(False, './cert/cert.pem', './cert/privkey.pem', './cert/fullchain.pem')):

    # Generate config and API
    config = Config.from_dict()
    api = create_api(config=config)

    # Check permissions or run as sudo as workaround
    # hostname = socket.gethostname()
    # if os.geteuid() != 0 and hostname != 'some-host':
    #     # os.execvp() replaces running process, (not just launching a child)
    #     logging.warning("need sudo for chown permissions, restarting myself")
    #     os.execvp("sudo", ["sudo"] + ["/usr/bin/python3"] + sys.argv)

    # Check permissions
    try:
        # os.chown(config.experiment_dir, 1000, 1000)
        # os.chown(config.patient_cohort_dir, 1000, 1000)
        # os.chown(config.method_dir, 1000, 1000)
        pass
    except Exception as ex:
        print("Permission issues, please rerun with sudo or fix permissions manually: {}".format(repr(ex)))
    else:
        if https:
            httpd = simple_server.make_server(server_address, server_port, api)
            httpd.socket = ssl.wrap_socket(
                httpd.socket,
                server_side=ssl_config.server_side,
                certfile=ssl_config.certfile,
                keyfile=ssl_config.keyfile,
                ca_certs=ssl_config.ca_certs
            )
            httpd.serve_forever()
        else:
            # gunicorn -b 0.0.0.0:8080 -b [::1]:8000 --reload api:app
            httpd = simple_server.make_server(server_address, server_port, api)
            httpd.serve_forever()


if __name__ == '__main__':
    main(https=False)
