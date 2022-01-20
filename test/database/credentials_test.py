import logging
from time import time
from unittest import TestCase

from app.database.credentials import Credentials


class CredentialsTest(TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        logging.basicConfig(
            filename='test.log',
            level=logging.DEBUG,
            format='%(asctime)s %(message)s'
        )
        self.credentials = Credentials(':memory:')

    def test_automatically_creates_credentials_table(self):
        self.credentials.table_exists(self.credentials._table)

    def test_can_get_all_credentials(self):
        rows = [{
            'service': 'test-service-1',
            'code': 'this-is-valid',
            'expires': 12345
        }, {
            'service': 'test-service-2',
            'code': 'this-also-valid',
            'expires': 6789
        }]
        self.credentials._insert_many(table=self.credentials._table, rows=rows)

        result = self.credentials.all()

        self.assertEquals(len(rows), len(result))

    def test_can_get_only_valid_credentials(self):
        rows = [{
            'service': 'test-service-1',
            'code': 'this-is-valid',
            'expires': time() + 3600
        }, {
            'service': 'test-service-2',
            'code': 'this-also-valid',
            'expires': 6789
        }]
        self.credentials._insert_many(table=self.credentials._table, rows=rows)

        result = self.credentials.all(valid=True)

        self.assertEquals(1, len(result))
        self.assertEquals(rows[0]['service'], result[0][1])

    def test_can_insert_credentials(self):
        service = 'test-service'
        code = 'oauth-code'
        self.credentials.insert(service, code, 3600)

        result = self.credentials.all()

        self.assertEquals(1, len(result))
        self.assertEquals(service, result[0][1])
        self.assertEquals(code, result[0][2])

    def test_can_refresh_credentials_table(self):
        service = 'test-service'
        code = 'oauth-code'
        self.credentials.insert(service, code, 3600)

        self.credentials.refresh()

        result = self.credentials.all()

        self.assertEquals(0, len(result))

    def test_can_get_credentials(self):
        service = 'test-service'
        code = 'oauth-code'
        self.credentials.insert(service, code, 3600)

        rows = self.credentials.get(service)

        self.assertEquals(service, rows[0][1])
