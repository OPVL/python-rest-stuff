import logging
from time import time
from src.database.database import Database


class Credentials(Database):
    _table = 'credentials'

    _schema = {
        'id': 'integer PRIMARY KEY AUTOINCREMENT',
        'service': 'string',
        'code': 'string',
        'expires': 'integer',
    }

    def __init__(self, database: str = None) -> None:
        super().__init__(database)

        if not self._create_table(name=self._table, schema=self._schema):
            raise logging.exception(
                'unable to create table/verify table exists')

    def insert(self, service: str, code: str, expires: int = 3600) -> bool:
        return self._insert(self._table, {
            'service': service,
            'code': code,
            'expires': int(time() + expires)
        })

    def all(self, columns: str = '*', valid: bool = False) -> list:
        if valid:
            where = f'WHERE expires > {int(time())}'
        else:
            where = None

        select_cursor = self._select(table=self._table, columns=columns,
                                     where=where, order_by='expires ASC')

        return select_cursor.fetchall()

    def get(self, service: str, valid: bool = True, columns: str = '*', limit: int = None, offset: int = None) -> list:
        where = f"""WHERE service = '{service}'"""

        if valid:
            where += f' AND expires > {int(time())}'

        select_cursor = self._select(table=self._table, columns=columns,
                                     where=where, order_by='expires DESC',
                                     limit=limit, offset=offset)

        return select_cursor.fetchall()

    def refresh(self) -> bool:
        self._drop(table=self._table, commit=False)
        return self._create_table(name=self._table, schema=self._schema, commit=True)


def main() -> None:
    store = Credentials(':memory:')
    store.insert('test-service', 'valid_code')
    credentials = store.all()

    print(credentials)


if __name__ == '__main__':
    main()
