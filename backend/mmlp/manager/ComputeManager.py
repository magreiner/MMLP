from __future__ import annotations

import dataclasses
import os
import tempfile
from multiprocessing import Process
from pathlib import Path
from shutil import copytree
from typing import Union

from mmlp.Config import Config
from mmlp.data import ModelSnapshot
from mmlp.data.Result import Result
from mmlp.manager import SnapshotManager, ResultManager
from mmlp.manager.DockerManager import DockerManager
from mmlp.manager.utils.computeUtils import clone_git_repository, write_parameters_to_dir, \
    update_status, create_archive, finalize_pipeline
from mmlp.manager.utils.utils import slimline_dict
from mmlp.utils import excepting_pipe


class ComputeManager:
    def __init__(self, config: Config, snapshot_manager: SnapshotManager, result_manager: ResultManager):
        self._config: Config = config
        self._docker: DockerManager = DockerManager(config=config)
        self._snapshot_manager: SnapshotManager = snapshot_manager
        self._result_manager: ResultManager = result_manager
        self._running_monitoring_processes = {}

        # if hasattr(self._results, "keys"):
        #     print(f'ComputeManager: Loaded {len(self._results.keys())} results')
        # else:
        #     print("FATAL ComputeManager: Could not load results, sorry :(")

    @staticmethod
    def load(config, snapshot_manager: SnapshotManager, result_manager: ResultManager) -> ComputeManager:
        # print(f'ComputeManager: Loading results from: {config.compute_result_dir}')
        return ComputeManager(config=config,
                              snapshot_manager=snapshot_manager,
                              result_manager=result_manager)

    def apply_method(self, result: Result) -> Union[Exception, Result]:
        # TODO: Rudimentary verification

        # Build environment container
        #############################
        # Prepare volumes for the method container
        result = update_status(manager=self._result_manager, instance=result, new_status='Prepare Method Application')

        # Prepare Pre-processing
        # Settings are loaded from snapshot, but new tmp dirs used
        pre_processing = slimline_dict(result.method.model_snapshot.pre_processing)
        if pre_processing.get('pre_processing_application', False):
            pre_processing['pre_processing_container_name'] = f"pre_processing_method_{result.id}"
            pre_processing['input_data_path'] = result.input_data_path
            pre_processing['container_mount_volumes'] = {
                str(pre_processing['input_data_path']): {
                    "bind": os.path.join(os.sep, "data", "dataset"),
                    "mode": "rw"
                }
            }

            result = dataclasses.replace(result, pre_processing=pre_processing)

        # Post processing not yet implemented
        # post_processing = slimline_dict(snap.parameters['post_processing'])

        result = dataclasses.replace(result, container_mount_volumes={
            str(result.input_data_path): {
                "bind": os.path.join(os.sep, "data", "dataset"),
                "mode": "ro"
            }
        })

        # Prepare Environment Variables (same as used for snapshot)
        environment_variables = slimline_dict(result.method.model_snapshot.parameters['hyper_parameters'])

        # Run in inference mode
        environment_variables["INFERENCE"] = True

        result = dataclasses.replace(result, container_environment_variables=environment_variables)

        # Start application
        # Create and start Process
        p = Process(target=excepting_pipe,
                    name=f"Monitor_for_{result.container_image_name}",
                    args=(result,
                          self._docker.pull_container_context,
                          self._docker.perform_pre_processing_context,
                          self._docker.run_container_context,
                          self._docker.monitor_wait_container_execution_apply,
                          self._docker.archive_and_remove_container,
                          create_archive,
                          finalize_pipeline))

        self._running_monitoring_processes[result.container_image_name] = p
        # self.logger.info("New Running Containers: {}".format(self.running_containers))

        p.start()

        return result

    def train_model(self, snap: ModelSnapshot) -> Union[Exception, ModelSnapshot]:
        # TODO: Rudimentary verification

        # Build environment container
        #############################
        # Prepare volumes for the experiment container
        snap = update_status(manager=self._snapshot_manager, instance=snap, new_status='Prepare Training')

        # Preprocessing
        pre_processing_tmp = slimline_dict(snap.parameters.get('pre_processing', {}))
        pre_processing = {}
        for pre_processing_container_name, pre_processing_application in pre_processing_tmp.items():
            if pre_processing.get('container_image_name'):
                print("Warning: Currently only one preprocessing container supported")
                break

            # Create preprocesing pipeline
            pre_processing['pre_processing_container_image_name'] = \
                f"{self._config.docker_registry_address}{pre_processing_container_name}"
            pre_processing['pre_processing_container_name'] = f"pre_processing_snap_{snap.id}"
            pre_processing['pre_processing_application'] = pre_processing_application
            pre_processing['input_data_path'] = Path(tempfile.mkdtemp()) / "dataset"
            pre_processing['container_mount_volumes'] = {
                str(pre_processing['input_data_path']): {
                    "bind": os.path.join(os.sep, "data", "dataset"),
                    "mode": "rw"
                }
            }

            # copy dataset to tmp location
            copytree(str(snap.input_data_path), f"{pre_processing['input_data_path']}")

            snap = dataclasses.replace(snap, input_data_path=pre_processing['input_data_path'])
            snap = dataclasses.replace(snap, pre_processing=pre_processing)

        # Post processing not yet implemented
        # post_processing = slimline_dict(snap.parameters['post_processing'])

        # Mount Dataset
        snap = dataclasses.replace(snap, container_mount_volumes={
            str(snap.input_data_path): {
                "bind": os.path.join(os.sep, "data", "dataset"),
                "mode": "ro"
            }
        })

        # Prepare Environment Variable
        environment_variables = slimline_dict(snap.parameters['hyper_parameters'])
        snap = dataclasses.replace(snap, container_environment_variables=environment_variables)

        # Ports on Training Container
        snap = dataclasses.replace(snap, container_ports={})

        # ensure monitoring services for training are running
        # monitoring_services = snap.parameters['monitoring']
        # for service in monitoring_services:
        #     # Ports to expose from monitoring service
        #     ports = {}
        #     ports[] = service['port']
        #
        # Start monitoring service
        if snap.parameters.get('monitoring', False):
            ports = {'{}/tcp'.format(snap.parameters['monitoring']['port']): snap.parameters['monitoring']['port']}
            self._docker.run_container(container_image_name=f"{self._config.docker_registry_address}{snap.parameters['monitoring']['container']}",
                                       container_autoremove=True,
                                       container_name=f"mon_{snap.parameters['monitoring']['name']}",
                                       ports=ports)

        # Start training
        # Create and start Process
        p = Process(target=excepting_pipe,
                    name=f"Monitor_for_{snap.container_image_name}",
                    args=(snap,
                          clone_git_repository,
                          write_parameters_to_dir(self._config.parameters_filename),
                          self._docker.pull_container_context,
                          self._docker.build_container_context,
                          self._docker.push_container_context,
                          self._docker.perform_pre_processing_context,
                          self._docker.run_container_context,
                          self._docker.monitor_wait_container_execution_train,
                          self._docker.save_container_state,
                          self._docker.push_container_trained_image_context,
                          self._docker.archive_and_remove_container,
                          create_archive,
                          finalize_pipeline))

        self._running_monitoring_processes[snap.container_image_name] = p
        # self.logger.info("New Running Containers: {}".format(self.running_containers))

        p.start()

        return snap
