import unittest, asyncio

import py_eureka_client.logger as logger
from py_eureka_client.http_client import HttpClient, HttpRequest, HttpResponse

logger.set_level("DEBUG")


class TestEurekaServer(unittest.TestCase):
    def test_load_page(self):
        req = HttpRequest("http://keijack:qwe%40rty%21@10.0.2.16:8080/a.txt")
        client = HttpClient()
        res: HttpResponse = asyncio.run(client.urlopen(req))
        assert res.body_text == "hello!"
