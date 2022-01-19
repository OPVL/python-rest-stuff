
import logging
import sqlite3
from time import time


class Database:
    _filename = 'app/database/vulture.db'

    def __init__(self, database: str = None) -> None:
        self._db = sqlite3.connect(database if database else self._filename)
        self._cursor = self._db.cursor()

    def table_exists(self, table: str) -> bool:
        query = f"SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{table}'"

        logging.debug(f'QUERY: {query}')
        self._cursor.execute(query)

        return self._cursor.fetchone()[0] == 1

    def _insert(self, table: str, data: dict, commit=True):
        columns = ",".join(data.keys())
        values = ",".join(f"'{value}'" for value in data.values())
        query = f'INSERT INTO {table}({columns}) VALUES({values})'

        logging.debug(f'QUERY: {query}')

        self._cursor.execute(query)

        if commit:
            self._db.commit()

        return self._cursor.lastrowid > 0

    def _insert_many(self, table: str, rows: list, commit=True):
        values = []
        for row in rows:
            values.append(
                f'''({",".join(f"'{data}'" for data in row.values())})'''
            )
        columns = ",".join(rows[0].keys())

        query = f'INSERT INTO {table} ({columns}) VALUES {",".join(values)}'

        logging.debug(f'QUERY: {query}')
        self._cursor.execute(query)

        if commit:
            self._db.commit()

        return self._cursor.rowcount == len(rows)

    def _select(self,
                table: str,
                columns: str = '*',
                where: str = None,
                order_by: str = None,
                limit: int = None,
                offset: int = None
                ):
        query = f'SELECT {columns} FROM {table};'
        if where:
            query = query.replace(';', f' {where};')
        if order_by:
            query = query.replace(';', f' ORDER BY {order_by};')
        if limit:
            query = query.replace(';', f' LIMIT {str(limit)};')
        if offset:
            query = query.replace(';', f' OFFSET {str(offset)};')

        logging.debug(f'QUERY: {query}')
        rows = self._cursor.execute(query)

        return rows

    def _create_table(self, name: str, schema: dict, safe: bool = True, commit: bool = True):
        parsed_schema = self._parse_schema(schema)
        query = f'CREATE TABLE {"IF NOT EXISTS " if safe else ""}{name} ({parsed_schema});'

        logging.debug(f'QUERY: {query}')
        self._cursor.execute(query)

        if commit:
            self._db.commit()

        return self.table_exists(name)

    def _parse_schema(self, schema: dict) -> str:
        return ', '.join(f'{key} {value}' for key, value in schema.items())

    def _drop(self, table: str, safe: bool = True, commit: bool = True):

        query = f'DROP TABLE {"IF EXISTS " if safe else ""}{table};'
        logging.debug(msg=f'QUERY: {query}')
        self._cursor.execute(query)

        if commit:
            self._db.commit()

        return not self.table_exists(table)

    def _delete(self, table: str, where: str = '', commit: bool = True):
        # delete all rows from table
        where = f'DELETE FROM {table} {where};'
        logging.debug(f'QUERY: {where}')
        self._cursor.execute(where)

        print('deleted', self._cursor.rowcount, 'records from the table.')

        if commit:
            self._db.commit()


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
    logging.basicConfig(filename='database.log',
                        level=logging.DEBUG, format='%(asctime)s %(message)s')

    database = Database(':memory:')
    table_name = 'test_insertion'
    schema = {
        'id': 'integer',
        'name': 'string'
    }
    offset = 1
    data = [
        {
            'id': 1,
            'name': 'jeffrey epstein'
        }, {
            'id': 2,
            'name': 'didnt kill himself'
        }, {
            'id': 3,
            'name': 'childish'
        },
        {
            'id': 4,
            'name': 'secure'
        }
    ]

    database._create_table(name=table_name, schema=schema)
    database._insert_many(table=table_name, rows=data)


if __name__ == '__main__':
    main()
