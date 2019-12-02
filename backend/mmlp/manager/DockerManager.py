import dataclasses
import json
import time
from pathlib import Path
from typing import Union

import docker
from toolz import curry, excepts

from mmlp import Config
from mmlp.data import ModelSnapshot, Result
from mmlp.manager.utils.computeUtils import update_instance_status_rest
from mmlp.utils.utils import write_to_file, get_timestamp, remove_ansi_escape_tags, write_json_file, \
    send_email

CONTAINER_RUNNING_STATUSES = ["created", "running"]


class DockerManager:
    def __init__(self, config: Config):
        self._config: Config = config
        self._d = docker.from_env()
        self._d_low = docker.APIClient()
        self._con = self._d.containers

        # Login to docker registry using the provided credentials from the config
        self.login = self._d.login(username=self._config.docker_registry_username,
                                   password=self._config.docker_registry_password,
                                   reauth=False)


    @curry
    def build_container_context(self, context: ModelSnapshot) -> ModelSnapshot:
        # container must be re-used
        if context.parent_id:
            return context

        context = update_instance_status_rest(instance=context, new_status='Building Container')

        log_container_build = "Started: {}\n".format(get_timestamp())
        container_image, build_logs = self._d.images.build(path=str(context.code_directory),
                                                           rm=False,
                                                           tag=context.container_image_name)

        # Convert log generator object to string
        last_key = ""
        for log_dict in build_logs:
            for key in log_dict.keys():
                if last_key == key:
                    log_container_build += "\t{}".format(log_dict[key])
                else:
                    last_key = key
                    log_container_build += "{}\t{}\n".format(key, log_dict[key])

        context = dataclasses.replace(context, container_image_id=container_image.id)
        context = dataclasses.replace(context, container_build_logs=log_container_build)

        return context

    @curry
    def run_container_context(self, context: Union[ModelSnapshot, Result]) -> Union[ModelSnapshot, Result]:
        # check if container is already running
        if self.get_container(context.container_name):
            Exception(f"Container '{context.container_name}' is already running. Nothing more to do.")

            return context
        else:
            context = update_instance_status_rest(instance=context, new_status=f'Running')

            container_id = self._con.run(image=context.container_image_name,
                                         name=context.container_name,
                                         environment=context.container_environment_variables,
                                         auto_remove=False,
                                         volumes=context.container_mount_volumes,
                                         ports=context.container_ports,
                                         shm_size="2G",
                                         detach=True)

        return dataclasses.replace(context, container_id=container_id.id)

    @curry
    def pull_container_context(self, context: Union[ModelSnapshot, Result]) -> Union[ModelSnapshot, Result]:
        context = update_instance_status_rest(instance=context, new_status=f'Pull Model-Container from Registry')

        log_container_pull = "Started: {}\n".format(get_timestamp())

        # Catch the exception if the image is not found (image will be build later)
        # log_container_pull += excepts(NotFound,

        # For debugging ignore errors from the registry and continue
        # TODO: Apply error handling
        log_container_pull += excepts(Exception,
                                      lambda image: self._d_low.pull(image),
                                      lambda _: 'image not present')(context.container_image_name)

        return dataclasses.replace(context, container_pull_logs=log_container_pull)

    @curry
    def push_container_context(self, context: ModelSnapshot) -> ModelSnapshot:
        context = update_instance_status_rest(instance=context, new_status=f'Push Model-Container to Registry')
        logs = self._d_low.push(context.container_image_name)

        return dataclasses.replace(context, container_push_logs=logs)

    @curry
    def push_container_trained_image_context(self, context: ModelSnapshot) -> ModelSnapshot:
        if self._config.push_trained_images_to_registry:
            context = update_instance_status_rest(instance=context,
                                                  new_status=f'Push Trained ModelSnapshot to Registry')

            i = self._d.images.get(context.new_container_image_name)
            new_image_tag = f"{self._config.docker_registry_address}{context.new_container_image_name}"

            # create new tag
            i.tag(new_image_tag)

            # reload image
            i.reload()

            # push image
            logs = self._d_low.push(new_image_tag)

            # Save new image tag as default
            context = dataclasses.replace(context, new_container_image_name=new_image_tag)

            merged_logs = f'{context.container_push_logs}\n\nPush new trained model Image:\n{logs}'

            # TODO: include in email
            context = dataclasses.replace(context, container_push_logs=merged_logs)

            # Write Push log
            write_to_file(Path(context.storage_path) / f"Container_Push_Trained_Model_{get_timestamp(date_format='filename')}.log", logs)

        return context

    @curry
    def monitor_wait_container_execution_apply(self, context: Result) -> Result:
        container_statistics = []
        log_container_running = ""

        # Get Container Object
        running_container = self._d.containers.get(context.container_id)

        # Wait for termination and collect performance statistics
        while running_container.status in CONTAINER_RUNNING_STATUSES:
            # Collect stats
            container_statistics += [running_container.stats(stream=False)]
            time.sleep(5)

            # Reload container data
            running_container.reload()

        context = dataclasses.replace(context, container_performance_statistics=container_statistics)

        # Container exited, check if success or failure
        container_info = dict()
        container_info["start_time"] = running_container.attrs["State"]["StartedAt"]
        container_info["end_time"] = running_container.attrs["State"]["FinishedAt"]
        container_info["exit_code"] = running_container.attrs["State"]["ExitCode"]
        container_info["exit_message"] = running_container.attrs["State"]["Error"]
        container_info["OOMKilled"] = running_container.attrs["State"]["OOMKilled"]
        container_info["Dead"] = running_container.attrs["State"]["Dead"]

        if container_info["OOMKilled"]:
            container_info["exit_message"] = "OOMKilled {}".format(container_info["exit_message"])
        elif container_info["Dead"]:
            container_info["exit_message"] = "Dead {}".format(container_info["exit_message"])

        context = dataclasses.replace(context, container_info=container_info)

        # Preserve the logs
        log_container_pull = context.container_pull_logs

        log_container_prepare = f"Pull Log: \n{log_container_pull}"

        # if pre processing was performed, add the logs to the email
        if context.container_pre_processing_logs:
            log_container_prepare += f"\nPre-processing Log: {context.container_pre_processing_logs}"

        # Write Build log
        write_to_file(Path(context.storage_path) / f"Container_Pull_{get_timestamp(date_format='filename')}.log", log_container_prepare)

        log_container_running += "Result: {}\n".format(True if container_info["exit_code"] == 0 else False)
        if container_info["exit_code"] != 0 and container_info["exit_message"]:
            log_container_running += "Errormessage: {}\n".format(container_info["exit_message"])
        log_container_running += "Started: {}\n".format(container_info["start_time"])
        log_container_running += "Finished: {}\n\nOutput:\n\n".format(container_info["end_time"])
        log_container_running += running_container.logs(timestamps=True).decode("utf-8")

        context = dataclasses.replace(context, container_run_logs=running_container.logs(timestamps=True).decode("utf-8"))

        # Write runtime log to disk
        write_to_file(Path(context.storage_path) / f"Container_Output_{get_timestamp(date_format='filename')}.log",
                      remove_ansi_escape_tags(log_container_running))

        # Write performance statistics to file
        write_json_file(filename=Path(context.storage_path) / f"Container_Performance_statistics.json", content=container_statistics)

        # Always true for eval purpose
        if container_info["exit_code"] == 0:
            # if container_info["exit_code"] == 0 or True:
            context = dataclasses.replace(context, success=True)
            if not context.container_image_name.startswith('mon_'):

                # Send Email to inform user
                send_email(self._config.notification_email_to,
                           subject=f"Successful Method Analysis Pipeline: {context.id}",
                           body="Congratulations!\n"
                                "Your method application pipeline succeeded\n"
                                "Check the attached logs for further details.\n",
                           attachments=[{
                               "Filename": f"Container-Pull_{context.container_name}_{get_timestamp(date_format='filename')}.log",
                               "Content": log_container_prepare
                           }, {
                               "Filename": f"Container-Output_{context.container_name}_{get_timestamp(date_format='filename')}.log",
                               "Content": remove_ansi_escape_tags(log_container_running)
                           }, {
                               "Filename": f"Container-PerformanceStatistics_{context.container_name}_{get_timestamp(date_format='filename')}.json",
                               "Content": json.dumps(container_statistics)
                           }

                           ])
        else:
            context = dataclasses.replace(context, success=False)
            send_email(self._config.notification_email_to,
                       subject=f"Failed Method Analysis Pipeline: {context.container_name}",
                       body="Unfortunately, your method analysis pipeline failed.\n"
                            "Check the attached logs to solve the issues.\n"
                            "If you have questions, please ask your administrator.",
                       attachments=[{
                           "Filename": f"Container-Pull_{context.container_name}_{get_timestamp(date_format='filename')}.log",
                           "Content": log_container_prepare
                       }, {
                           "Filename": f"Container-Output_{context.container_name}_{get_timestamp(date_format='filename')}.log",
                           "Content": remove_ansi_escape_tags(log_container_running)
                       }
                       ])
        return context

    @curry
    def monitor_wait_container_execution_train(self, context: ModelSnapshot) -> ModelSnapshot:
        container_statistics = []
        log_container_running = ""

        # Get Container Object
        running_container = self._d.containers.get(context.container_id)

        # Wait for termination and collect performance statistics
        while running_container.status in CONTAINER_RUNNING_STATUSES:
            # Collect stats
            container_statistics += [running_container.stats(stream=False)]
            time.sleep(10)

            # Reload container data
            running_container.reload()

        context = dataclasses.replace(context, container_performance_statistics=container_statistics)

        # Container exited, check if success or failure
        container_info = dict()
        container_info["start_time"] = running_container.attrs["State"]["StartedAt"]
        container_info["end_time"] = running_container.attrs["State"]["FinishedAt"]
        container_info["exit_code"] = running_container.attrs["State"]["ExitCode"]
        container_info["exit_message"] = running_container.attrs["State"]["Error"]
        container_info["OOMKilled"] = running_container.attrs["State"]["OOMKilled"]
        container_info["Dead"] = running_container.attrs["State"]["Dead"]

        if container_info["OOMKilled"]:
            container_info["exit_message"] = "OOMKilled {}".format(container_info["exit_message"])
        elif container_info["Dead"]:
            container_info["exit_message"] = "Dead {}".format(container_info["exit_message"])

        context = dataclasses.replace(context, container_info=container_info)

        # Preserve the logs
        log_container_build = context.container_build_logs
        log_container_pull = context.container_pull_logs

        log_container_push = f"Started: {get_timestamp()}\n"
        log_container_push += context.container_push_logs

        log_container_prepare = f"Pull Log: \n{log_container_pull}\nBuild Log:\n{log_container_build}\nPush Log:\n{log_container_push}"

        # if pre processing was performed, add the logs to the email
        if context.container_pre_processing_logs:
            log_container_prepare += f"\nPre-processing Log: {context.container_pre_processing_logs}"

        # Write Build log
        write_to_file(Path(context.storage_path) / f"Container_Build_{get_timestamp(date_format='filename')}.log", log_container_prepare)

        log_container_running += "Result: {}\n".format(True if container_info["exit_code"] == 0 else False)
        if container_info["exit_code"] != 0 and container_info["exit_message"]:
            log_container_running += "Errormessage: {}\n".format(container_info["exit_message"])
        log_container_running += "Started: {}\n".format(container_info["start_time"])
        log_container_running += "Finished: {}\n\nOutput:\n\n".format(container_info["end_time"])
        log_container_running += running_container.logs(timestamps=True).decode("utf-8")

        context = dataclasses.replace(context, container_run_logs=running_container.logs(timestamps=True).decode("utf-8"))

        # Write runtime log to disk
        write_to_file(Path(context.storage_path) / f"Container_Output_{get_timestamp(date_format='filename')}.log",
                      remove_ansi_escape_tags(log_container_running))

        # Write performance statistics to file
        write_json_file(filename=Path(context.storage_path) / f"Container_Performance_statistics.json", content=container_statistics)

        # Always true for eval purpose
        if container_info["exit_code"] == 0:
        # if container_info["exit_code"] == 0 or True:
            context = dataclasses.replace(context, success=True)
            if not context.container_image_name.startswith('mon_'):

                # Send Email to inform user
                send_email(self._config.notification_email_to,
                           subject=f"Successful Model Training Pipeline: {context.id}",
                           body="Congratulations!\n"
                                "Your model training pipeline succeeded\n"
                                "Check the attached logs for further details.\n",
                           attachments=[{
                               "Filename": f"Container-Build_{context.container_name}_{get_timestamp(date_format='filename')}.log",
                               "Content": log_container_prepare
                           }, {
                               "Filename": f"Container-Output_{context.container_name}_{get_timestamp(date_format='filename')}.log",
                               "Content": remove_ansi_escape_tags(log_container_running)
                           }, {
                               "Filename": f"Container-PerformanceStatistics_{context.container_name}_{get_timestamp(date_format='filename')}.json",
                               "Content": json.dumps(container_statistics)
                           }

                           ])
        else:
            context = dataclasses.replace(context, success=False)
            send_email(self._config.notification_email_to,
                       subject=f"Failed Model Training Pipeline: {context.container_name}",
                       body="Unfortunately, your training pipeline failed.\n"
                            "Check the attached logs to solve the issues.\n"
                            "If you have questions, please ask your administrator.",
                       attachments=[{
                           "Filename": f"Container-Build_{context.container_name}_{get_timestamp(date_format='filename')}.log",
                           "Content": log_container_prepare
                       }, {
                           "Filename": f"Container-Output_{context.container_name}_{get_timestamp(date_format='filename')}.log",
                           "Content": remove_ansi_escape_tags(log_container_running)
                       }
                       ])
        return context

    @curry
    def save_container_state(self, context: Union[ModelSnapshot, Result]):
        # Create archive of container
        if context.success:
            context = update_instance_status_rest(instance=context, new_status=f'Export Container State')

            # commit container state
            container = self._d.containers.get(context.container_id)
            new_container_image_name = f'snap_{context.id}'
            container.commit(repository=new_container_image_name,
                             tag=f'latest',
                             message=f"MMLP: trained model snapshot",
                             author=f"Matthias Greiner")

            # save the new container name
            context = dataclasses.replace(context, new_container_image_name=new_container_image_name)
        else:
            # Prevent methods with broken snapshots from producing errors (debugging)
            context = dataclasses.replace(context, new_container_image_name=context.container_image_name)

        return context

    @curry
    def archive_and_remove_container(self, context: Union[ModelSnapshot, Result]):
        # Create archive of container
        context = update_instance_status_rest(instance=context, new_status=f'Export Container Filesystem')
        container = self._d.containers.get(context.container_id)

        # Export full filesystem
        # data_stream = container.export()

        # Export specific path
        data_stream = container.get_archive('/data')[0]

        # Write archive file
        f = open(str(context.container_archive_path), "wb")
        for x in data_stream:
            f.write(x)

        # Cleanup
        # Remove the stopped container
        self.remove_container(str(context.id))

        return context

    def active_pipelines(self):
        result = []
        for container in self.list_running_containers():
            if container.name.startswith("train_") or container.name.startswith("apply_"):
                result += [container]

        return result

    def build_container(self, code_directory: Path, container_image_name: str, container_image_registry: str = "mattg"):
        image, logs = self._d.images.build(path=str(code_directory),
                                           rm=False,
                                           tag=f"{container_image_registry}/{container_image_name}")

        return dict(image=image, logs=logs)

    def pull_container(self, container_image_registry: str, container_image_name: str):
        logs = self._d_low.pull("{}{}".format(container_image_registry, container_image_name))

        return logs

    def push_container(self, container_image_registry: str, container_image_name: str):
        logs = self._d_low.push("{}/{}".format(container_image_registry, container_image_name))

        return logs

    @curry
    def perform_pre_processing_context(self, context: Union[ModelSnapshot, Result]) -> Union[Exception, ModelSnapshot, Result]:
        if context.pre_processing.get('pre_processing_application', False):
            context = update_instance_status_rest(instance=context, new_status=f'Pre-Processing Input Data')

            # Pull pre processing container
            container_pre_processing_logs = "Preprocessing Container Pull Log: \n"
            container_pre_processing_logs += self.pull_container(container_image_registry="", container_image_name=context.pre_processing['pre_processing_container_image_name'])

            # Run pre processing container
            pre_container = self.run_container(
                container_image_name=context.pre_processing['pre_processing_container_image_name'],
                container_name=context.pre_processing['pre_processing_container_name'],
                container_autoremove=False,
                mount_volumes=context.pre_processing['container_mount_volumes']
            )

            # Wait for termination
            while pre_container.status in CONTAINER_RUNNING_STATUSES:

                time.sleep(10)

                # Reload container data
                pre_container.reload()

            # Container exited, check if success or failure
            container_info = dict()
            container_info["start_time"] = pre_container.attrs["State"]["StartedAt"]
            container_info["end_time"] = pre_container.attrs["State"]["FinishedAt"]
            container_info["exit_code"] = pre_container.attrs["State"]["ExitCode"]
            container_info["exit_message"] = pre_container.attrs["State"]["Error"]
            container_info["OOMKilled"] = pre_container.attrs["State"]["OOMKilled"]
            container_info["Dead"] = pre_container.attrs["State"]["Dead"]

            container_pre_processing_logs += "\nResult: {}\n".format(True if container_info["exit_code"] == 0 else False)
            if container_info["exit_code"] != 0 and container_info["exit_message"]:
                container_pre_processing_logs += "Errormessage: {}\n".format(container_info["exit_message"])
            container_pre_processing_logs += "Started: {}\n".format(container_info["start_time"])
            container_pre_processing_logs += "Finished: {}\n\nOutput:\n\n".format(container_info["end_time"])
            container_pre_processing_logs += pre_container.logs(timestamps=True).decode("utf-8")

            # Write runtime log to disk
            write_to_file(Path(context.storage_path) / f"Pre_processing_Output_{get_timestamp(date_format='filename')}.log",
                          remove_ansi_escape_tags(container_pre_processing_logs))

            context = dataclasses.replace(context, container_pre_processing_logs=container_pre_processing_logs)

            # remove pre-processing container
            self.remove_container(container_name=context.pre_processing['pre_processing_container_name'])
        return context

    def run_container(self,
                      container_image_name: str,
                      container_name: str,
                      environment_variables=None,
                      container_autoremove: bool = False,
                      mount_volumes=None,
                      ports=None
                      ):

        # Set mutable default parameters
        if ports is None:
            ports = {}
        if mount_volumes is None:
            mount_volumes = {}
        if environment_variables is None:
            environment_variables = {}

        # check if container is already running
        if self.get_container(container_name):
            print(f"Container '{container_name}' is already running. Nothing more to do.")

            return Exception(f"Container '{container_name}' is already running. Nothing more to do.")
        else:
            container_id = self._con.run(image=container_image_name,
                                         name=container_name,
                                         environment=environment_variables,
                                         auto_remove=container_autoremove,
                                         volumes=mount_volumes,
                                         ports=ports,
                                         shm_size="2G",
                                         detach=True)

        return container_id

    def list_running_containers(self):
        return self._d.containers.list(all=True)

    def get_container(self, container_name):
        con_list = self._d.containers.list(all=True, filters={"name": container_name})
        if con_list:
            return con_list[0]
        else:
            return con_list

    def remove_container(self, container_name: str):
        if not container_name:
            # raise ValueError("Please provide a valid docker container name to remove it")
            raise ValueError('Error: Please provide a valid docker container name')

        container = self.get_container(container_name)
        if not container:
            raise ValueError(f'Error: could not find container {container_name}')

        print(f"Removing container {container.name}")
        return container.remove(force=True)
