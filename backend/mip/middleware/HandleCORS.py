import falcon
from falcon.http_status import HTTPStatus


class HandleCORS:
    def process_request(self, req, resp):
        # print(f"HandleCORS: {req.method}: {req.url}")
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Methods', '*')
        resp.set_header('Access-Control-Allow-Headers', '*')
        resp.set_header('Access-Control-Max-Age', 1728000)  # 20 days
        if req.method == 'OPTIONS':
            raise HTTPStatus(falcon.HTTP_200, body='\n')
