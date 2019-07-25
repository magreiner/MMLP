# To use the instance return type from static methods
from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Mapping, Union, Iterator
from uuid import UUID
from uuid import uuid4

from toolz import curry, partition_all, get

from mip.Config import Config
from mip.data import Method
from mip.data import ModelSnapshot
from mip.endpoint.compute.utils import transform_dataclass_to_dict
from mip.manager.utils.utils import load_objects_from_storage
from mip.utils import ensure_uuid, excepting_pipe
from mip.utils.utils import write_json_file


class MethodManager:
    def __init__(self, config: Config, methods: Mapping[UUID, Method]):
        self._config: Config = config
        self._methods: Mapping[UUID, Method] = methods

        if hasattr(self._methods, "keys"):
            print(f'MethodManager:   Loaded {len(self._methods.keys())} methods')
        else:
            print("FATAL MethodManager: Could not load methods, sorry :(")

    @staticmethod
    def load(config: Config) -> MethodManager:
        # print(f'MethodManager: Loading models from: {config.model_base_dir}')
        return MethodManager(config=config,
                             methods=load_objects_from_storage(metadata_filename=config.method_filename,
                                                               class_factory=Method,
                                                               root_directory=config.model_base_dir))

    def create_method(self, name: str, description: str, snap: ModelSnapshot) -> Union[Exception, ModelSnapshot]:

        if (Path(snap.storage_path) / self._config.method_filename).exists():
            return Exception("create_method", "A method for this snapshot already exist.")

        # create method object
        method = Method.from_dict(dict(
            id=uuid4(),
            name=name,
            created=str(datetime.now()),
            description=description,
            model_snapshot=snap
        ))

        # Create method on filesystem
        write_json_file(str(Path(snap.storage_path) / self._config.method_filename),
                        transform_dataclass_to_dict(method))

        # add method object
        self._methods[method.id] = method

        return method

    def remove_method(self, method: Method) -> Union[Exception, Method]:
        if not self._methods.get(method.id, None):
            raise Exception("remove_method", f"Method {method.id} is not known")

        # Remove the method file from filesystem
        # Only delete the method  (snapshot is still there)!
        (Path(method.model_snapshot.storage_path) / self._config.method_filename).unlink()

        # Remove object from collection
        self._methods.pop(method.id)

        return method

    def get_method(self, method_id: UUID) -> Union[Exception, Method]:

        method = self._methods.get(ensure_uuid(method_id))
        return method if method else Exception(f'method: {method_id} not found')

    def list_methods(self, query: dict) -> Iterator[ModelSnapshot]:
        """
        List all methods
        :param query:
        :return:
        """
        return excepting_pipe(
            self._methods.values(),
            curry(sorted, key=lambda x: getattr(x, query['sortby']), reverse=query['order']),
            curry(partition_all)(query['limit'] if query['limit'] > 0 else len(self._methods.values())),
            list,
            curry(get, default=[])(query['offset'])
        )

    def count_methods(self) -> int:
        return len(self._methods)
