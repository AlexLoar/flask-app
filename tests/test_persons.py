import json
import unittest

from pony.orm import db_session
from src import app

from tests.utils.factories import Person as PersonFake
from src.users.models import Person


class TestPersons(unittest.TestCase):
    def setUp(self):
        self.person = PersonFake().__dict__
        self.test_app = app.test_client()

    def test_get_persons(self):
        response = self.test_app.get('/persons/')
        self.assertEqual(response.status_code, 200)

    def test_get_person(self):
        with db_session:
            person = Person(**self.person)
        person_id = person.id
        response = self.test_app.get('/persons/person/{}'.format(person_id))
        with db_session:
            Person[person_id].delete()
        self.assertEqual(response.status_code, 200)

    @db_session
    def test_post_person(self):
        response = self.test_app.post('/persons/create', data=json.dumps(self.person), headers={'Content-Type': 'application/json'})
        response_body = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        person_name = response_body['Person'].values()[0]['name']
        Person.get(name=person_name).delete()

    def test_put_person(self):
        with db_session:
            person = Person(**PersonFake().__dict__)
        person_id = person.id
        self.person['city'] = 'Valencia'

        response = self.test_app.put('/persons/{}'.format(person_id), data=json.dumps(self.person),
                                      headers={'Content-Type': 'application/json'})

        self.assertEqual(response.status_code, 200)
        with db_session:
            person = Person[person_id]
            person.delete()

    def test_delete_person(self):
        with db_session:
            person = Person(**self.person)

        response = self.test_app.get('/persons/delete/{}'.format(person.id))

        self.assertEqual(response.status_code, 302)
