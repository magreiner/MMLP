from __future__ import annotations

import dataclasses
import shutil
from pathlib import Path
from toolz import get, partition_all, curry
from typing import Mapping, Union, Iterator
from uuid import UUID

from mmlp.Config import Config
from mmlp.data import Result
from mmlp.endpoint.compute.utils import transform_dataclass_to_dict
from mmlp.manager.utils.utils import load_objects_from_storage
from mmlp.utils import excepting_pipe, ensure_uuid
from mmlp.utils.utils import write_json_file


class ResultManager:
    def __init__(self, config: Config, results: Mapping[UUID, Result]):
        self._config: Config = config
        self._results: Mapping[UUID, Result] = results

        if hasattr(self._results, "keys"):
            print(f'ResultManager:   Loaded {len(self._results.keys())} results')
        else:
            print("FATAL ResultManager: Could not load results, sorry :(")

    @staticmethod
    def load(config: Config) -> ResultManager:

        print(f'ResultManager:   Loading results from: {config.result_base_dir}')
        return ResultManager(config=config,
                             results=load_objects_from_storage(metadata_filename=config.result_filename,
                                                               class_factory=Result,
                                                               root_directory=config.result_base_dir))

    def create_result(self, result: Result) -> Union[Exception, Result]:
        if self._results.get(result.id, None):
            raise Exception("create_result", f"Result with ID {result.id} is already known")

        # Create result on filesystem
        storage_path = self._config.platform_base_dir / self._config.result_base_dir / str(result.id)
        Path(storage_path).mkdir(parents=True)
        result = dataclasses.replace(result, storage_path=storage_path)

        write_json_file(str(storage_path / self._config.result_filename), transform_dataclass_to_dict(result))

        # add result object
        self._results[result.id] = result

        return result

    def replace(self, result: Result):
        if not self._results.get(result.id, None):
            raise Exception("replace_result", f"Result with ID {result.id} is not known")

        # Write changes to file
        write_json_file(str(result.storage_path / self._config.result_filename), transform_dataclass_to_dict(result))

        # Replace result object
        self._results.pop(result.id)
        self._results[result.id] = result

        return result

    def remove_result(self, result: Result) -> Union[Exception, Result]:
        if not self._results.get(result.id, None):
            raise Exception("remove_result", f"Result {result.id} is not known")

        # Remove the method file from filesystem
        shutil.rmtree(result.storage_path)

        # Remove object from collection
        self._results.pop(result.id)

        return result

    def get_result(self, result_id: UUID) -> Union[Exception, Result]:

        result = self._results.get(ensure_uuid(result_id))
        return result if result else Exception(f'Result: {result_id} not found')

    def list_results(self, query: dict) -> Iterator[Result]:
        """
        List all list_results
        :param query:
        :return:
        """
        return excepting_pipe(
            self._results.values(),
            curry(sorted, key=lambda x: getattr(x, query['sortby']), reverse=query['order']),
            curry(partition_all)(query['limit'] if query['limit'] > 0 else len(self._results.values())),
            list,
            curry(get, default=[])(query['offset'])
        )

    def result_count(self) -> int:
        return len(self._results)
