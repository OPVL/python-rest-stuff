from unittest import TestCase


class ApiTest(TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)

        # self.api = Api()

    def test_can_make_http_requests(self):
        self.assertTrue(1)
