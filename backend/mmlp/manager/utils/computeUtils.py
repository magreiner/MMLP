from __future__ import annotations

import dataclasses
import json
import tempfile
from pathlib import Path
from typing import Union

from git import Repo
from shutil import rmtree
from toolz import curry

from mmlp.data import ModelSnapshot, Result
from mmlp.manager import SnapshotManager, ResultManager
from mmlp.utils.RequestClient import RequestClient
from mmlp.utils.utils import create_directory_zip, create_directory_tar


@curry
def clone_git_repository(context: ModelSnapshot) -> ModelSnapshot:
    # code is already present in the snapshot container
    if context.parent_id:
        return context

    context = dataclasses.replace(context, code_directory=Path(tempfile.mkdtemp()))
    print(f'Training temp directory: {context.code_directory}')

    context = update_instance_status_rest(instance=context, new_status='cloning git repo')

    # Get Repo
    repo = Repo(context.model.code_path)
    repo.clone(context.code_directory)

    # Get specific version
    repo.git.checkout(context.model_git_commit)

    return context


@curry
def write_parameters_to_dir(parameters_filename: str, context: ModelSnapshot) -> ModelSnapshot:
    # code is already present in the snapshot container
    if context.parent_id:
        return context

    # Replace parameter file with custom parameter set
    print(f'write parameters to: {Path(context.code_directory) / parameters_filename}')
    with open(str(Path(context.code_directory) / parameters_filename), 'w') as fp:
        json.dump(context.parameters, fp)

    return context


@curry
def finalize_pipeline(instance: Union[ModelSnapshot, Result]) -> Union[Exception, ModelSnapshot, Result]:
    # Update status if no error occurred
    if not instance.status.lower().startswith('error'):
        instance = update_instance_status_rest(instance=instance, new_status='finished')

    # Update the instance object of the manager
    update_instance_rest(instance=instance)

    # remove preprocessed data after training
    if instance.pre_processing['pre_processing_application']:
        rmtree(instance.pre_processing['input_data_path'])

    return instance


@curry
def update_instance_status_rest(instance: Union[ModelSnapshot, Result], new_status: str) -> Union[ModelSnapshot, Result]:
    instance = dataclasses.replace(instance, status=new_status)

    return update_instance_rest(instance=instance)


@curry
def update_instance_rest(instance: Union[ModelSnapshot, Result]) -> Union[ModelSnapshot, Result]:
    # Send Request
    req_c = RequestClient()
    if type(instance) == ModelSnapshot:
        result = req_c.send_post_request("/snapshots/replace", dict(ModelSnapshot=instance))
    elif type(instance) == Result:
        result = req_c.send_post_request("/results/replace", dict(Result=instance))
    else:
        Exception(f'update_instance_rest: unknown object {instance}, type: {type(instance)}')

    return instance


@curry
def update_status(manager: Union[SnapshotManager, ResultManager], instance: Union[ModelSnapshot, Result], new_status: str) -> Union[ModelSnapshot, Result]:
    instance = dataclasses.replace(instance, status=new_status)
    instance = manager.replace(instance)

    return instance


@curry
def create_archive(context: Union[ModelSnapshot, Result]) -> Union[ModelSnapshot, Result]:
    context = update_instance_status_rest(instance=context, new_status=f'Create Archive')

    # Set archive name
    if type(context) == ModelSnapshot:
        archive_name = f"snap_{context.id}"
    elif type(context) == Result:
        archive_name = f"result_{context.id}"
    else:
        archive_name = f"custom_{context.id}"

    context = dataclasses.replace(context, archive_path=Path(context.storage_path) / f'{archive_name}.zip')

    # Update file before creating the zip file
    context = update_instance_rest(context)

    if not create_directory_zip(str(context.storage_path), archive_name):
        Exception(f"Could not create zipfile for object {archive_name}")

    return context
