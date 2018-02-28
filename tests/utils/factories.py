from random import randint

from faker import Faker

fake = Faker('en_US')


class User(object):
    def __init__(self):
        self.username = fake.name()
        self.email = '{}@gmail.com'.format(fake.name())
        self.age = randint(20, 35)
        self.phone = '{}{}{}'.format(randint(111, 999), randint(111, 999), randint(111, 999))
        self.location = fake.address()


class UserFactory(object):
    def __init__(self, quantity):
        self.users = []
        self.amount = quantity
        self._create_users()

    def _create_users(self):
        for _ in range(self.amount):
            self.users.append(User())


class Person(object):
    def __init__(self):
        self.name = fake.name()
        self.city = fake.city()
        self.phone = '{}{}{}'.format(randint(111, 999), randint(111, 999), randint(111, 999))
