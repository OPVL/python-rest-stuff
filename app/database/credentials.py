import logging
import time
from app.database.database import Database


class Credentials(Database):
    _table = 'credentials'
    _schema = {
        'service': 'string',
        'code': 'string',
        'expires': 'integer',
    }

    def __init__(self, database: str = None) -> None:
        super().__init__(database)

        if not self.table_exists(table=self._table):
            if not self._create_table(name=self._table, schema=self._schema):
                raise logging.exception(
                    'unable to create table/verify table exists')

    def insert(self, service: str, code: str, expires: int = 3600):
        self._insert(self._table, {'service': service,
                     'code': code, 'expires': int(time() + expires)})

    def all(self, valid: bool = False):
        query = f'SELECT * FROM {self._table}'

        if valid:
            query += f'WHERE expires<{int(time())}'

        self._cursor.execute(query)
        return self._cursor.fetchall()

    def refresh(self):
        self._drop(table=self._table, commit=False)
        self._create_table(name=self._table, schema=self._schema, commit=True)


def main():
    print('hello')


if __name__ == '__main__':
    main()
