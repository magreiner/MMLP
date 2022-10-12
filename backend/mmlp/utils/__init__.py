import io
import json
import math
import os
import shutil
import tarfile
import tempfile
import time
from falcon import Request
from pathlib import Path
from toolz import curry, do
from toolz import excepts
from typing import Iterator, List, Union
from uuid import UUID

# Converts a string to an int safely, default is 0
safe_int = excepts(ValueError, lambda s: int(s), lambda _: 0)


def load_json(path: Path) -> dict:
    with open(str(path), 'r') as fp:
        return json.load(fp)


# Traverses a directory tree and looks for files with file name 'filename'.
# The function outputs a list of the full paths to these files.
def list_files(root_dir: Path, filename: str) -> Iterator[str]:
    return excepting_pipe(
        os.walk(str(root_dir)),
        curry(filter)(lambda _: filename in _[2]),
        curry(map)(lambda _: os.path.join(_[0], filename))
    )


# Like toolz's pipe, but returns an exception immediately when it occurs in a step of calculations:
def excepting_pipe(data, *funcs):
    for func in funcs:
        data = excepts(Exception, func, lambda _: _)(data)
        if isinstance(data, Exception):
            # Modify the error object to preserve the function name where it occurred
            # A generic error class would be better
            if hasattr(func, '__code__'):
                if hasattr(func, 'args'):
                    print(f'Exception occurred in excepting pipe function {repr(func.__code__), func.args}: {data}')
                    data.args = (f'{repr(func.__code__), func.args}: {data.args[0]}',)
                else:
                    print(f'Exception occurred in excepting pipe function {repr(func.__code__)}: {data}')
                    data.args = (f'{repr(func.__code__)}: {data.args[0]}',)
            else:
                if hasattr(func, 'args'):
                    print(f'Exception occurred in excepting pipe function {repr(func.__name__), func.args}: {data}')
                    data.args = (f'{repr(func.__name__), func.args}: {data.args[0]}',)
                else:
                    print(f'Exception occurred in excepting pipe function {repr(func.__name__)}: {data}')
                    data.args = (f'{repr(func.__name__)}: {data.args[0]}',)
            return data
    return data


# Writes the request byte stream to a unique temporary directory
def upload_to_temp_dir(req: Request, chunk_size: int = 4096, tmp_filename='data.tar.gz') -> dict:
    # Create new temp directory
    temp_dir = Path(tempfile.mkdtemp())
    tarball_path = temp_dir / tmp_filename

    # Receive archive and store archive
    with io.open(tarball_path, 'wb') as fp:
        while True:
            chunk = req.stream.read(chunk_size)
            if not chunk:
                break
            fp.write(chunk)

    # Pass temporary directory and tarball path
    return dict(temp_dir=temp_dir, tarball_path=tarball_path)


def process_multi_part_upload(req: Request) -> Union[dict, Exception]:
    print(req.params)
    if not req.params.get('id'):
        return Exception('Missing file id')

    if not req.params.get('size'):
        return Exception('Missing file size')

    if not req.params.get('offset'):
        return Exception('Missing file chunk offset')

    if not req.params.get('chunk'):
        return Exception('Missing chunk size')

    file_id = req.params.get('id')
    file_size = int(req.params.get('size'))
    chunk_offset = int(req.params.get('offset'))
    chunk_size = int(req.params.get('chunk'))
    chunk_count = math.ceil(file_size / chunk_size)
    print(f'total chunk count: {chunk_count}')
    chunk_number = int(chunk_offset / chunk_size)
    print(f'chunk number: {chunk_number}')

    part_upload_dir = Path('/tmp') / file_id
    part_upload_dir.mkdir(parents=True, exist_ok=True)

    # Store the file part
    file_part = part_upload_dir / f'part_{chunk_number:05d}'
    byte_count = 0
    start = time.time()
    with io.open(file_part, 'wb') as fp:
        while True:
            chunk = req.stream.read(chunk_size)
            byte_count += len(chunk)
            if not chunk:
                break
            fp.write(chunk)

    print(f'Read: {byte_count} bytes in {time.time() - start} s')

    # If this is the last chunk of the file, stitch all the parts together and process accordingly
    if chunk_number == chunk_count - 1:
        print(f'Total file upload is finished')
        print(f'Writing large file ...')
        complete_file_path = part_upload_dir / 'data.tar.gz'
        with io.open(complete_file_path, 'ab') as write_fp:
            for part_file in sorted(os.listdir(part_upload_dir)):
                part_file_path = part_upload_dir / part_file
                print(f'Writing part: {part_file_path}')
                with open(part_file_path, 'rb') as read_fp:
                    write_fp.write(read_fp.read())
        print(f'Finished writing')

        result = excepting_pipe(
            complete_file_path,
            move_to_temp_dir,
            curry(do)(lambda _: shutil.rmtree(part_upload_dir)),
            lambda _: _)

        # Pass temporary directory and tarball path
        return result

    # Return feedback on current progress
    return dict(id=file_id, message=f'write success', offset=chunk_offset, bytes=byte_count)


def move_to_temp_dir(path: Path, tmp_filename='data.tar.gz') -> dict:
    # Create new temp directory
    temp_dir = Path(tempfile.mkdtemp())
    tarball_path = temp_dir / tmp_filename

    os.rename(str(path), tarball_path)

    # Pass temporary directory and tarball path
    return dict(temp_dir=temp_dir, tarball_path=tarball_path)


def extract_tarball_to_temp_dir(context: dict) -> dict:
    current_dir = Path(context['temp_dir']) / 'archive'
    current_dir.mkdir()

    print(f'Temporary archive directory: {current_dir}')

    with tarfile.open(context['tarball_path'], 'r:gz') as fp:
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(fp, current_dir)

    return dict(temp_dir=context['temp_dir'], current_dir=current_dir)


@curry
def ensure_no_metadata_files_present(metadata_file_list: List[str], context: dict) -> dict:
    current_dir = context['current_dir']

    for filename in metadata_file_list:
        # Search for metadata file recursively
        filename_list = excepting_pipe(
            os.walk(str(current_dir)),
            curry(filter)(lambda _: filename in _[2]),
            curry(map)(lambda _: os.path.join(_[0], filename))
        )

        # rename file
        for file in filename_list:
            print(f"Renaming metadata file {file}.")
            Path(file).rename(f'{file}.orig')

    return context


def get_params_to_query(req: Request, sort_attributes: List[str], default_sort_attribute: str,
                        default_order: str) -> dict:
    sortby = req.params.get('sortby', default_sort_attribute)
    return dict(
        limit=safe_int(req.params.get('limit', 0)),
        offset=safe_int(req.params.get('offset', 0)),
        sortby=sortby if sortby in sort_attributes else default_sort_attribute,
        order=True if req.params.get('order', default_order) == 'desc' else False
    )


def ensure_uuid(uuid):
    return uuid if type(uuid) == UUID else UUID(uuid)
