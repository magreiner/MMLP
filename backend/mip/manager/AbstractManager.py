import logging

import falcon

from mip.utils.utils import throw_exception, max_body


class AbstractManager:
    def __init__(self, config, classname):
        self.c = config
        self.logger = logging.getLogger('backend.' + classname)

        # Endpoints (override this in your manager class)
        self.endpoint_map = {
            'ping': self.ping
        }

    def on_head(self, req, resp, command):
        self.logger.info(
            'HEAD request received at endpoint "{}", resp "{}", command "{}"'.format(req.path, resp, command))
        # Get endpoint
        endpoint = self.endpoint_map.get(command)
        if endpoint:
            # Command implemented, process request
            resp.context['result'] = endpoint()
            resp.set_header('Powered-By', 'Falcon')
            resp.status = falcon.HTTP_200
        else:
            # Command not implemented, raise issue
            throw_exception("on_head", "ERROR: Unfortunately, the command {} is not available yet.".format(command))

    def on_trace(self, req, resp, command):
        self.logger.info(
            'TRACE request received at endpoint "{}", resp "{}", command "{}"'.format(req.path, resp, command))
        # Get endpoint
        endpoint = self.endpoint_map.get(command)
        if endpoint:
            # Command implemented, process request
            resp.context['result'] = endpoint()
            resp.set_header('Powered-By', 'Falcon')
            resp.status = falcon.HTTP_200
        else:
            # Command not implemented, raise issue
            throw_exception("on_trace", "ERROR: Unfortunately, the command {} is not available yet.".format(command))

    @falcon.before(max_body(64 * 1024))
    def on_post(self, req, resp, command):
        # Get endpoint
        endpoint = self.endpoint_map.get(command)
        if endpoint:
            # Command implemented, process request
            resp.context['result'] = endpoint(req)
            resp.set_header('Powered-By', 'Falcon')
            resp.status = falcon.HTTP_200
        else:
            # Command not implemented, raise issue
            throw_exception("on_post", "ERROR: Unfortunately, the command {} is not available yet.".format(command))

    def on_delete(self, req, resp, command):
        self.logger.warning(
            'DELETE request received at endpoint "{}", resp "{}", command "{}"'.format(req.path, resp, command))
        # Get endpoint
        endpoint = self.endpoint_map.get(command)
        if endpoint:
            # Command implemented, process request
            resp.context['result'] = endpoint(req)
            resp.set_header('Powered-By', 'Falcon')
            resp.status = falcon.HTTP_200
        else:
            # Command not implemented, raise issue
            throw_exception("on_delete", "ERROR: Unfortunately, the command {} is not available yet.".format(command))

    def on_put(self, req, resp, command):
        self.logger.info(
            'PUT request received at endpoint "{}", resp "{}", command "{}"'.format(req.path, resp, command))
        # Get endpoint
        endpoint = self.endpoint_map.get(command)
        if endpoint:
            # Command implemented, process request
            resp.context['result'] = endpoint()
            resp.set_header('Powered-By', 'Falcon')
            resp.status = falcon.HTTP_200
        else:
            # Command not implemented, raise issue
            throw_exception("on_put", "ERROR: Unfortunately, the command {} is not available yet.".format(command))

    def on_get(self, req, resp, command):
        if req.path != '/monitor/status':
            self.logger.info(
                'GET request received at endpoint "{}", resp "{}", command "{}"'.format(req.path, resp, command))
        # Get endpoint
        endpoint = self.endpoint_map.get(command)
        if endpoint:
            # Command implemented, process request
            resp.context['result'] = endpoint()
            resp.set_header('Powered-By', 'Falcon')
            resp.status = falcon.HTTP_200
        else:
            # Command not implemented, raise issue
            throw_exception("on_get", "ERROR: Unfortunately, the command {} is not available yet.".format(command))

    def ping(self):
        return "pong"
