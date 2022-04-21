from dataclasses import dataclass
from pathlib import Path
from typing import List

from mmlp.data.utils.AbstractEntity import AbstractEntity


@dataclass
class Config(AbstractEntity):
    platform_base_dir: Path
    dataset_base_dir: Path
    dataset_filename: str
    dataset_meta_attributes: List
    model_base_dir: Path
    model_filename: str
    model_snapshot_filename: str
    model_snapshot_dirname: str
    method_filename: str
    repository_dirname: str
    parameters_filename: str
    result_filename: str
    result_base_dir: Path
    version_filename: str
    version_meta_attributes: List
    versions_file: str
    chunk_size_bytes: int
    docker_registry_address: str
    docker_registry_username: str
    docker_registry_password: str
    email_notification_smtp_address: str
    email_notification_to: str
    email_notification_from: str
    email_notification_username: str
    email_notification_password: str
    metadata_file_list: List[str]
    push_trained_images_to_registry: bool
    backend_base_url: str

    @staticmethod
    def from_dict(  # Set docker registry credentials:
            # Default registry address: https://index.docker.io/v1
            docker_registry_address="SET_REGISTRY_ADDRESS",
            docker_registry_username="SET_USERNAME",
            docker_registry_password="SET_PASSWORD",
            # Set Email SMTP credentials:
            email_notification_smtp_address="SET_SMTP_HOST",
            email_notification_to="SET_RECEPIENT",
            email_notification_from="SomeMail@provider.com",
            email_notification_username="SET_USERNAME",
            email_notification_password="SET_PASSWORD",
            # Set IP-Address or domain name of the docker-host:
            # For https setup certificates first
            backend_base_url="http://SET_HOST:8000",

            # Advanced Settings:
            push_trained_images_to_registry=True,
            platform_base_dir=Path('/data/MMLP'),
            dataset_base_dir_name='datasets',
            dataset_filename='dataset.json',
            dataset_meta_attributes=None,
            model_base_dir_name='models',
            model_filename='model.json',
            model_snapshot_filename='snapshot.json',
            model_snapshot_dirname='snapshots',
            repository_dirname='repository',
            parameters_filename='parameters.json',
            method_filename='method.json',
            result_filename='result.json',
            result_base_dir='results',
            version_filename='version.json',
            version_meta_attributes=None,
            versions_file='versions.json',
            chunk_size_bytes=4096):

        # initialize mutable default arguments
        if dataset_meta_attributes is None:
            dataset_meta_attributes = ['name', 'description', 'license', 'origin', 'maintainer']

        if version_meta_attributes is None:
            version_meta_attributes = ['description']

        # create base directory
        Path.mkdir(platform_base_dir / dataset_base_dir_name, parents=True, exist_ok=True)
        Path.mkdir(platform_base_dir / model_base_dir_name, parents=True, exist_ok=True)
        Path.mkdir(platform_base_dir / result_base_dir, parents=True, exist_ok=True)

        # Loglevel:
        # CRITICAL	50
        # ERROR	    40
        # WARNING	30
        # INFO	    20
        # DEBUG	    10
        # NOTSET	0
        # loglevel = 10
        #
        # logging.basicConfig(level=logging.DEBUG,
        #                     format='[%(process)d, %(thread)d]: %(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        #                     datefmt='%m-%d %H:%M')

        return Config(
            platform_base_dir=platform_base_dir,
            dataset_base_dir=platform_base_dir / dataset_base_dir_name,
            dataset_filename=dataset_filename,
            dataset_meta_attributes=dataset_meta_attributes,
            model_base_dir=platform_base_dir / model_base_dir_name,
            model_filename=model_filename,
            model_snapshot_filename=model_snapshot_filename,
            model_snapshot_dirname=model_snapshot_dirname,
            repository_dirname=repository_dirname,  # source_code
            parameters_filename=parameters_filename,
            result_filename=result_filename,
            result_base_dir=platform_base_dir / result_base_dir,
            method_filename=method_filename,
            version_filename=version_filename,
            version_meta_attributes=version_meta_attributes,
            versions_file=versions_file,
            chunk_size_bytes=chunk_size_bytes,
            docker_registry_address=docker_registry_address,
            docker_registry_username=docker_registry_username,
            docker_registry_password=docker_registry_password,
            email_notification_smtp_address=email_notification_smtp_address,
            email_notification_to=email_notification_to,
            email_notification_from=email_notification_from,
            email_notification_username=email_notification_username,
            email_notification_password=email_notification_password,
            backend_base_url=backend_base_url,
            push_trained_images_to_registry=push_trained_images_to_registry,
            # parameters.json is required and should not be renamed
            metadata_file_list=[dataset_filename,
                                model_filename,
                                model_snapshot_filename,
                                version_filename,
                                method_filename]
        )
