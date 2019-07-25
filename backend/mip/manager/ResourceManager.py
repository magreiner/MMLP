from collections import Mapping
from uuid import UUID, uuid4

import GPUtil
import psutil

from mip.data import ModelSnapshot
from mip.manager import DockerManager
from mip.utils.utils import throw_exception, update_json_file, read_json_file


class ResourceManager:
    def __init__(self, config):
        self._d = DockerManager(config)
        self._active_monitors: Mapping[UUID, dict] = {}
        for mon in self._d.active_pipelines():
            self._active_monitors[uuid4()] = dict(status="unknown",
                                                  name=mon)

    def create_monitor(self, snap: ModelSnapshot, context: dict):
        if self._active_monitors.get(snap.id, None):
            throw_exception("create_monitor", f"Monitor for {snap.id} is already known")

        self._active_monitors[snap.id] = dict(snapshot=snap)

        return snap

    def remove_monitor(self, snap: ModelSnapshot, context: dict):
        if not self._active_monitors.get(snap.id, None):
            throw_exception("remove_monitor", f"Monitor for {snap.id} is not known")

        self._active_monitors.pop(snap.id)

        return snap

    def monitors(self):
        if len(GPUtil.getGPUs()) > 0:
            gpu_usage = round(GPUtil.getGPUs()[0].load * 100, 2)
            gpu_memory = round(GPUtil.getGPUs()[0].memoryUtil * 100, 2)
            gpu_temperature = round(GPUtil.getGPUs()[0].temperature, 2)
        else:
            gpu_usage = -1
            gpu_memory = -1
            gpu_temperature = -1

        return {'cpu': psutil.cpu_percent(),
                'memory': psutil.virtual_memory()._asdict()['percent'],
                'disk': psutil.disk_usage('/')._asdict()['percent'],
                'gpu_usage': gpu_usage,
                'gpu_memory': gpu_memory,
                'gpu_temperature': gpu_temperature,
                'running_experiments': self._active_monitors
                }

    # def extract_experiment_input(self, payload):
    #     exp_info = self.get_payload(payload)
    #
    #     # Extract experiment name
    #     exp_name = exp_info.keys()
    #
    #     # Only one experiment should be updated per request (since each experiment runs in a separate process)
    #     if len(exp_name) != 1:
    #         throw_exception("extract_experiment_input", "ERROR: Multiple experiments can not be updated at the same time ({})".format(exp_name))
    #
    #     exp_name = next(iter(exp_name))
    #
    #     return exp_name, exp_info[exp_name]
    #
    #
    # def remove_experiment_monitor(self, payload):
    #     exp_name, exp_info = self.extract_experiment_input(payload)
    #
    #     if not self.experiment_state.get(exp_name, None):
    #         throw_exception("remove_experiment_monitor", "ERROR: Remove Experiment Monitor: {} is not known".format(exp_name))
    #
    #     self.experiment_state.pop(exp_name)
    #     self.logger.info("Removed Experiment {}".format(exp_name))
    #
    #     return True
    #
    # def update_experiment_status(self, payload):
    #     exp_name, exp_info = self.extract_experiment_input(payload)
    #
    #     # Extract experiment status
    #     exp_status = exp_info.get('status', None)
    #
    #     if not exp_status:
    #         throw_exception("update_experiment_status", "ERROR: Could not read the new exp status ({})".format(exp_name))
    #
    #     # Update storage
    #     if not self.experiment_state.get(exp_name, None):
    #         throw_exception("update_experiment_status", "ERROR: Update Experiment Monitor: {} is not known to the monitor. "
    #                                                     "Forgot to create it?".format(exp_name))
    #
    #     # Store information in the metadata file
    #     if exp_info.get("filepath"):
    #         if exp_info['progressCode']:
    #             update_json_file(exp_info["filepath"], "experimentProgress", exp_info['progressCode'])
    #         else:
    #             self.logger.fatal("No internal Status provided for {}".format(exp_name))
    #
    #     # TODO: Save Status history?
    #     self.logger.info("Update Status of experiment {} from {} to {}".format(exp_name,
    #                                                                            self.experiment_state[exp_name]['status'],
    #                                                                            exp_status))
    #     self.experiment_state[exp_name]['status'] = exp_status
    #
    #     return True
    #
    # def get_experiment_status(self, payload):
    #     exp_name, _ = self.extract_experiment_input(payload)
    #     return self.experiment_state[exp_name]
    #
    # def get_running_experiments(self):
    #     return self.experiment_state


