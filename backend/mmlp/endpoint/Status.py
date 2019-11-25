import json


# from dataclasses import asdict
# from mmlp import data


class Status:
    def __init__(self):
        pass

    @staticmethod
    def on_get(req, resp):
        # m = data.Method('Segmentation', 2)
        status = {'name': 'MethodX', 'status': 'running'}
        resp.body = json.dumps(status, ensure_ascii=False)
