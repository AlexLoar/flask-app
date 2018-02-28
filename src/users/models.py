from os.path import abspath, dirname, join
from datetime import date as dt

import pony.orm as pony
from pony.orm.ormtypes import date

basedir = abspath(dirname(dirname(dirname(__file__))))
PONY_DATABASE_URI = join(basedir, 'users.db')

database = pony.Database(
    "sqlite",
    PONY_DATABASE_URI,
    create_db=True
)


class User(database.Entity):
    username = pony.Required(str, unique=True)
    email = pony.Required(str, 40, unique=True)
    age = pony.Required(int, min=1, max=99)
    phone = pony.Required(str)
    location = pony.Required(str)
    updated_at = pony.Required(date, default=lambda: dt.today())

    def __repr__(self):
        return '{}: {}'.format(self.id, self.username)


class Person(database.Entity):
    """Person, it's asociated with the persons_page"""
    name = pony.Required(str, unique=True)
    city = pony.Required(str)
    phone = pony.Required(str)

    def __repr__(self):
        return '{}: {}'.format(self.id, self.name)

pony.sql_debug(True)

database.generate_mapping(create_tables=True)
