import logging
import multiprocessing
import requests
from multiprocessing import Process
from pandas.io import json

from mmlp.Config import Config
from mmlp.endpoint.compute.utils import transform_dataclass_to_dict


class RequestClient:
    def __init__(self):
        self._config = Config.from_dict()
        self.base_url = self._config.backend_base_url
        self.logger = logging.getLogger('backend.' + __name__)

    def send_post_request(self, relative_path, payload):
        # Check input
        if not relative_path or not payload:
            self.logger.fatal("Relative Path {} or Payload invalid.".format(relative_path, payload))
            return False

        # Prepare request
        headers = {'content-type': 'application/json'}

        # Send Request
        self.logger.info("Sending request to '{}', payload: {}".format(relative_path, payload))

        # Issue when using the standard json library with
        # data=json.dumps(transform_dataclass_to_dict(payload), cls=DataclassJSONEncoder),
        resp = requests.post("{}{}".format(self.base_url, relative_path),
                             data=json.dumps(transform_dataclass_to_dict(payload)),
                             headers=headers)

        if not resp.ok:
            return Exception(f"send_post_request FAILED: {resp.status_code}, {resp.reason}")

        return resp

    def send_post_request_process(self, relative_path, payload):
        p = Process(target=self.send_post_request,
                    args=(relative_path,
                          payload))
        p.start()

        return True

    def send_get_request(self, relative_path, payload, return_dict=None):
        # Check input
        if not relative_path or not payload:
            self.logger.fatal("Relative Path {} or Payload invalid.".format(relative_path, payload))
            return False

        # Prepare request
        headers = {'content-type': 'application/json'}

        # Send Request
        self.logger.info("Sending request to '{}', payload: {}".format(relative_path, payload))
        resp = requests.get("{}{}".format(self.base_url, relative_path),
                            data=json.dumps(transform_dataclass_to_dict(payload)),
                            headers=headers)
        return_dict["resp"] = resp

        if not resp.ok:
            return Exception(f"send_get_request FAILED: {resp.status_code}, {resp.reason}")

        return resp

    def send_get_request_process(self, relative_path, payload):
        manager = multiprocessing.Manager()
        return_dict = manager.dict()

        p = Process(target=self.send_get_request,
                    args=(relative_path,
                          payload,
                          return_dict))
        p.start()
        p.join()

        return return_dict["resp"]
