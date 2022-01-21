import logging
from src.database.database import Database


class Quotes(Database):
    _table = 'quotes'

    _schema = {
        'id': 'integer PRIMARY KEY AUTOINCREMENT',
        'author': 'string',
        'quote': 'string',
    }

    def __init__(self, database: str = None) -> None:
        super().__init__(database)

        if not self._create_table(name=self._table, schema=self._schema):
            raise logging.exception(
                'unable to create table/verify table exists')

    def insert(self, author: str, quote: str) -> bool:
        return self._insert(self._table, {
            'author': author,
            'quote': quote,
        })

    def all(self, columns: str = '*') -> list:

        select_cursor = self._select(
            table=self._table, columns=columns, order_by='id ASC')

        return select_cursor.fetchall()

    def get(self, where: str = None, columns: str = '*', limit: int = None, offset: int = None) -> list:

        select_cursor = self._select(table=self._table, columns=columns,
                                     where=where, order_by='id DESC',
                                     limit=limit, offset=offset)

        return select_cursor.fetchall()

    def first(self, where: str = None, columns: str = '*', offset: int = None) -> list:
        select_cursor = self._select(table=self._table, columns=columns,
                                     where=where, order_by='id DESC',
                                     limit=1, offset=offset)

        quote = select_cursor.fetchall()

        if not quote:
            return None

        return quote[0]

    def update(self, id: int, data=dict) -> bool:
        return id == self._update(table=self._table, where=f'id = {id}', data=data)

    def delete(self, id) -> bool:
        return 1 == self._delete(self._table, f'WHERE id = {id}')

    def refresh(self) -> bool:
        self._drop(table=self._table, commit=False)
        return self._create_table(name=self._table, schema=self._schema, commit=True)


ai_quotes = [
    {
        "author": "Kevin Kelly",
        "quote": "The business plans of the next 10,000 startups are easy to forecast: " +
                 "Take X and add AI."
    },
    {
        "author": "Stephen Hawking",
        "quote": "The development of full artificial intelligence could " +
                 "spell the end of the human race…. " +
                 "It would take off on its own, and re-design " +
                 "itself at an ever increasing rate. " +
                 "Humans, who are limited by slow biological evolution, " +
                 "couldnt compete, and would be superseded."
    },
    {
        "author": "Claude Shannon",
        "quote": "I visualize a time when we will be to robots what " +
                 "dogs are to humans, " +
                 "and Im rooting for the machines."
    },
    {
        "author": "Elon Musk",
        "quote": "The pace of progress in artificial intelligence " +
                 "(Im not referring to narrow AI) " +
                 "is incredibly fast. Unless you have direct " +
                 "exposure to groups like Deepmind, " +
                 "you have no idea how fast—it is growing " +
                 "at a pace close to exponential. " +
                 "The risk of something seriously dangerous " +
                 "happening is in the five-year timeframe." +
                 "10 years at most."

    },
    {
        "author": "Geoffrey Hinton",
        "quote": "I have always been convinced that the only way " +
                 "to get artificial intelligence to work " +
                 "is to do the computation in a way similar to the human brain. " +
                 "That is the goal I have been pursuing. We are making progress, " +
                 "though we still have lots to learn about " +
                 "how the brain actually works."
    },
    {
        "author": "Pedro Domingos",
        "quote": "People worry that computers will " +
                 "get too smart and take over the world, " +
                 "but the real problem is that theyre too stupid " +
                 "and theyve already taken over the world."
    },
    {
        "author": "Alan Turing",
        "quote": "It seems probable that once the machine thinking " +
                 "method had started, it would not take long " +
                 "to outstrip our feeble powers… " +
                 "They would be able to converse " +
                 "with each other to sharpen their wits. " +
                 "At some stage therefore, we should " +
                 "have to expect the machines to take control."
    },
    {
        "author": "Ray Kurzweil",
        "quote": "Artificial intelligence will reach " +
                 "human levels by around 2029. " +
                 "Follow that out further to, say, 2045, " +
                 "we will have multiplied the intelligence, " +
                 "the human biological machine intelligence " +
                 "of our civilization a billion-fold."
    },
    {
        "author": "Sebastian Thrun",
        "quote": "Nobody phrases it this way, but I think " +
                 "that artificial intelligence " +
                 "is almost a humanities discipline. Its really an attempt " +
                 "to understand human intelligence and human cognition."
    },
    {
        "author": "Andrew Ng",
        "quote": "Were making this analogy that AI is the new electricity." +
                 "Electricity transformed industries: agriculture, " +
                 "transportation, communication, manufacturing."
    }
]


def main() -> None:
    store = Quotes()
    store.refresh()
    store._insert_many(store._table, ai_quotes)
    quotes = store.first()

    print(quotes)


if __name__ == '__main__':
    main()
