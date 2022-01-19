import logging
from unittest import TestCase

from app.database.database import Database


class DatabaseTest(TestCase):
    _database = ':memory:'

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        logging.basicConfig(
            filename='test.log',
            level=logging.DEBUG,
            format='%(asctime)s %(message)s'
        )

    def test_can_create_table(self):
        database = Database(self._database)
        table_name = 'test_creation'
        schema = {
            'id': 'integer',
            'name': 'string'
        }

        self.assertTrue(database._create_table(name=table_name, schema=schema))
        self.assertTrue(database.table_exists(table=table_name))

    def test_safe_handle_duplicate_table_creation(self):
        database = Database(self._database)
        table_name = 'test_creation'
        schema = {
            'id': 'integer',
            'name': 'string'
        }

        self.assertTrue(database._create_table(
            name=table_name, schema=schema, safe=False))
        self.assertTrue(database.table_exists(table=table_name))

        self.assertTrue(database._create_table(
            name=table_name, schema=schema, safe=True))

    def test_can_drop_table(self):
        database = Database(self._database)
        table_name = 'test_destroy'
        schema = {
            'id': 'integer',
            'name': 'string'
        }

        database._create_table(name=table_name, schema=schema)
        self.assertTrue(database.table_exists(table=table_name))

        database._drop(table=table_name, safe=False)
        self.assertFalse(database.table_exists(table=table_name))

    def test_can_safely_drop_nonexistent_table(self):
        database = Database(self._database)
        table_name = 'test_destroy_nonexistent'

        self.assertFalse(database.table_exists(table=table_name))

        database._drop(table=table_name, safe=True)

    def test_can_insert_data(self):
        database = Database(self._database)
        table_name = 'test_insertion'
        schema = {
            'id': 'integer',
            'name': 'string'
        }

        self.assertTrue(database._create_table(name=table_name, schema=schema))

        database._insert(table=table_name, data={
            'id': id(self),
            'name': table_name
        })

        rows = database._cursor.execute(f'''SELECT * FROM {table_name};''')
        row_list = rows.fetchall()

        self.assertEquals(1, rows.arraysize)
        self.assertEquals(1, database._cursor.lastrowid)

        self.assertEquals(id(self), row_list[0][0])
        self.assertEquals(table_name, row_list[0][1])

    def test_can_insert_many(self):
        database = Database(self._database)
        table_name = 'test_insertion'
        schema = {
            'id': 'integer',
            'name': 'string'
        }

        self.assertTrue(database._create_table(name=table_name, schema=schema))

        data = [
            {
                'id': 69,
                'name': 'jeffrey epstein'
            }, {
                'id': 420,
                'name': 'didnt kill himself'
            }, {
                'id': 8008135,
                'name': 'childish'
            }
        ]

        database._insert_many(table=table_name, rows=data)

        rows = database._cursor.execute(f'''SELECT * FROM {table_name};''')
        row_list = rows.fetchall()

        self.assertEquals(3, database._cursor.lastrowid)
        self.assertEquals(3, len(row_list))

        for iterator in range(0, len(row_list)):
            self.assertEquals(data[iterator]['id'], row_list[iterator][0])
            self.assertEquals(data[iterator]['name'], row_list[iterator][1])

    def test_can_get_data(self):
        database = Database(self._database)
        table_name = 'test_selection'
        schema = {
            'id': 'integer',
            'name': 'string'
        }

        self.assertTrue(database._create_table(name=table_name, schema=schema))

        database._insert(table=table_name, data={
            'id': id(self),
            'name': table_name
        })

        rows = database._select(columns='*', table=table_name)
        row_list = rows.fetchall()

        self.assertEquals(id(self), row_list[0][0])
        self.assertEquals(table_name, row_list[0][1])

    def test_can_get_data_with_condition(self):
        database = Database(self._database)
        table_name = 'test_selection'
        schema = {
            'id': 'integer',
            'name': 'string'
        }

        self.assertTrue(database._create_table(name=table_name, schema=schema))

        data = [
            {
                'id': 69,
                'name': 'jeffrey epstein'
            }, {
                'id': 420,
                'name': 'didnt kill himself'
            }, {
                'id': 8008135,
                'name': 'childish'
            }
        ]

        database._insert_many(table=table_name, rows=data)

        rows = database._select(columns='*', table=table_name,
                                where=f"WHERE id = {data[0]['id']}")
        row_list = rows.fetchall()

        self.assertEquals(1, len(row_list))
        self.assertEquals(data[0]['id'], row_list[0][0])
        self.assertEquals(data[0]['name'], row_list[0][1])

    def test_can_get_ordered_data(self):
        database = Database(self._database)
        table_name = 'test_selection'
        schema = {
            'id': 'integer',
            'name': 'string'
        }

        self.assertTrue(database._create_table(name=table_name, schema=schema))

        data = [
            {
                'id': 69,
                'name': 'jeffrey epstein'
            }, {
                'id': 420,
                'name': 'didnt kill himself'
            }, {
                'id': 8008135,
                'name': 'childish'
            }
        ]

        database._insert_many(table=table_name, rows=data)

        rows = database._select(columns='*', table=table_name,
                                order_by="id DESC")
        row_list = rows.fetchall()

        self.assertEquals(3, len(row_list))
        self.assertEquals(data[2]['id'], row_list[0][0])
        self.assertEquals(data[2]['name'], row_list[0][1])

    def test_can_get_data_with_limit(self):
        database = Database(self._database)
        table_name = 'test_selection'
        schema = {
            'id': 'integer',
            'name': 'string'
        }

        self.assertTrue(database._create_table(name=table_name, schema=schema))

        data = [
            {
                'id': 69,
                'name': 'jeffrey epstein'
            }, {
                'id': 420,
                'name': 'didnt kill himself'
            }, {
                'id': 8008135,
                'name': 'childish'
            }
        ]

        database._insert_many(table=table_name, rows=data)

        rows = database._select(columns='*', table=table_name,
                                limit=2, order_by='id ASC')
        row_list = rows.fetchall()

        self.assertEquals(2, len(row_list))

        for iterator in range(0, len(row_list)):
            self.assertEquals(data[iterator]['id'], row_list[iterator][0])
            self.assertEquals(data[iterator]['name'], row_list[iterator][1])

    def test_can_get_data_with_offset(self):
        database = Database(self._database)
        table_name = 'test_selection'
        schema = {
            'id': 'integer',
            'name': 'string'
        }
        offset = 1

        self.assertTrue(database._create_table(name=table_name, schema=schema))

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
            }
        ]

        database._insert_many(table=table_name, rows=data)

        rows = database._select(columns='*', table=table_name,
                                limit=5, offset=offset, order_by='id ASC')
        row_list = rows.fetchall()

        self.assertEquals(2, len(row_list))

        for iterator in range(offset, len(row_list)):
            self.assertEquals(data[iterator]['id'],
                              row_list[iterator - offset][0])
            self.assertEquals(data[iterator]['name'],
                              row_list[iterator - offset][1])

    def test_can_delete(self):
        database = Database(self._database)
        table_name = 'test_insertion'
        schema = {
            'id': 'integer',
            'name': 'string'
        }

        self.assertTrue(database._create_table(name=table_name, schema=schema))

        data = [
            {
                'id': 69,
                'name': 'jeffrey epstein'
            }, {
                'id': 420,
                'name': 'didnt kill himself'
            }, {
                'id': 8008135,
                'name': 'childish'
            }
        ]

        database._insert_many(table=table_name, rows=data)

        rows = database._select(table=table_name)
        row_list = rows.fetchall()
        self.assertEquals(3, len(row_list))

        database._delete(table=table_name)

        rows = database._select(table=table_name)
        row_list = rows.fetchall()
        self.assertEquals(0, len(row_list))

    def test_can_delete_with_condition(self):
        database = Database(self._database)
        table_name = 'test_insertion'
        schema = {
            'id': 'integer',
            'name': 'string'
        }

        self.assertTrue(database._create_table(name=table_name, schema=schema))

        data = [
            {
                'id': 69,
                'name': 'jeffrey epstein'
            }, {
                'id': 420,
                'name': 'didnt kill himself'
            }, {
                'id': 8008135,
                'name': 'childish'
            }
        ]

        database._insert_many(table=table_name, rows=data)
        database._delete(table=table_name, where=f"WHERE id != {data[0]['id']}")
        rows = database._select(table=table_name)
        row_list = rows.fetchall()
        self.assertEquals(1, len(row_list))

        self.assertEquals(data[0]['id'], row_list[0][0])
