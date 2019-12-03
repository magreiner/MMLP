import json
from datetime import datetime
from git import Commit, Repo
from pathlib import Path
from toolz import curry, partition_all, merge
from typing import Iterator, List
from uuid import UUID, uuid4

from mmlp.data import ModelVersion, Model
from mmlp.utils import ensure_no_metadata_files_present


def commit_to_version(model: Model, commit: Commit) -> ModelVersion:
    return ModelVersion.from_dict(dict(
        name=model.name,
        id=UUID(commit.hexsha[:32]),
        git_commit_id=commit.hexsha,
        model=model.id,
        author=commit.author.name,
        description=commit.message,
        created=commit.authored_datetime.isoformat()
    ))


@curry
# Note that the versions have been converted to a list by the sorted function already
def partition_versions(query: dict, versions: List[ModelVersion]) -> List[ModelVersion]:
    limit = query['limit']
    return list(partition_all(limit if limit > 0 else len(versions), versions))


@curry
def clone_and_create_model(base_dir: Path, repository_dir_name: str, metadata_filename: str,
                           metadata_frontend: dict) -> dict:
    model_id = uuid4()

    # Create generic metadata
    meta_new = dict(id=model_id,
                    created=datetime.now().isoformat(),
                    storage_path=base_dir / str(model_id),
                    code_path=base_dir / str(model_id) / repository_dir_name)

    # Clone the repository
    Repo.clone_from(metadata_frontend['source_url'], meta_new['storage_path'] / repository_dir_name)

    # Read the metadata
    meta_file_path = meta_new['storage_path'] / repository_dir_name / metadata_filename
    if meta_file_path.exists():
        with open(str(meta_file_path), 'r') as fp:
            meta_file = json.load(fp)
    # else:
    #     print("model_from_metadata: No metadata file found - skipping")

    full_metadata = merge(merge(meta_file, metadata_frontend), meta_new)

    return dict(model=Model.from_dict(full_metadata),
                current_dir=meta_new['storage_path'])


# Repository Management
########################################################################################################################
@curry
def update_repository(metadata_file_list: List, repository_dirname: str, model: Model):
    repo = Repo(model.storage_path / repository_dirname)
    checkout_master = repo.git.checkout('master')
    fetch_info = repo.remotes.origin.pull()
    last_commit = fetch_info[0].commit

    # TODO: update model metadata if model.json is present
    #  (only present if it was changed and re-created by git pull)
    ensure_no_metadata_files_present(metadata_file_list,
                                     context=dict(current_dir=model.storage_path / repository_dirname))

    return dict(id=model.id, name=model.name, version=last_commit.hexsha)


@curry
def repository_versions(repository_dirname: str, model: Model) -> Iterator[ModelVersion]:
    log = Repo(model.storage_path / repository_dirname).iter_commits('master')
    return map(lambda commit: commit_to_version(model, commit), log)
