# To use the instance return type from static methods
from __future__ import annotations

import json
import shutil
from typing import Iterator, Mapping, Union
from uuid import UUID

from falcon import Request
from git import Repo
from toolz import get, partition_all, curry, assoc, dissoc, do

from mmlp.Config import Config
from mmlp.data import Model, ModelVersion
from mmlp.manager.utils.modelUtils import repository_versions, partition_versions, \
    update_repository, clone_and_create_model
from mmlp.manager.utils.utils import load_objects_from_storage
from mmlp.utils import excepting_pipe, ensure_no_metadata_files_present, ensure_uuid


class ModelManager:
    def __init__(self, config: Config, models: Mapping[UUID, Model]):
        self._config: Config = config
        self._models: Mapping[UUID, Model] = models

        # Validate Models
        if hasattr(self._models, "keys"):
            print(f'ModelManager:    Loaded {len(self._models.keys())} models')
        else:
            print("FATAL ModelManager: Could not load models, sorry :(")

    @staticmethod
    def load(config: Config) -> ModelManager:
        print(f'ModelManager:    Loading models from: {config.model_base_dir}')
        return ModelManager(config=config,
                            models=load_objects_from_storage(metadata_filename=config.model_filename,
                                                             class_factory=Model,
                                                             root_directory=config.model_base_dir))

    # Returns a list of Model objects
    # def models(self, limit: int = 0, offset: int = 0, sortby: str = 'created', order: bool = False) -> Iterator[Model]:
    def models(self, query) -> Iterator[Model]:
        """
        List all models
        :param limit:
        :param offset:
        :param sortby:
        :param order:
        :return:
        """
        return excepting_pipe(
            self._models.values(),
            curry(sorted, key=lambda ds: getattr(ds, query['sortby']), reverse=query['order']),
            curry(partition_all)(query['limit'] if query['limit'] > 0 else len(self._models.values())),
            list,
            curry(get, default=[])(query['offset']),
        )

    # Returns a model by id
    def get_model(self, model_id: UUID) -> Union[str, Model]:
        """
        Return a model or an error if it is not found by id
        :param model_id:
        :return:
        """
        model = self._models.get(ensure_uuid(model_id))
        return model if model else Exception(f'model: {model_id} not found')

    @curry
    def store_model(self, model_filename: str, context: dict) -> Model:
        model = context['model']

        # Serialize model metadata
        with open(str(model.storage_path / model_filename), 'w') as fp:
            fp.write(model.json())

        return model

    @curry
    def load_model(self, model: Model) -> Model:
        self._models = assoc(self._models, model.id, model)
        # self._models[model.id] = model
        return model

    def import_model(self, req: Request) -> Union[Exception, Model]:
        return excepting_pipe(
            json.load(req.stream),
            clone_and_create_model(self._config.model_base_dir, self._config.repository_dirname,
                                   self._config.model_filename),
            ensure_no_metadata_files_present(self._config.metadata_file_list),
            ModelManager.store_model(self, self._config.model_filename),
            ModelManager.load_model(self)
        )

    # How many datasets do we have
    def model_count(self):
        return len(self._models)

    # Transform all log commits of the repository to model versions
    def versions(self, model_id: UUID, query: dict) -> Iterator[ModelVersion]:
        """
        Lists all versions of a given modek
        :param model_id:
        :param query:
        :return:
        """
        return excepting_pipe(
            ensure_uuid(model_id),
            self._models.get,
            repository_versions(self._config.repository_dirname),
            curry(sorted, key=lambda ds: getattr(ds, query['sortby']), reverse=query['order']),
            partition_versions(query),
            curry(get, default=[])(query['offset'])
        )

    def update_model(self, model_id: UUID) -> Union[Exception, str]:
        return excepting_pipe(
            ensure_uuid(model_id),
            self._models.get,
            update_repository(self._config.metadata_file_list, self._config.repository_dirname)
        )

    def model_version_count(self, model_id: UUID) -> Union[Exception, int]:
        return excepting_pipe(
            ensure_uuid(model_id),
            self._models.get,
            repository_versions(self._config.repository_dirname),
            list,
            len
        )

    def model_version_parameters(self, model_id: UUID, git_commit_id: str) -> Union[Exception, dict]:
        return excepting_pipe(
            self._models,
            curry(get)(ensure_uuid(model_id)),
            lambda model: Repo(model.storage_path / self._config.repository_dirname),
            lambda repo: repo.git.show(f'{git_commit_id}:{self._config.parameters_filename}'),
            lambda content: json.loads(content)
        )

    # Unload model from data manager
    def unload_model(self, model: Model) -> Model:
        self._models = dissoc(self._models, model.id)
        return model

    def delete_model(self, model_id: UUID) -> Union[Exception, Model]:
        return excepting_pipe(
            ensure_uuid(model_id),
            self.get_model,

            # Remove complete model directory
            curry(do)(lambda model: shutil.rmtree(model.storage_path)),

            # Unload model from data manager
            self.unload_model
        )
