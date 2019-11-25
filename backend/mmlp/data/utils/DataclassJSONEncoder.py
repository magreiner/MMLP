import json
from datetime import datetime
from pathlib import Path, PosixPath
from uuid import UUID


class DataclassJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        # return str(f"{obj}")
        # return str(obj)
        # print(type(obj), obj)
        if isinstance(obj, datetime):
            # print(1)
            return obj.isoformat()
        elif isinstance(obj, UUID):
            # if the obj is uuid, return the value of uuid
            # print(2)
            return str(obj)
        elif isinstance(obj, Path):
            # print(3)
            return str(f"{obj}")
        elif isinstance(obj, PosixPath):
            # print(4)
            return str(obj)
        elif type(obj) == PosixPath:
            # print(5)
            return str(obj)
        # elif type(type(obj)) == ABCMeta:
        #     print(6)
        #     return json.dumps(asdict(obj), cls=DataclassJSONEncoder)
        # else:
        #     return str(obj)
        # print(7)
        return json.JSONEncoder.default(self, obj)
